from zope.security import checkPermission

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase

from .browser import layouts
from .browser import encode
from .browser import RenderContext
from .traversal import PanelManager


class faux_required:
    @staticmethod
    def render():
        return u'<div style="background-color: #666;">&nbsp;</div>'


class faux_optional:
    @staticmethod
    def render():
        return u'<div style="background-color: #999;">&nbsp;</div>'


class PanelViewlet(ViewletBase):
    """Self-contained panel viewlet.

    You can drop this viewlet into most viewlet managers, typically
    those that render above- or below content in the main display
    area.
    """

    index = ViewPageTemplateFile("viewlet.pt")

    @property
    def add_panel_url(self):
        return self.context.absolute_url() + "/++panel++%s/+" % \
               self.normalized_manager_name

    @property
    def can_add(self):
        # If there's an empty panel in set, we don't want to allow the
        # user to add another (empty) panel.
        for panel in self.panels:
            if len(panel) == 0:
                return False

        return True

    @property
    def can_manage(self):
        return checkPermission(
            "plone.app.portlets.ManagePortlets", self.context
            )

    @property
    def available_layouts(self):
        context = self.context

        ptypes = []
        for name, (pt, title, range) in layouts.items():
            # To-Do: Add support for any range.
            count = max(range)

            portlets = []
            for i in range:
                portlets.append(faux_optional)

            portlets.extend(
                [faux_required] *
                (count - len(portlets)))

            rcontext = RenderContext(name, portlets).__of__(context)
            renderer = rcontext.render

            ptypes.append({
                'name': name,
                'title': title,
                'icon': renderer,
                })

        # Sort by layout title
        ptypes.sort(key=lambda ptype: ptype['title'])

        return ptypes

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
