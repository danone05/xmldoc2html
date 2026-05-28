from xmldoc2html.xml_node import XmlNode

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
    Image,
    Member,
    Summary,
    Param,
    Returns,
    Reference
)


"""превращает xml теги во внутренние объекты документа"""


class XmlToDocumentMapper:
    def __init__(self, *, strict: bool = False):
        self.strict = strict

    def map_root(self, root: XmlNode) -> Document:
        if root.tag == "document":
            return self._map_document(root)

        if root.tag == "doc":
            return self._map_csharp_doc(root)

        raise ValueError("Root tag must be <document> or <doc>")

    def _map_document(self, root: XmlNode) -> Document:
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

    def _map_csharp_doc(self, root: XmlNode) -> Document:
        children: list[Node] = []

        for child in root:
            if child.tag == "members":
                for member_node in child:
                    if member_node.tag == "member":
                        member = self._map_member(member_node)
                        if member is not None:
                            children.append(member)

        return Document(title="C# Documentation", children=children)

    def _map_member(self, element: XmlNode) -> Member | None:
        name = element.attrs.get("name")
        if not name:
            self._handle_unsupported(element)
            return None

        children: list[Node] = []

        for child in element:
            match child.tag:
                case "summary":
                    children.append(Summary(children=self._inline_children(child)))

                case "param":
                    param_name = child.attrs.get("name", "")
                    children.append(
                        Param(
                            name=param_name,
                            children=self._inline_children(child),
                        )
                    )

                case "returns":
                    children.append(Returns(children=self._inline_children(child)))

                case _:
                    mapped = self._map_block(child, heading_level=3)
                    if mapped is not None:
                        children.append(mapped)

        return Member(name=name, children=children)

    def _map_block(self, element: XmlNode, *, heading_level: int) -> Node | None:
        match element.tag:
            case "section":
                nodes: list[Node] = []

                for child in element:
                    if child.tag == "title":
                        nodes.append(
                            Heading(
                                level=heading_level,
                                children=self._inline_children(child),
                            )
                        )
                    else:
                        mapped = self._map_block(
                            child,
                            heading_level=min(heading_level + 1, 6),
                        )
                        if mapped is not None:
                            nodes.append(mapped)

                return Section(children=nodes)

            case "title":
                return Heading(
                    level=heading_level,
                    children=self._inline_children(element),
                )

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

            case "img":
                src = element.attrs.get("src")
                if not src:
                    self._handle_unsupported(element)
                    return None

                alt = element.attrs.get("alt", "")
                return Image(src=src, alt=alt)

            case _:
                self._handle_unsupported(element)
                return None

    def _inline_children(self, element: XmlNode) -> list[Node]:
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
                    href = child.attrs.get("href", "#")
                    result.append(
                        Link(
                            href=href,
                            children=self._inline_children(child),
                        )
                    )

                case "img":
                    src = child.attrs.get("src")
                    if not src:
                        self._handle_unsupported(child)
                    else:
                        alt = child.attrs.get("alt", "")
                        result.append(Image(src=src, alt=alt))
                case "see":
                    cref = child.attrs.get("cref")

                    if cref:
                        result.append(Reference(cref=cref))

                case _:
                    self._handle_unsupported(child)

        return result

    def _append_text(self, nodes: list[Node], text: str | None) -> None:
        if text is None:
            return

        normalized = " ".join(text.split())

        if normalized:
            nodes.append(TextNode(normalized))

    def _text_content(self, element: XmlNode) -> str:
        parts = [element.text]

        for child in element.children:
            parts.append(self._text_content(child))

        return " ".join("".join(parts).split())

    def _handle_unsupported(self, element: XmlNode) -> None:
        if self.strict:
            raise UnsupportedTagError(f"Unsupported tag: <{element.tag}>")