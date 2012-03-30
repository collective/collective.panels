import logging
import itertools

from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletAssignmentSettings
from plone.portlets.constants import CONTEXT_CATEGORY

from plone.app.portlets.browser.editmanager import EditPortletManagerRenderer

from plone.memoize.ram import cache
from plone.protect import protect
from plone.protect import PostOnly
from plone.protect import CheckAuthenticator

from zope.component import getMultiAdapter
from zope.component import ComponentLookupError
from zope.pagetemplate.pagetemplatefile import PageTemplateFile

from AccessControl import getSecurityManager
from Acquisition import Implicit
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from .i18n import MessageFactory as _

layouts = {
    'deco16': (
        PageTemplateFile("layouts/deco16.pt"),
        _(u"Deco 16"),
        xrange(1, 5)
        ),
    'left16': (
        PageTemplateFile("layouts/left16.pt"),
        _(u"Left 16"),
        xrange(1, 5)
        ),
    'right16': (
        PageTemplateFile("layouts/right16.pt"),
        _(u"Right 16"),
        xrange(1, 5)
        ),
    }


def encode(name):
    return name.replace('.', '-')


def decode(name):
    return name.replace('-', '.')


def addable_portlets_cache_key(function, view):
    roles = getSecurityManager().getUser().getRoles()
    return set(roles), view.manager.__name__


def batch(iterable, size):
    sourceiter = iter(iterable)
    while True:
        batchiter = itertools.islice(sourceiter, size)
        yield itertools.chain([batchiter.next()], batchiter)


class RenderContext(Implicit):
    """Portlet rendering context."""

    def __init__(self, name, portlets=None):
        self.name = name
        self.portlets = portlets or []

    def add(self, portlet):
        self.portlets.append(portlet)

    def render(self):
        template, title, count = layouts[self.name]
        return template.pt_render(self.__dict__)


class DisplayView(BrowserView):
    """This view displays a panel."""

    def __call__(self):
        # The parent object is the Plone content object here; we get
        # it from the acquisition chain.
        parent = self.context.aq_inner.aq_parent.aq_parent
        panel = self.context

        context = RenderContext(self.context.layout).__of__(parent)

        pt, title, slots = layouts[panel.layout]
        count = max(slots)

        output = []
        for assignments in batch(panel, count):
            for assignment in assignments:
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
                    context.add(portlet)

            result = context.render()
            output.append(result)

        return u"\n".join(output)


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
        ptypes = [
            {'name': name, 'title': title}
            for name, (pt, title, range) in layouts.items()
            ]

        ptypes.sort(key=lambda ptype: ptype['title'])
        return ptypes

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
