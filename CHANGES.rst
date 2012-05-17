Changes
=======

1.2.1 (2012-05-17)
------------------

Bugfixes:

- Fixed an issue with incompatible template syntax.

- Fixed an issue where a panel would not correctly return a
  representation string when not acquisition-wrapped. This fixes issue
  #5.

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
