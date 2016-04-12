Changes
=======

1.9 (2016-04-12)
----------------

- Show each panel HTML container element only when it contains one or
  more panel instances.
  [malthe]

- Added optional heading field which if set is rendered immediately
  before the panel.
  [malthe]

- Add Finnish localization
  [datakurre]

1.8 (2014-12-15)
----------------

- Move css browser resources to dedicated resource directory. Include an
  upgrade step for that.
  [thet]

- Move templates to dedicated templates directory and layout templtes to
  layouts directory.
  [thet]

- Plone 4.3.4 compatibility:
  Save __portlet_metadata__ on the portlet renderer.
  [sunew]

- The key should not be unicode (Traversal error).
  [sunew]

- The aq chain to the plone content object (the 'parent') can vary in length depending on
  where we render. Go up the aq chain until we are out of nested panels, portlet assignments,
  and panel managers. (The chain is long when rendering panels, maybe in the footer, on a
  panel portlet edit form).
  [sunew]

- Use the parent path as key (the plone content object), not the panel path. The key is used for
  transformations of urls in portlets, so this avoids urls like http://domain.com/++panel++plone-portalfooter/1/contact-info
  [sunew]

- Never catch ConflictErrors.
  [sunew]


1.7 (2014-04-24)
----------------

Bugfixes:

- Add missing upgrade step for installing the registry from released
  1.5 to the released 1.6. If you already managed to update to 1.6 by
  uninstalling / reinstalling the product you don't need this, that's
  why it's retrofitted in the 1.0 -> 1.1 metadata.xml version bump for sites
  coming from collective.panels 1.5.
  [fredvd]

- If portlet.available is a property it may throw an exception
  that will make the whole page rendering fail.
  [bosim]

Features:

- Added vertical layout.
  [bosim]

- Add missing styles for the Plone Classic theme.
  The Plone Classic theme doesn't have the grid-based styles present in
  the Sunburst theme. The styles added in this commit allow the
  grid-based styling used by the panels to work when the theme in use is
  Plone Classic or one based on it.
  [afrepues]

Misc:

- Put a warning instead of an error whenever the settings are not available
  (can be solved usually by profile update).
  [bosim]

- Updated danish translations
  [bosim]

- Add Dutch translations, update .po files. Add rebuild_i18n.sh script.
  [fredvd]


1.6 (2013-11-04)
----------------

Feature:

- Added navigation_local option - for setting local panel managers
  on INavigationRoot instead of ISiteRoot. Useful eg. with modules for
  multilingual content.
  [tmog]

Bugfix:

- Reworked the arrangement actions for the panels, due to the KSS dependency
  on plone.app.portlets has been removed.
  [bosim]

1.5 (2012-10-12)
----------------

Features:

- Added function to duplicate an existing panel.

- The "Manage panels" form now has a better default styling.

Bugfixes:

- Fixed "Add panels" action.

1.4 (2012-10-12)
----------------

Features:

- Portlet column spacing, and the omission of left- and right margins
  is now a global setting, and spacing can be expressed in floating
  point as a percentage of the available width.

  Previously, each panel had a spacing option.

  As a result of this, the HTML now uses CSS-classes to control width
  and position (previously inline styling).
  [chervol]

Implementation:

- The persistent ``Panel`` class now inherits from a new
  ``PortletContainerAssignment`` class, which is a portlet assignment
  that can contain other portlets. This is a generic base class that
  other portlet assignments can use.

1.3.2 (2012-06-15)
------------------

Bugfixes:

- Fixed template compatibility issue.

1.3.1 (2012-06-15)
------------------

Features:

- Added ``panel-${n}`` classes to the panel elements.

- Added ``portlet-${n}`` classes to the wrapper elements that render
  the portlet.

- The panel elements now have a class that matches the layout id.

- Added new spacing 'small', set at 0.55%.

1.3 (2012-06-15)
----------------

Features:

- A panel location can now be configured to be local to nearest site
  context. For instance, the footer manager can be configured in this
  way such that it's possible to use panels to create a site footer
  (which will be shown on all pages within that site).

- Layouts now have a required ``description`` attribute which will be
  shown in the "Manage panels" fieldset (instead of the title, which
  is usually very short and non-descriptive).

Bugfixes:

- Fixed issue where the error message would not get correctly
  rendered.

- Fixed issue #9: "Unexpected non-class object while iterating over
  viewlet managers".

1.2.3 (2012-06-08)
------------------

Bugfixes:

- The portlet ``settings`` dictionary was missing. Not strictly a bug,
  but the ``IPortletAssignmentSettings`` API exists to provide this
  information to the column renderer and we should provide it, too,
  for the portlet renderer wrapper template.

- Panel manager must provide ``get`` method. This fixes issue #8.

1.2.2 (2012-05-18)
------------------

Bugfixes:

- Fixed an issue that prevented the versioning tool to check in a
  document when a panel had been added. This fixes issue #5.

1.2.1 (2012-05-17)
------------------

Bugfixes:

- Fixed an issue with incompatible template syntax.

- Fixed an issue where a panel would not correctly return a
  representation string when not acquisition-wrapped. This addresses
  issue #5 (but turned out not quite to fix it entirely).

1.2 (2012-05-16)
----------------

Features:

- Added three new vertical layouts, assigned respectively 1/3, 1/2 and
  2/3 page width.

- Added option to select standard, double or triple spacing, all of
  which are given as a percentage of the page width.

Bugfixes:

- Fixed an issue with the panel adding view that made it impossible to
  add panels to content marked as private (the request would be
  unauthorized). This fixes issue #6.

- Views and resources are now registered against a package-specific
  browser layer. This ensures that the user interface is not available
  unless the product is installed (issue #7).

1.1 (2012-05-15)
----------------

Changes:

- Layout titles are now simply letters: A, B, C, etc. It turned out to
  be difficult to provide a short, descriptive title for each layout.

Features:

- Improved styling of adding interface.

- Added two new horizontal layouts that assign a fixed width of 1/3 to
  respectively the left-most and the right-most assignment.

Translation:

- Added Danish translation.

Bugfixes:

- Fixed layout "Left" in the case of a single assignment.

- The addable portlets check is now robust to misconfigured adding
  views and will log a warning instead of letting the exception
  trickle through.

- Assignments now get unique names. For example, if two calendar
  assignments are added, the second assignment gets the name
  "calendar-1".

- The panel info hash now correctly encodes a valid portlet
  manager. This fixes an issue where KSS-enabled portlets would
  operate incorrectly.

- The panel assignment class and traverser now inherit from
  ``OFS.Traversable.Traversable`` and implement the ``getId``
  method. This fixes an issue where a physical path would not be
  correctly computed.

1.0.2 (2012-04-19)
------------------

Bugfixes:

- Fixed issue where you could not add portlets to a panel other than
  the first (for a given manager). This fixes issue #3.

1.0.1 (2012-04-17)
------------------

Bugfixes:

- Fixed template formatting issue.

- Added markup from Plone's column renderer, wrapping each portlet in
  a structure that provides a unique portlet hash. Also, use a "safe"
  rendering method such that rendering may fail gracefully.

1.0 (2012-04-12)
----------------

- Initial public release.
