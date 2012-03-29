from zope.interface import Attribute
from zope.container.interfaces import IContained

from plone.app.portlets.interfaces import IColumn


class IPanel(IColumn, IContained):
    """A portlet panel.

    Register a portlet for this portlet manager type to enable them
    only for the panel (and not for the regular portlet column
    manager).
    """

    layout = Attribute("Assigned layout.")
