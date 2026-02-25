import unittest
import textwrap

from isso import config
from isso.html import Markup
from isso.html.mistune import MistuneMarkdown


class TestHTMLMistune(unittest.TestCase):

    def test_markdown(self):
        conf = config.new({
            "markup.mistune": {
                "plugins": "",
                "parameters": ""
            }
        })
        convert = MistuneMarkdown(conf.section("markup.mistune"))
        examples = [
            ("*Ohai!*", "<p><em>Ohai!</em></p>"),
            ("<em>Hi</em>", "<p>&lt;em&gt;Hi&lt;/em&gt;</p>"),
            ("http://example.org/", '<p>http://example.org/</p>')]

        for (markup, expected) in examples:
            self.assertEqual(expected, convert.render(markup))

    def test_markdown_plugins(self):
        conf = config.new({
            "markup.mistune": {
                "plugins": "strikethrough, superscript",
                "parameters": ""
            }
        })
        convert = MistuneMarkdown(conf.section('markup.mistune'))
        examples = [
            ("~~strike~~ through", "<p><del>strike</del> through</p>"),
            ("sup^script^", "<p>sup<sup>script</sup></p>")]

        for (markup, expected) in examples:
            self.assertEqual(expected, convert.render(markup))

    def test_github_flavoured_markdown(self):
        convert = MistuneMarkdown()

        # without lang
        _in = textwrap.dedent("""\
            Hello, World

            ```
            #!/usr/bin/env python
            print("Hello, World")""")
        _expected = textwrap.dedent("""\
            <p>Hello, World</p>
            <pre><code>#!/usr/bin/env python
            print(&quot;Hello, World&quot;)
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
            print(&quot;Hello, World&quot;)
            </code></pre>""")

        self.assertEqual(_expected, convert.render(_in))

    def test_render(self):
        conf = config.new({
            "markup": {
                "renderer": "mistune",
                "allowed-elements": "",
                "allowed-attributes": ""
            },
            "markup.mistune": {
                "plugins": "url",
                "parameters": ""
            }
        })
        convert = Markup(conf)
        self.assertIn(convert.render("http://example.org/ and sms:+1234567890"),
                      ['<p><a href="http://example.org/" rel="nofollow noopener">http://example.org/</a> and sms:+1234567890</p>',
                       '<p><a rel="nofollow noopener" href="http://example.org/">http://example.org/</a> and sms:+1234567890</p>'])

    def test_code_blocks(self):
        convert = MistuneMarkdown()
        examples = [
            ("```\nThis is a code-fence. <hello>\n```", "<p><pre><code>This is a code-fence. &lt;hello&gt;\n</code></pre></p>"),
            ("```cpp\nThis is a code-fence. <hello>\n```", "<p><pre><code class=\"language-cpp\">This is a code-fence. &lt;hello&gt;\n</code></pre></p>")]

        for (markup, expected) in examples:
            self.assertEqual(expected, convert.render(markup))
