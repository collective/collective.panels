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

    heading = Attribute("Panel heading.")


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

    navigation_local = schema.Bool(
        title=_(u"Use navigation root"),
        description=_(u"Site-local panel managers will be assignable "
                      u"on navigation roots instead of only site roots "
                      u"if you select this option. Check this if you are "
                      u"using LinguaPlone, collective.multilingual or "
                      u"similar, and you want per-language Site-local "
                      u"panel managers."),
    )

    spacing = schema.Float(
        title=_(u"Column spacing"),
        description=_(u"This is the horizontal distance between "
                      u"portlets in a panel layout, expressed as "
                      u"a percentage of the available width."),
        required=False,
        default=1.25,
    )

    omit = schema.Bool(
        title=_(u"Omit margins"),
        description=_(u"Select this option to omit margins "
                      u"on the left- and right side of a "
                      u"panel."),
        required=False,
        default=True,
    )
