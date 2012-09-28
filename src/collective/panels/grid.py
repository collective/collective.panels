from fractions import Fraction

from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from .interfaces import IGlobalSettings


class GridView(BrowserView):

    def __init__(self, context, request):
        """initialize view, read settings"""
        super(GridView, self).__init__(context, request)
        self.spacing = -1
        self.omit = True
        self.cells = 6      #max number of colums
        try:
            settings = getUtility(IRegistry).forInterface(IGlobalSettings)
        except (ComponentLookupError, KeyError):
            # This (non-critical) error is reported elsewhere. The
            # product needs to be installed before we let users manage
            # panels.
            return False
        else:
            if settings.spacing >= 0:
                self.spacing = settings.spacing
            self.omit = settings.omit


    def __call__(self):
        """render the CSS"""
        if self.spacing == -1:
            return "/* panels settings not installed properly */"
        self.request.RESPONSE.setHeader('Content-Type','text/css;;charset=utf-8')
        return self.grid(self.spacing, self.omit)


    def grid(self, spacing, omit):
        """the grid calculation"""
        margin = spacing
        spacing = 2 * spacing
        css = ""
        if omit:
            spacing = 0
            css += ".panels div.width-full { width: 100%; }\n"
            css += ".panels div.position-0 { margin-left: -100%; }\n"
        else:
            css += ".panels div.width-full { width: %.4f%%; }\n" % \
                    (100.0 - 2 * margin)
            css += ".panels div.position-0 { margin-left: %.4f%%; }\n" % \
                    (margin - 100.0)
        pcss = ""
        for i in range(2, self.cells+1):
            for k in range(1, i):
                fraction = Fraction(k,i)
                if k!=1 and fraction.denominator != i:
                    continue
                
                width = (100.0 - (i - 1) * 2 * margin - spacing) / i * k + \
                        2 * margin * (k - 1)
                css += ".panels div.width-%s\\3a %s {width: %.4f%%}\n" % \
                        (fraction.numerator, fraction.denominator, width)
                pos = width + 2 * margin + spacing / 2 - 100
                pcss += (".panels div.position-%s\\3a %s "+\
                       "{margin-left: %.4f%%;}\n") % \
                        (fraction.numerator, fraction.denominator, pos)

        return css + pcss





