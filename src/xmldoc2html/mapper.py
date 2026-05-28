from xml.etree.ElementTree import Element

from xmldoc2html.exceptions import UnsupportedTagError
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

'''превращает xml теги во внутренние объекты документа'''

class XmlToDocumentMapper:
    def __init__(self, *, strict: bool = False):
        self.strict = strict

    def map_root(self, root: Element) -> Document:
        if root.tag != "document":
            raise ValueError("Root tag must be <document>")

        title = None
        children: list[Node] = []

        for child in root:
            if child.tag == "title" and title is None:
                title = self._text_content(child)
                continue

            mapped = self._map_block(child, heading_level=2)
            if mapped is not None:
                children.append(mapped)

        return Document(title=title, children=children)

    def _map_block(self, element: Element, *, heading_level: int) -> Node | None:
        match element.tag:
            case "section":
                nodes: list[Node] = []
                for child in element:
                    if child.tag == "title":
                        nodes.append(Heading(level=heading_level, children=self._inline_children(child)))
                    else:
                        mapped = self._map_block(child, heading_level=min(heading_level + 1, 6))
                        if mapped is not None:
                            nodes.append(mapped)
                return Section(children=nodes)

            case "title":
                return Heading(level=heading_level, children=self._inline_children(element))

            case "p":
                return Paragraph(children=self._inline_children(element))

            case "ul" | "ol":
                items: list[list[Node]] = []
                for li in element:
                    if li.tag != "li":
                        self._handle_unsupported(li)
                        continue
                    items.append(self._inline_children(li))
                return ListBlock(kind=element.tag, items=items)

            case _:
                self._handle_unsupported(element)
                return None

    def _inline_children(self, element: Element) -> list[Node]:
        result: list[Node] = []
        self._append_text(result, element.text)

        for child in element:
            match child.tag:
                case "b" | "strong":
                    result.append(Bold(children=self._inline_children(child)))
                case "i" | "em":
                    result.append(Italic(children=self._inline_children(child)))
                case "code":
                    result.append(Code(children=self._inline_children(child)))
                case "br":
                    result.append(LineBreak())
                case "a":
                    href = child.attrib.get("href", "#")
                    result.append(Link(href=href, children=self._inline_children(child)))
                case _:
                    self._handle_unsupported(child)

            self._append_text(result, child.tail)

        return result

    def _append_text(self, nodes: list[Node], text: str | None) -> None:
        if text is None:
            return
        normalized = " ".join(text.split())
        if normalized:
            nodes.append(TextNode(normalized))

    def _text_content(self, element: Element) -> str:
        return " ".join("".join(element.itertext()).split())

    def _handle_unsupported(self, element: Element) -> None:
        if self.strict:
            raise UnsupportedTagError(f"Unsupported tag: <{element.tag}>")
