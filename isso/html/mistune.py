import logging

import mistune

from isso.html.markdown import Markdown

logger = logging.getLogger("isso")


class MistuneMarkdown(Markdown):
    _parameters = []
    _plugins = ("strikethrough", "subscript", "superscript", "url")

    def __init__(self, conf=None):
        if conf is not None:
            self._plugins = conf.getlist("plugins")
            # If the list of plugins is empty, getlist returns ['']. Mistune however wants a None:
            if not self._plugins or not self._plugins[0]:
                self._plugins = None

            self._parameters = conf.getlist("parameters")

        hard_wrap = True if "hard_wrap" in self._parameters else False

        logging.info("Loading Mistune with plugins: %s and parameters: %s", self._plugins, self._parameters)

        # The isso.cfg syntax does not allow to set a parameter like escape to False. With Misaka, HTML was not always
        # escaped, but it seems prudent to enable that here.
        # If we ever want to make escape configurable, we could add a parameter no-escape.
        self.md = mistune.create_markdown(escape=True, hard_wrap=hard_wrap, plugins=self._plugins)

    @property
    def _markdown(self):
        return self.md

    def _render(self, text: str) -> str:
        return self.md(text)
