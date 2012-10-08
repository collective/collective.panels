import logging
from Products.CMFCore.utils import getToolByName
PROFILE_ID = 'profile-collective.panels:default'


def null_upgrade_step(setup_tool):
    """
    This is a null upgrade. Use it when nothing happens
     """
    pass


def update_registry(context, logger = None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.panels')
        logger.info("import regisitry setting")
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')