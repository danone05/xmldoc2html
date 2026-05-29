from pathlib import Path

from xmldoc2html.xml.simple_xml_parser import SimpleXmlParser
from xmldoc2html.xml.xml_node import XmlNode


class XmlParser:
    def parse_file(self, path: str | Path) -> XmlNode:
        xml = Path(path).read_text(encoding="utf-8")
        return self.parse_string(xml)

    def parse_string(self, xml: str) -> XmlNode:
        try:
            return SimpleXmlParser().parse(xml)
        except Exception as exc:
            raise ValueError(f"Invalid XML: {exc}") from exc