from zope.interface import implements
from zope.component import getUtilitiesFor
from zope.container.contained import Contained

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletAssignment
from plone.app.portlets.interfaces import IPortletAssignmentMapping

from Acquisition import Implicit

from persistent import Persistent

from .interfaces import IPanel
from .i18n import MessageFactory as _

PANEL_ANNOTATION_KEY = "collective.panels"


class Panel(Implicit, Persistent, Contained):
    implements(IPanel, IPortletAssignment, IPortletAssignmentMapping)

    __allow_access_to_unprotected_subobjects__ = 1

    # Currently, panel assignments do not carry state.
    data = None

    def __init__(self, name, layout, *assignments):
        self.__name__ = name
        self._assignments = list(assignments)
        self.layout = layout

    def __delitem__(self, name):
        for index, assignment in enumerate(self):
            if assignment.__name__ == name:
                break
        else:
            raise KeyError(name)

        self._assignments.pop(index)
        self._p_changed = True

    def __getitem__(self, name):
        for assignment in self:
            if assignment.__name__ == name:
                return assignment

        raise KeyError(name)

    def __setitem__(self, name, assignment):
        assignment.__name__ = name
        self._assignments.append(assignment)
        self._p_changed = True

    def __iter__(self):
        return iter(self._assignments)

    def __len__(self):
        return len(self._assignments)

    def __repr__(self):
        return '<%s name="%s" items="%d">' % (
            type(self.aq_base).__name__, self.__name__, len(self._assignments)
            )

    @property
    def available(self):
        return any(
            assignment.available for assignment in self
            )

    @property
    def title(self):
        return _(u"Panel ${name}", mapping={'name': self.__name__})

    def getAddablePortletTypes(self):
        types = (p[1] for p in getUtilitiesFor(IPortletType))

        return filter(
            lambda p: any(
                i for i in p.for_ if i.providedBy(self)
                ),
            types)

    def keys(self):
        return [assignment.__name__ for assignment in self]

    def updateOrder(self, keys):
        self._assignments.sort(
            key=lambda assignment: keys.index(assignment.__name__)
            )
        self._p_changed = True
