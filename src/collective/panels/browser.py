import logging
import itertools

from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletAssignmentSettings
from plone.portlets.constants import CONTEXT_CATEGORY

from plone.app.portlets.browser.editmanager import EditPortletManagerRenderer
from plone.app.layout.viewlets.interfaces import IBelowContentBody

from plone.memoize.ram import cache
from plone.protect import protect
from plone.protect import PostOnly
from plone.protect import CheckAuthenticator

from zope.interface import alsoProvides
from zope.interface import providedBy
from zope.component import getAdapter
from zope.component import getAdapters
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.component import ComponentLookupError

from AccessControl import getSecurityManager
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from .i18n import MessageFactory as _

from zope.security import checkPermission

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase

from .interfaces import ILayout
from .interfaces import IManagePanels
from .traversal import PanelManager
from .traversal import encode


def addable_portlets_cache_key(function, view):
    roles = getSecurityManager().getUser().getRoles()
    return set(roles), view.manager.__name__


def batch(iterable, size):
    def ticker(x, s=size, a=[-1]):
        r = a[0] = a[0] + 1
        return r // s

    for k, g in itertools.groupby(iterable, ticker):
        yield g


def lookup_layouts(request):
    ptypes = []

    components = getAdapters((request, ), ILayout)

    for name, layout in components:
        ptypes.append(layout)

    # Sort by layout title
    ptypes.sort(key=lambda ptype: ptype['title'])

    return ptypes


def render(portlets, name, request):
    namespace = {'portlets': [portlet.render for portlet in portlets]}
    try:
        layout = getAdapter(request, ILayout, name=name)
    except ComponentLookupError:
        return _(u"Missing layout: ${name}.",
                 mapping={'name': name})

    template = layout['template']
    return template.pt_render(namespace)


def render_template(portlets, template):
    namespace = {'portlets': portlets}
    return template.pt_render(namespace)


class DisplayView(BrowserView):
    """This view displays a panel."""

    def __call__(self):
        # The parent object is the Plone content object here; we get
        # it from the acquisition chain.
        parent = self.context.aq_inner.aq_parent.aq_parent
        panel = self.context

        portlets = []
        for assignment in panel:
            settings = IPortletAssignmentSettings(assignment)
            if not settings.get('visible', True):
                continue

            try:
                portlet = getMultiAdapter(
                    (parent,
                     self.request,
                     self,
                     panel,
                     assignment), IPortletRenderer)
            except ComponentLookupError:
                logging.getLogger("panels").info(
                    "unable to look up renderer for '%s.%s'." % (
                        assignment.__class__.__module__,
                        assignment.__class__.__name__
                        )
                    )
                continue

            portlet.update()
            if portlet.available:
                portlets.append(portlet)

        return render(portlets, self.context.layout, self.request)


class ManageView(EditPortletManagerRenderer):
    """This view displays a management interface for a panel."""

    category = CONTEXT_CATEGORY

    def __init__(self, context, request):
        # This `manager` is the viewlet manager, or an object
        # emulating it.
        manager = context.aq_inner.aq_parent

        super(ManageView, self).__init__(context, request, manager, context)

    @cache(addable_portlets_cache_key)
    def addable_portlets(self):
        return super(ManageView, self).addable_portlets()

    @property
    def available_layouts(self):
        return lookup_layouts(self.request)

    @property
    def can_move_down(self):
        return self.__parent__.index(self.context.__name__) < \
               len(self.__parent__) - 1

    @property
    def can_move_up(self):
        return self.__parent__.index(self.context.__name__) > 0

    @property
    def key(self):
        return '/'.join(self.context.getPhysicalPath())

    @property
    def normalized_manager_name(self):
        return encode(self.__parent__.__name__)

    def context_url(self):
        return self.context.absolute_url()

    def manageUrl(self):
        return self.context_url() + "/++panel++%s" % \
               self.normalized_manager_name

    def baseUrl(self):
        return self.manageUrl() + "/%s" % self.context.__name__

    def portlets(self):
        assignments = tuple(self.context)
        return self.portlets_for_assignments(
            assignments, self.__parent__, self.baseUrl()
            )

    @protect(PostOnly)
    @protect(CheckAuthenticator)
    def delete(self, REQUEST=None):
        name = self.context.__name__
        del self.context.aq_inner.aq_parent[name]

        referer = self.request.get('HTTP_REFERER') or \
                  self.context.absolute_url()

        return self.request.response.redirect(referer)

    @protect(PostOnly)
    @protect(CheckAuthenticator)
    def change_layout(self, layout=None, REQUEST=None):
        self.context.layout = layout

        IStatusMessage(self.request).addStatusMessage(
            _(u"Layout changed."), type="info")

        referer = self.request.get('HTTP_REFERER') or \
                  self.context.absolute_url()

        return self.request.response.redirect(referer)


class ManagePanelsView(BrowserView):
    def __call__(self):
        alsoProvides(self.request, IManagePanels)

        if self.__name__ not in self.request.get('HTTP_REFERER', ''):
            IStatusMessage(self.request).addStatusMessage(
                _(u"This is the panel management interface. " \
                  u"Add a new panel or manage existing ones."),
                type="info")

        return self.context()


class BaseViewlet(ViewletBase):
    @property
    def can_manage(self):
        if IManagePanels.providedBy(self.request):
            return checkPermission(
                "plone.app.portlets.ManagePortlets", self.context
                )


class AddingViewlet(BaseViewlet):
    index = ViewPageTemplateFile("adding.pt")

    available_viewlet_managers = {
        IBelowContentBody: _(u"Below page content"),
        }

    @property
    def available_layouts(self):
        return lookup_layouts(self.request)

    @property
    def can_add(self):
        # If there's empty panels in all the available viewlet
        # managers, then we don't want to allow the user to add
        # another (empty) panel.
        #
        # This gets pretty esoteric when there's more than one viewlet
        # manager in play, but it's convenient for the case of one.
        for manager in self.iter_panel_managers():
            for panel in manager:
                if len(panel) == 0:
                    break
            else:
                return self.can_manage

        return False

    @property
    def default_viewlet_manager(self):
        for data in self.encode_viewlet_managers():
            return data

    @property
    def has_panels(self):
        # This is used to determine whether to initially collapse the
        # interface to add new panels. It should be collapsed if
        # there's a panel defined already.
        for manager in self.iter_panel_managers():
            for panel in manager:
                return True

        return False

    def iter_panel_managers(self):
        for name, iface in self.iter_viewlet_managers():
            name = encode(name)
            yield PanelManager(self.context, self.request, name)

    def iter_viewlet_managers(self):
        gsm = getSiteManager()
        lookup = gsm.adapters.lookupAll

        spec = tuple(map(providedBy, (
            self.context, self.request, self.__parent__
            )))

        for iface in self.available_viewlet_managers:
            for name, factory in lookup(spec, iface):
                yield name, iface

    def encode_viewlet_managers(self):
        for name, iface in self.iter_viewlet_managers():
            yield {
                'name': encode(name),
                'title': self.available_viewlet_managers[iface],
                }


class DisplayViewlet(BaseViewlet):
    index = ViewPageTemplateFile("display.pt")

    @property
    def normalized_manager_name(self):
        return encode(self.manager.__name__)

    @property
    def panels(self):
        # Wrap the panel in an acquisition context that provides
        # information about which viewlet manager the panel is
        # implicitly associated with.
        context = PanelManager(
            self.context, self.request,
            self.normalized_manager_name
            ).__of__(self.context)

        return tuple(context)
