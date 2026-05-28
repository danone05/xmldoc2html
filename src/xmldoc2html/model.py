from dataclasses import dataclass, field
from typing import Literal

'''Описание элементов документа как объектов'''
@dataclass(frozen=True)
class Node:
    pass


@dataclass(frozen=True)
class TextNode(Node):
    text: str


@dataclass(frozen=True)
class Paragraph(Node):
    children: list[Node] = field(default_factory=list)


@dataclass(frozen=True)
class Heading(Node):
    level: int
    children: list[Node] = field(default_factory=list)


@dataclass(frozen=True)
class Section(Node):
    children: list[Node] = field(default_factory=list)


@dataclass(frozen=True)
class ListBlock(Node):
    kind: Literal["ul", "ol"]
    items: list[list[Node]] = field(default_factory=list)


@dataclass(frozen=True)
class Link(Node):
    href: str
    children: list[Node] = field(default_factory=list)


@dataclass(frozen=True)
class Bold(Node):
    children: list[Node] = field(default_factory=list)


@dataclass(frozen=True)
class Italic(Node):
    children: list[Node] = field(default_factory=list)


@dataclass(frozen=True)
class Code(Node):
    children: list[Node] = field(default_factory=list)


@dataclass(frozen=True)
class LineBreak(Node):
    pass


@dataclass(frozen=True)
class Document:
    title: str | None = None
    children: list[Node] = field(default_factory=list)

@dataclass(frozen=True)
class Image(Node):
    src: str
    alt: str = ""

@dataclass(frozen=True)
class Member(Node):
    name: str
    children: list[Node]

@dataclass(frozen=True)
class Summary(Node):
    children: list[Node]

@dataclass(frozen=True)
class Returns(Node):
    children: list[Node] = field(default_factory=list)

@dataclass(frozen=True)
class Param(Node):
    name: str
    children: list[Node] = field(default_factory=list)

@dataclass(frozen=True)
class Reference(Node):
    cref: str
