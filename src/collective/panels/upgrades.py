import logging
from Products.CMFCore.utils import getToolByName

PROFILE_ID = 'profile-collective.panels:default'


# upgrade 1.0 to 1.1

def run_registry_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')


def add_plone_grid_styles(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.panels')
        logger.info("Adding new stylesheets to CSS registry")
    css_registry = getToolByName(context, 'portal_css')
    css_registry.registerStylesheet('panels-grid.css')
    css_registry.registerStylesheet(
        '++resource++panels-grid-classic-theme.css')


# upgrade 1.1 to 2

def upgrade_11_2__css_registry(context):
    logger = logging.getLogger('collective.panels')
    logger.info("Upgrading stylesheets in CSS registry")
    css_registry = getToolByName(context, 'portal_css')
    css_registry.unregisterResource(
        '++resource++panels-grid-classic-theme.css')
    css_registry.unregisterResource('++resource++panels.css')
    context.runImportStepFromProfile(PROFILE_ID, 'cssregistry')
