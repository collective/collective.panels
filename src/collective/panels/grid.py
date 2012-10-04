from fractions import Fraction

from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component import ComponentLookupError
from .interfaces import IGlobalSettings


def grid(spacing, omit, cells):
    """the grid calculation"""
    margin = spacing
    spacing = 2 * spacing
    css = ""
    if omit:
        spacing = 0
        css += ".panels div.width-full {width: 100%}\n"
        css += ".panels div.position-0 {margin-left: -100%}\n"
    else:
        css += ".panels div.width-full {width: %.4f%%}\n" % \
                (100.0 - 2 * margin)
        css += ".panels div.position-0 {margin-left: %.4f%%}\n" % \
                (margin - 100.0)
    pcss = ""
    for i in range(2, cells + 1):
        for k in range(1, i):
            fraction = Fraction(k, i)
            if k != 1 and fraction.denominator != i:
                continue

            width = (100.0 - (i - 1) * 2 * margin - spacing) / i * k + \
                    2 * margin * (k - 1)
            css += ".panels div.width-%s\\3a %s {width: %.4f%%}\n" % \
                    (fraction.numerator, fraction.denominator, width)
            pos = width + 2 * margin + spacing / 2 - 100
            pcss += (".panels div.position-%s\\3a %s " + \
                   "{margin-left: %.4f%%}\n") % \
                    (fraction.numerator, fraction.denominator, pos)

    return css + pcss


class GridView(BrowserView):
    cells = 6

    def __call__(self):
        """render the CSS"""
        try:
            settings = getUtility(IRegistry).forInterface(IGlobalSettings)
        except (ComponentLookupError, KeyError):
            spacing = IGlobalSettings['spacing'].default
            omit = IGlobalSettings['omit'].default
        else:
            spacing = settings.spacing
            omit = settings.omit

        response = self.request.response
        response.setHeader('Content-Type', 'text/css;;charset=utf-8')
        return grid(spacing, omit, self.cells)
