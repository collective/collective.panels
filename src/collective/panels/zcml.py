from zope.component.zcml import handler
from zope.pagetemplate.pagetemplatefile import PageTemplateFile

from .interfaces import ILayout


def panel(_context, name, title, description, template, layer):
    component = {
        'name': name,
        'title': title,
        'description': description,
        'template': PageTemplateFile(template),
        }

    adapter = lambda request: component

    _context.action(
        discriminator=('panel', name, layer),
        callable=handler,
        args=(
            'registerAdapter',
            adapter, (layer, ), ILayout,
            name, _context.info),
        )
