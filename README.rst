Overview
========

This add-on extends Plone with "portlet panels", where a panel is a
container for a number of portlet assignments.

Panels can be added to any viewlet manager in principle, although in
the default setup, the panel management interface is registered only
for the "below content" manager.

There's a choice of layout for each panel, selected when the panel is
first added with an option to change later on. These layouts are
registered as components using an included ZCML-directive.

Use the directive to add additional layouts::

  <browser:panel
      name="example"
      title="Example"
      template="templates/example.pt"
      layer=".interfaces.IThemeSpecific"
      />

The package includes a layout that arranges portlets horizontally,
automatically adjusting to equal width.


Author
------

Malthe Borch <mborch@gmail.com>
