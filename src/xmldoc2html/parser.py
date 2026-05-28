from pathlib import Path
from xml.etree import ElementTree as ET

'''Чтение xml'''

class XmlParser:
    def parse_file(self, path: str | Path) -> ET.Element:
        try:
            tree = ET.parse(path)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML: {exc}") from exc
        return tree.getroot()

    def parse_string(self, xml: str) -> ET.Element:
        try:
            return ET.fromstring(xml)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML: {exc}") from exc
