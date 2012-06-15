from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from plone.app.layout.viewlets import interfaces

from .i18n import MessageFactory as _


class ManagerVocabulary(object):
    implements(IVocabularyFactory)

    # Order is important here; the default location will be the first
    # available (non-hidden) manager.
    all_viewlet_managers = (
        (interfaces.IBelowContentBody, _(u"Below page content")),
        (interfaces.IAboveContentBody, _(u"Above page content")),
        (interfaces.IPortalFooter, _(u"Portal footer")),
        (interfaces.IPortalTop, _(u"Portal top")),
        )

    def __call__(self, context):
        return SimpleVocabulary([
            SimpleTerm(interface, interface.__name__, title)
            for (interface, title) in self.all_viewlet_managers
            ])


managers = ManagerVocabulary()
