# -*- encoding: utf-8 -*-

import unittest

from isso.html import Sanitizer


class TestHTML(unittest.TestCase):

    def test_sanitizer(self):
        sanitizer = Sanitizer(elements=[], attributes=[])
        examples = [
            ('Look: <img src="..." />', 'Look: '),
            ('<a href="http://example.org/">Ha</a>',
             ['<a href="http://example.org/" rel="nofollow noopener">Ha</a>',
              '<a rel="nofollow noopener" href="http://example.org/">Ha</a>']),
            ('<a href="sms:+1234567890">Ha</a>', '<a>Ha</a>'),
            ('ld.so', 'ld.so'),
            ('/usr/lib/x86_64-linux-gnu/libc/memcpy-preload.so', '/usr/lib/x86_64-linux-gnu/libc/memcpy-preload.so'),
            ('<p style="visibility: hidden;">Test</p>', '<p>Test</p>'),
            ('<code class="language-cpp">Test</code>', '<code class="language-cpp">Test</code>'),
            ('<code class="test language-cpp">Test</code>', '<code>Test</code>'),
            ('<script>alert("Onoe")</script>', 'alert("Onoe")')]

        for (markup, expected) in examples:
            if isinstance(expected, list):
                self.assertIn(sanitizer.sanitize(markup), expected)
            else:
                self.assertEqual(sanitizer.sanitize(markup), expected)

    def test_sanitizer_extensions(self):
        sanitizer = Sanitizer(elements=["img"], attributes=["src"])
        examples = [
            ('<img src="cat.gif" />', '<img src="cat.gif">'),
            ('<script src="doge.js"></script>', '')]

        for (element, expected) in examples:
            self.assertEqual(sanitizer.sanitize(element), expected)
