Panels are sets of portlets appearing in various layout configurations
which you can insert into a selection of Plone's existing locations
(above and below page contents, portal top and footer).

It aims to render a number of existing add-ons obsolete, including
`Collage <http://pypi.python.org/pypi/Products.Collage>`_,
`collective.portletpage
<http://pypi.python.org/pypi/collective.portletpage>`_ and
`Products.ContentWellPortlets
<http://pypi.python.org/pypi/Products.ContentWellPortlets>`_. The
functionality represented by these add-ons is mostly available in
panels, too, and comes in an implementation that builds directly on
Plone's portlets framework.

There's an alternative to panels still in development in Carlos de la
Guardia's `collective.cover
<https://github.com/collective/collective.cover>`_. It supports
a number of advanced use-cases mostly related to workflow and
security. Panels does not currently integrate with Plone's permission
system except require the blanket "can manage portlets" permission.


Compatibility: Plone 4+ required.


Introduction
============

You often have a need to add supplemental content to existing pages,
content items or folders.

The included portlets infrastructure serves some, but not all of these
needs, letting you add portlets in the left and right column, which
are inherited down the content hierarchy.

Panels provide a simple mechanism to add portlets to additional
locations, without inheritance, and let you display portlets in
different layouts.


Examples
--------

*Front page*

    Instead of, or in addition to, a page acting as the default
    content on a folder, you can create a collage of portlets and
    display it below an introductory text.

    There's a lot of flexibility because you can integrate the panel
    display with Plone's built-in content views. For instance, you
    could provide a search interface in addition to the standard
    folder listing.


*Supplement static content*

    Use panels to add portlets above or below a static page.


*Features or advertisement*

    Add panels to the 'portal top' location which by default renders
    just below the section navigation for an impressive effect.


Documentation
=============

Usage
-----

To create a new panel, or manage existing ones, the editor clicks the
"Manage panels" link appearing in the footer (it links to
``@@manage-panels``) — similar to Plone's column portlets.

The management view is an overlay of the default content view.

*Creating a new panel*

    To create a new panel, there's a collapsible form appearing just below
    the page title ("Add panel").

    If no panels exist already, the add form appears open to begin
    with.

    Then, simply choose a location (a default choice is already
    provided), and select a layout. Then add portlets using the
    "Manage panel" form (see next).

*Managing existing panels*

    In the management interface, a collapsible form appears below
    existing panels ("Manage panel").

    This is similar to Plone's standard portlet interface and in fact
    uses it directly.

    It provides options to add a new portlet, change panel layout or
    manage existing portlet assignments.


Locations
---------

The management interface checks with Plone's viewlet visibility
settings to list only the applicable adding locations. This allows an
administrator to visit the portal's ``@@manage-viewlets`` screen and
put a restriction on panel locations.

Adding additional locations is currently not supported. The limitation
here is that Plone's viewlet manager framework does not provide
labels, or other enumeration.


Layouts
-------

There's a choice of layout for each panel, selected when the panel is
first added, with an option to change later on. These layouts are
registered as components using an included ZCML-directive.

Use the directive to add additional layouts::

  <browser:panel
      name="example"
      title="Example"
      template="templates/example.pt"
      layer=".interfaces.IThemeSpecific"
      />


License
-------

GPLv3 (http://www.gnu.org/licenses/gpl.html).


Author
------

Malthe Borch <mborch@gmail.com>

