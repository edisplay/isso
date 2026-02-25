from abc import ABC, abstractmethod


class Markdown(ABC):
    """ Abstract base class for rendering Markdown to HTML """

    @property
    @abstractmethod
    def _markdown(self):
        pass

    @abstractmethod
    def _render(self, text: str) -> str:
        pass

    def render(self, text: str) -> str:
        rv = self._render(text).rstrip("\n")
        if rv.startswith("<p>") or rv.endswith("</p>"):
            return rv
        return "<p>" + rv + "</p>"
