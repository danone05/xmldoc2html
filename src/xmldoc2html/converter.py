from pathlib import Path

from xmldoc2html.mapper import XmlToDocumentMapper
from xmldoc2html.parser import XmlParser
from xmldoc2html.renderer import HtmlRenderer

'''Соединение parser, mapper и renderer в один pipeline'''

class XmlDoc2HtmlConverter:
    def __init__(self, *, strict: bool = False):
        self.parser = XmlParser()
        self.mapper = XmlToDocumentMapper(strict=strict)
        self.renderer = HtmlRenderer()

    def convert_string(self, xml: str) -> str:
        root = self.parser.parse_string(xml)
        document = self.mapper.map_root(root)
        return self.renderer.render(document)

    def convert_file(self, input_path: str | Path, output_path: str | Path) -> None:
        root = self.parser.parse_file(input_path)
        document = self.mapper.map_root(root)
        html = self.renderer.render(document)
        Path(output_path).write_text(html, encoding="utf-8")
