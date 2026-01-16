Migration from Misaka to Mistune
=============

Introduction
------

Misaka was the rendering engine for converting Markdown to HTML in previous
versions of Isso. It has been replaced by Mistune. The Markdown syntax and
options between these engines is differing and this is to document the
differences.

Plugins
------

Superscript
^^^^^^^

This plugin exists in both engines with the same name ``superscript``. The
Markdown syntax is different however.

Misaka: ``^(superscripted_text)``

Mistune: ``^superscripted_text^``
