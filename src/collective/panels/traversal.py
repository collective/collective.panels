from zope.annotation.interfaces import IAttributeAnnotatable
from zope.interface import implements
from zope.component import adapts
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.traversing.interfaces import ITraversable

from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import ILocalPortletAssignable
from plone.app.portlets.assignable import localPortletAssignmentMappingAdapter

from zExceptions import BadRequest, NotFound
from Acquisition import aq_base
from Acquisition import Implicit
from Acquisition import ExplicitAcquisitionWrapper
from OFS.Traversable import Traversable

from Products.statusmessages.interfaces import IStatusMessage

from .content import Panel
from .interfaces import IPanel
from .i18n import MessageFactory as _


def encode(name):
    return name.replace('.', '-')


def decode(name):
    return name.replace('-', '.')


class PanelManager(Implicit, Traversable):
    implements(IBrowserPublisher, IPortletAssignmentMapping, ILocalPortletAssignable)

    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, context, request, location, name):
        self.__name__ = decode(name)
        self.context = context
        self.request = request

        # We use `self` as the viewlet manager here because only the
        # name is actually needed.
        self._mapping = localPortletAssignmentMappingAdapter(location, self)

    def __delitem__(self, name):
        del self._mapping[name]
        IStatusMessage(self.request).addStatusMessage(
            _(u"Panel removed."), type="info")

    def __getitem__(self, name):
        if name == "+":
            # To-Do: Ideally this should be POST-only to protect
            # against CSRF. It's not critical.
            try:
                layout = self.request.TraversalRequestNameStack.pop()
            except IndexError:
                raise BadRequest("Missing layout.")

            def adding():
                """Add panel, then redirect to referer."""

                self.addPanel(layout)

                referer = (
                    self.request.get('HTTP_REFERER') or
                    self.context.absolute_url()
                )

                return self.request.response.redirect(referer)

            return ExplicitAcquisitionWrapper(adding, self)

        for panel in self.getAssignments():
            if panel.__name__ == name:
                return panel.__of__(self)

        raise KeyError(name)

    def getAssignments(self):
        """Return panel assignments.

        Note that panels are specialized portlet assignments. We make
        sure that the contained assignment implement the ``IPanel``
        interface.
        """

        assignments = self._mapping.values()
        return filter(IPanel.providedBy, assignments)

    def addPanel(self, *args):
        """Add panel with the provided layout."""

        # Find first available integer; we use this as the
        # panel name.
        n = 1
        for panel in self.getAssignments():
            i = int(panel.__name__)
            if i >= n:
                n = i + 1

        panel = Panel(str(n), *args)
        aq_base(self._mapping)[panel.__name__] = panel

        IStatusMessage(self.request).addStatusMessage(
            _(u"Panel added."), type="info")

        return panel

    def __iter__(self):
        return (
            assignment.__of__(self) for assignment
            in self.getAssignments()
        )

    def __len__(self):
        return len(tuple(iter(self)))

    def getId(self):
        return "++panel++%s" % encode(self.__name__)

    def publishTraverse(self, request, name):
        try:
            return self[name]
        except KeyError:
            raise NotFound(self, name, request)

    def index(self, name):
        for index, panel in enumerate(self):
            if panel.__name__ == name:
                return index

        return -1

    def keys(self):
        return self._mapping.keys()

    def updateOrder(self, keys):
        self._mapping.updateOrder(keys)


class PanelTraverser(object):
    implements(ITraversable)
    adapts(IAttributeAnnotatable, IBrowserRequest)

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        if not name:
            raise BadRequest("Must provide panel name.")

        return PanelManager(self.context, self.request, self.context, name)
