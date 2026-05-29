from html import escape
from xmldoc2html.rendering.syntax_highlighter import SyntaxHighlighter
from xmldoc2html.core.model import (
    Bold,
    Code,
    Document,
    Heading,
    Italic,
    LineBreak,
    Link,
    ListBlock,
    Node,
    Paragraph,
    Section,
    TextNode,
    Image,
    Member,
    Summary,
    Param,
    Returns,
    Reference,

)
'''Превращает внутреннюю модель документа в готовый html код'''

class HtmlRenderer:
    def __init__(self):
        self.highlighter = SyntaxHighlighter()

    def render(self, document: Document) -> str:
        title = escape(document.title or "Document")
        body_parts: list[str] = []
        toc = self._render_toc(document)

        if document.title:
            body_parts.append(f"<h1>{escape(document.title)}</h1>")

        if toc:
            body_parts.append(toc)

        body_parts.extend(self._render_node(node) for node in document.children)
        body = "\n".join(body_parts)

        return (
            "<!doctype html>\n"
            "<html lang=\"en\">\n"
            "<head>\n"
            "  <meta charset=\"utf-8\">\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            f"  <title>{title}</title>\n"
            "  <style>\n"
            "    .kw { color: blue; font-weight: bold; }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            f"{body}\n"
            "</body>\n"
            "</html>\n"
        )

    def _render_node(self, node: Node) -> str:
        match node:
            case TextNode(text=text):
                return escape(text)
            case Paragraph(children=children):
                return f"<p>{self._render_inline(children)}</p>"
            case Heading(level=level, children=children):
                safe_level = max(1, min(level, 6))
                return f"<h{safe_level}>{self._render_inline(children)}</h{safe_level}>"
            case Section(children=children):
                inner = "\n".join(self._render_node(child) for child in children)
                return f"<section>\n{inner}\n</section>"
            case ListBlock(kind=kind, items=items):
                rendered_items = "\n".join(
                    f"  <li>{self._render_inline(item)}</li>" for item in items
                )
                return f"<{kind}>\n{rendered_items}\n</{kind}>"
            case Bold(children=children):
                return f"<strong>{self._render_inline(children)}</strong>"
            case Italic(children=children):
                return f"<em>{self._render_inline(children)}</em>"
            case Code(children=children):
                raw = self._render_inline(children)
                highlighted = self.highlighter.highlight(raw)
                return f"<code>{highlighted}</code>"
            case LineBreak():
                return "<br>"
            case Link(href=href, children=children):
                return f"<a href=\"{escape(href, quote=True)}\">{self._render_inline(children)}</a>"
            case Image(src=src, alt=alt):
                return f"<img src=\"{escape(src, quote=True)}\" alt=\"{escape(alt, quote=True)}\">"
            case Member(name=name, children=children):
                safe_id = escape(name.replace(":", "-").replace(".", "-"), quote=True)
                inner = "\n".join(self._render_node(child) for child in children)
                return f'<section id="{safe_id}" class="member">\n<h2>{escape(name)}</h2>\n{inner}\n</section>'
            case Summary(children=children):
                return f'<div class="summary"><strong>Summary:</strong> {self._render_inline(children)}</div>'
            case Param(name=name, children=children):
                return f'<div class="param"><strong>{escape(name)}:</strong> {self._render_inline(children)}</div>'
            case Returns(children=children):
                return f'<div class="returns"><strong>Returns:</strong> {self._render_inline(children)}</div>'
            case Reference(cref=cref):
                safe_id = cref.replace(":", "-").replace(".", "-")
                text = cref.split(":", 1)[-1]

                return (
                    f'<a href="#{escape(safe_id, quote=True)}">'
                    f'{escape(text)}</a>'
                )
            case _:
                raise TypeError(f"Unsupported node type: {type(node)!r}")


    def _render_inline(self, nodes: list[Node]) -> str:
        parts: list[str] = []
        for node in nodes:
            rendered = self._render_node(node)
            if isinstance(node, LineBreak):
                parts.append(rendered)
            elif rendered in {".", ",", ";", ":", "!", "?"}:
                parts.append(rendered)
            elif parts and not parts[-1].endswith((" ", "<br>")):
                parts.append(" " + rendered)
            else:
                parts.append(rendered)
        return "".join(parts)

    def _render_toc(self, document: Document) -> str:
        links: list[str] = []

        for node in document.children:
            if isinstance(node, Member):
                safe_id = node.name.replace(":", "-").replace(".", "-")

                links.append(
                    f'<li><a href="#{escape(safe_id, quote=True)}">'
                    f'{escape(node.name)}</a></li>'
                )

        if not links:
            return ""

        items = "\n".join(links)

        return (
            '<nav class="toc">\n'
            '<h2>Table of Contents</h2>\n'
            '<ul>\n'
            f'{items}\n'
            '</ul>\n'
            '</nav>'
        )
