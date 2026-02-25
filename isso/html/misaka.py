import html
import logging

import misaka

from isso.html.markdown import Markdown

logger = logging.getLogger("isso")


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
        """
        :param conf: Takes a ConfigParser instance. Ideally, this would be a Section, but we need to parse both
                     the Markup and Markup.misaka sections.
        """
        if conf is not None:
            misaka_markup_section = conf.section('markup.misaka')
            markup_section = conf.section('markup')

            self._flags = misaka_markup_section.getlist("flags")
            self._extensions = misaka_markup_section.getlist("options")

            markup_flags = None
            if markup_section.has_option("flags"):
                markup_flags = markup_section.getlist("flags")
            if markup_flags:
                if self._flags:
                    logger.warning('The configuration setting flags is set in both sections Markup and Markup.misaka. '
                                   'The setting in section Markup has been deprecated and is ignored.')
                else:
                    self._flags = markup_section.getlist("flags")
                    logger.warning('The configuration setting flags in section Markup has been deprecated. Please move '
                                   'the setting to the new section Markup.misaka or preferably replace Misaka with '
                                   'Mistune entirely.')

            markup_options = None
            if markup_section.has_option("options"):
                markup_options = markup_section.getlist("options")
            if markup_options:
                if self._extensions:
                    logger.warning('The configuration setting options is set in both sections Markup and '
                                   'Markup.misaka. The setting in section Markup has been deprecated and is ignored.')
                else:
                    self._extensions = markup_section.getlist("options")
                    logger.warning('The configuration setting options in section Markup has been deprecated. Please '
                                   'move the setting to the new section Markup.misaka or preferably replace Misaka '
                                   'with Mistune entirely.')

            # Normalize render flags and extensions for Misaka 2.0, which uses
            # `dashed-case` instead of `snake_case` (Misaka 1.x) for options.
            self._flags = [x.replace("_", "-") for x in self._flags]
            self._extensions = [x.replace("_", "-") for x in self._extensions]

        logging.info("Loading Misaka with options: %s and flags: %s", self._extensions, self._flags)

        renderer = Unofficial(flags=self._flags)
        self.md = misaka.Markdown(renderer, extensions=self._extensions)

    @property
    def _markdown(self):
        return self.md

    def _render(self, text: str) -> str:
        return self.md(text)
