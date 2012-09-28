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

    description = schema.TextLine(
        title=_("Description"),
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


class IGlobalSettings(Interface):
    site_local_managers = schema.Set(
        title=_(u"Site-local panel managers"),
        description=_(u"The locations listed here will be assignable "
                      u"only at sites (typically Plone's site "
                      u"root, unless local sites are present)."),
        required=False,
        value_type=schema.Choice(
            vocabulary="collective.panels.vocabularies.Managers",
            )
        )
    spacing = schema.Float(
        title =  _(u"Columns spacing"),
        description = _(u'The horisontal distance between portlets in panels'),
        required = False,
        default = 1.25,
        )
    omit = schema.Bool(
        title = _(u'Omit left and right margins'),
        description = _(u'If checked the right and left margin will be 0'),
        required = False,
        default = True
        )
    
