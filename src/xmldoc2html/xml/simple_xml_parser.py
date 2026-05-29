import re
from html import unescape
from xmldoc2html.xml.xml_node import XmlNode
from xmldoc2html.xml.xml_tokenizer import XmlTokenizer


ATTR_REGEX = re.compile(r'(\w+)="([^"]*)"')


class SimpleXmlParser:
    def parse(self, xml: str) -> XmlNode:
        tokens = XmlTokenizer().tokenize(xml)
        stack: list[XmlNode] = []
        root = None
        last_closed: XmlNode | None = None

        for token in tokens:
            if token.startswith("</"):
                closing_tag = token[2:-1].strip()
                if not stack:
                    raise ValueError("Invalid XML")
                node = stack.pop()
                if node.tag != closing_tag:
                    raise ValueError("Invalid XML")
                last_closed = node

            elif token.startswith("<"):
                self_closing = token.endswith("/>")
                content = token[1:-1].strip()

                if content.endswith("/"):
                    content = content[:-1].strip()
                parts = content.split(maxsplit=1)
                tag = parts[0]
                attrs = {}

                if len(parts) > 1:

                    for key, value in ATTR_REGEX.findall(parts[1]):
                        attrs[key] = unescape(value)
                node = XmlNode(tag=tag, attrs=attrs)

                if stack:
                    stack[-1].children.append(node)

                else:
                    root = node

                if self_closing:
                    last_closed = node

                else:
                    stack.append(node)
                    last_closed = None

            else:
                text = unescape(token.strip())

                if not text:
                    continue

                if last_closed is not None:
                    last_closed.tail += text
                    last_closed = None

                elif stack:
                    stack[-1].text += text

        if root is None:
            raise ValueError("Invalid XML")

        if stack:
            raise ValueError("Invalid XML")

        return root
