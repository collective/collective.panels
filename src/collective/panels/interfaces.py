from zope import schema
from zope.interface import Attribute
from zope.interface import Interface
from zope.container.interfaces import IContained
from zope.configuration.fields import Path
from zope.configuration.fields import GlobalInterface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from plone.app.portlets.interfaces import IColumn

from .i18n import MessageFactory as _


class ILayer(Interface):
    """Package-specific browser layer."""


class ILayout(Interface):
    """Marker for a layout dictionary."""


class IManagePanels(IDefaultBrowserLayer):
    """Enables panels management interface."""


class IPanel(IColumn, IContained):
    """A portlet panel.

    Register a portlet for this portlet manager type to enable them
    only for the panel (and not for the regular portlet column
    manager).
    """

    layout = Attribute("Assigned layout.")


class IPanelDirective(Interface):
    name = schema.TextLine(
        title=_("Name"),
        required=True
        )

    title = schema.TextLine(
        title=_("Title"),
        required=True
        )

    template = Path(
        title=_("Template"),
        required=True
        )

    layer = GlobalInterface(
        title=_("Layer"),
        required=True,
        default=IDefaultBrowserLayer,
        )
