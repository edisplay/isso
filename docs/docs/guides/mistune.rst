Migration from Misaka to Mistune
=============

Introduction
------

Misaka was the rendering engine for converting Markdown to HTML in previous
versions of Isso. It has been replaced by Mistune. The Markdown syntax and
options between these engines is differing and this is to document the
differences.

For Misaka, plugins are configured with the ``options`` setting. Misaka actually
refers to plugins as extensions. The ``options`` setting must be in section
``[markup.misaka]`` in the server configuration file ``isso.cfg``.

For Mistune, plugins are configured with the ``plugins`` setting. The ``plugins``
setting must be in section ``[markup.mistune]`` in the server configuration file
``isso.cfg``.

Syntax differences
--------

HTML elements
^^^^^^^^^

Misaka allows HTML expressions like ``<em>Hi</em>`` in Markdown. This expression
will be rendered to HTML as is: ``<em>Hi</em>``. Mistune takes a stricter approach
and replaces any HTML element with rendered text like this: ``&lt;em&gt;Hi&lt;/em&gt;``.

Fenced code
^^^^^^^^^

In Misaka, fenced code can be marked by enclosing the code block in three backticks
``````` or by putting four space characters in front of each code line. Mistune
only understands three backticks.

Plugins
------

Fenced-code
^^^^^^

Mistune always renders fenced code. The behavior is not configurable and no
fenced-code plugin exists for Mistune.

Superscript
^^^^^^^

This plugin exists in both engines with the same name ``superscript``. The
Markdown syntax is differing however.

Misaka: ``^(superscripted_text)``

Mistune: ``^superscripted_text^``
