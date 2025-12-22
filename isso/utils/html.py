# -*- encoding: utf-8 -*-

import html
import re

import bleach
import mistune


class Sanitizer(object):

    # pattern to match a valid class attribute for code tags
    code_language_pattern = re.compile(r"^language-[a-zA-Z0-9]{1,20}$")

    @staticmethod
    def allow_attribute_class(tag, name, value):
        return name == "class" and bool(Sanitizer.code_language_pattern.match(value))

    def __init__(self, elements, attributes):
        # attributes found in Sundown's HTML serializer [1]
        # - except for <img> tag, because images are not generated anyways.
        # - sub and sup added
        #
        # [1] https://github.com/vmg/sundown/blob/master/html/html.c
        self.elements = ["a", "p", "hr", "br", "ol", "ul", "li",
                         "pre", "code", "blockquote",
                         "del", "ins", "strong", "em",
                         "h1", "h2", "h3", "h4", "h5", "h6", "sub", "sup",
                         "table", "thead", "tbody", "th", "td"] + elements

        # allowed attributes for tags
        self.attributes = {
            "table": ["align"],
            "a": ["href"],
            "code": Sanitizer.allow_attribute_class,
            "*": attributes
        }

    def sanitize(self, text):
        clean_html = bleach.clean(text, tags=self.elements, attributes=self.attributes, strip=True)

        def set_links(attrs, new=False):
            # Linker can misinterpret text as a domain name and create new invalid links.
            # To prevent this, we only allow existing links to be modified.
            if new:
                return None

            href_key = (None, u'href')

            if href_key not in attrs:
                return attrs
            if attrs[href_key].startswith(u'mailto:'):
                return attrs

            rel_key = (None, u'rel')
            rel_values = [val for val in attrs.get(rel_key, u'').split(u' ') if val]

            for value in [u'nofollow', u'noopener']:
                if value not in [rel_val.lower() for rel_val in rel_values]:
                    rel_values.append(value)

            attrs[rel_key] = u' '.join(rel_values)
            return attrs

        linker = bleach.linkifier.Linker(callbacks=[set_links])
        return linker.linkify(clean_html)


def Markdown(plugins=('strikethrough', 'superscript', 'url')):

    renderer = Unofficial()
    md = mistune.create_markdown(renderer=renderer, plugins=plugins)

    def inner(text):
        rv = md(text).rstrip("\n")
        if rv.startswith("<p>") or rv.endswith("</p>"):
            return rv
        return "<p>" + rv + "</p>"

    return inner


class Unofficial(mistune.HTMLRenderer):
    """A few modifications to process "common" Markdown.

    For instance, fenced code blocks (~~~ or ```) are just wrapped in <code>
    which does not preserve line breaks. If a language is given, it is added
    to <code class="language-$lang">, compatible with Highlight.js.
    """

    def blockcode(self, text, lang):
        lang = ' class="language-{0}"'.format(html.escape(lang)) if lang else ''
        return "<pre><code{1}>{0}</code></pre>\n".format(html.escape(text, False), lang)


class Markup(object):

    # Map the name of each misaka extension to a corresponding mistune plugin.
    # The mistune plugin may be None if mistune does not support similar functionality or it is already built in.
    _MISAKA_TO_MISTUNE = {
        'autolink': 'url',
        'disable-indented-code': None,
        'fenced-code': None,
        'footnotes': 'footnotes',
        'highlight': None,
        'math': 'math',
        'no-intra-emphasis': None,
        'quote': None,
        'strikethrough': 'strikethrough',
        'superscript': 'superscript',
        'tables': 'table',
        'underline': None,
    }

    def __init__(self, conf):
        self.plugins = self._misaka_to_mistune_plugins(conf.getlist("options"))

        parser = Markdown(plugins=self.plugins)
        # Filter out empty strings:
        allowed_elements = [x for x in conf.getlist("allowed-elements") if x]
        allowed_attributes = [x for x in conf.getlist("allowed-attributes") if x]

        # If images are allowed, source element should be allowed as well
        if 'img' in allowed_elements and 'src' not in allowed_attributes:
            allowed_attributes.append('src')
        sanitizer = Sanitizer(allowed_elements, allowed_attributes)

        self._render = lambda text: sanitizer.sanitize(parser(text))

    def render(self, text):
        return self._render(text)

    def _misaka_to_mistune_plugins(self, options):
        """Replace misaka extension names with mistune plugins.

        This allows users to keep using their existing markup options and get a rendered
        result with mistune that corresponds to misaka.
        """
        plugins = []
        for option in options:
            if option in self._MISAKA_TO_MISTUNE:
                if self._MISAKA_TO_MISTUNE[option] is not None:
                    # option is known misaka extension and maps to mistune plugin
                    plugins.append(self._MISAKA_TO_MISTUNE[option])
                else:
                    # option is known misaka extension but has no corresponding mistune plugin or functionality
                    # is already built in
                    pass
            else:
                # option is not a known misaka extension, so we assume that it is a mistune plugin
                plugins.append(option)

        return plugins
