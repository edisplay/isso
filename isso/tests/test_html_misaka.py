import unittest
import textwrap

from isso import config
from isso.html import Markup
from isso.html.misaka import MisakaMarkdown


class TestHTMLMisaka(unittest.TestCase):

    def test_markdown(self):
        conf = config.new({
            "markup.misaka": {
                "options": "",
                "flags": ""
            }
        })
        convert = MisakaMarkdown(conf)
        examples = [
            ("*Ohai!*", "<p><em>Ohai!</em></p>"),
            ("<em>Hi</em>", "<p><em>Hi</em></p>"),
            ("http://example.org/", '<p>http://example.org/</p>')]

        for (markup, expected) in examples:
            self.assertEqual(expected, convert.render(markup))

    def test_markdown_plugins(self):
        conf = config.new({
            "markup.misaka": {
                "options": "strikethrough, superscript",
                "flags": ""
            }
        })
        convert = MisakaMarkdown(conf)
        examples = [
            ("~~strike~~ through", "<p><del>strike</del> through</p>"),
            ("sup^(script)", "<p>sup<sup>script</sup></p>")]

        for (markup, expected) in examples:
            self.assertEqual(expected, convert.render(markup))

    def test_github_flavoured_markdown(self):
        conf = config.new({
            "markup.misaka": {
                "options": "fenced-code",
                "flags": ""
            }
        })
        convert = MisakaMarkdown(conf)

        # without lang
        _in = textwrap.dedent("""\
            Hello, World

            ```
            #!/usr/bin/env python
            print("Hello, World")""")
        _expected = textwrap.dedent("""\
            <p>Hello, World</p>
            <pre><code>#!/usr/bin/env python
            print("Hello, World")
            </code></pre>""")

        self.assertEqual(_expected, convert.render(_in))

        # w/ lang
        _in = textwrap.dedent("""\
            Hello, World

            ```python
            #!/usr/bin/env python
            print("Hello, World")""")
        _expected = textwrap.dedent("""\
            <p>Hello, World</p>
            <pre><code class="language-python">#!/usr/bin/env python
            print("Hello, World")
            </code></pre>""")

        self.assertEqual(_expected, convert.render(_in))

    def test_render(self):
        conf = config.new({
            "markup": {
                "renderer": "misaka",
                "allowed-elements": "",
                "allowed-attributes": ""
            },
            "markup.misaka": {
                "options": "autolink",
                "flags": ""
            }
        })
        convert = Markup(conf)
        self.assertIn(convert.render("http://example.org/ and sms:+1234567890"),
                      ['<p><a href="http://example.org/" rel="nofollow noopener">http://example.org/</a> and sms:+1234567890</p>',
                       '<p><a rel="nofollow noopener" href="http://example.org/">http://example.org/</a> and sms:+1234567890</p>'])

    def test_sanitized_render_extensions(self):
        """Options should be normalized from both dashed-case or snake_case (legacy)"""
        conf = config.new({
            "markup.misaka": {
                "options": "no_intra_emphasis",  # Deliberately snake_case
                "flags": "",
            }
        })
        convert = MisakaMarkdown(conf)
        self.assertEqual('<p>foo_bar_baz</p>', convert.render("foo_bar_baz"))

        conf.set("markup.misaka", "options", "no-intra-emphasis")  # dashed-case
        convert = MisakaMarkdown(conf)
        self.assertEqual('<p>foo_bar_baz</p>', convert.render("foo_bar_baz"))

    def test_code_blocks(self):
        convert = MisakaMarkdown()
        examples = [
            ("```\nThis is a code-fence. <hello>\n```", "<p><pre><code>This is a code-fence. &lt;hello&gt;\n</code></pre></p>"),
            ("```cpp\nThis is a code-fence. <hello>\n```", "<p><pre><code class=\"language-cpp\">This is a code-fence. &lt;hello&gt;\n</code></pre></p>"),
            ("    This is a four-character indent. <hello>", "<p><pre><code>This is a four-character indent. &lt;hello&gt;\n</code></pre></p>")]

        for (markup, expected) in examples:
            self.assertEqual(expected, convert.render(markup))
