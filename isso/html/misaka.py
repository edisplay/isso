import html

import misaka

from isso.html.markdown import Markdown


class Unofficial(misaka.HtmlRenderer):
    """A few modifications to process "common" Markdown.

    For instance, fenced code blocks (~~~ or ```) are just wrapped in <code>
    which does not preserve line breaks. If a language is given, it is added
    to <code class="language-$lang">, compatible with Highlight.js.
    """

    def blockcode(self, text, lang):
        lang = ' class="language-{0}"'.format(html.escape(lang)) if lang else ''
        return "<pre><code{1}>{0}</code></pre>\n".format(html.escape(text, False), lang)


class MisakaMarkdown(Markdown):
    _flags = []
    _extensions = ("autolink", "fenced-code", "no-intra-emphasis", "strikethrough", "superscript")

    def __init__(self, conf=None):
        if conf is not None:
            self._flags = conf.getlist("flags")
            self._extensions = conf.getlist("options")

            # Normalize render flags and extensions for Misaka 2.0, which uses
            # `dashed-case` instead of `snake_case` (Misaka 1.x) for options.
            self._flags = [x.replace("_", "-") for x in self._flags]
            self._extensions = [x.replace("_", "-") for x in self._extensions]

        renderer = Unofficial(flags=self._flags)
        self.md = misaka.Markdown(renderer, extensions=self._extensions)

    @property
    def _markdown(self):
        return self.md

    def _render(self, text: str) -> str:
        return self.md(text)
