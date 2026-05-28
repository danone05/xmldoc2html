from html import escape

from xmldoc2html.model import (
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
)
'''Превращает внутреннюю модель документа в готовый html код'''

class HtmlRenderer:
    def render(self, document: Document) -> str:
        title = escape(document.title or "Document")
        body_parts: list[str] = []

        if document.title:
            body_parts.append(f"<h1>{escape(document.title)}</h1>")

        body_parts.extend(self._render_node(node) for node in document.children)
        body = "\n".join(body_parts)

        return (
            "<!doctype html>\n"
            "<html lang=\"en\">\n"
            "<head>\n"
            "  <meta charset=\"utf-8\">\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            f"  <title>{title}</title>\n"
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
                return f"<code>{self._render_inline(children)}</code>"
            case LineBreak():
                return "<br>"
            case Link(href=href, children=children):
                return f"<a href=\"{escape(href, quote=True)}\">{self._render_inline(children)}</a>"
            case _:
                raise TypeError(f"Unsupported node type: {type(node)!r}")

    def _render_inline(self, nodes: list[Node]) -> str:
        parts: list[str] = []
        for node in nodes:
            rendered = self._render_node(node)
            if isinstance(node, LineBreak):
                parts.append(rendered)
            elif parts and not parts[-1].endswith((" ", "<br>")):
                parts.append(" " + rendered)
            else:
                parts.append(rendered)
        return "".join(parts)
