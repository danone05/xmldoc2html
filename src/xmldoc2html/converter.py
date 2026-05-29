from pathlib import Path
from xmldoc2html.input.project_scanner import ProjectScanner
from xmldoc2html.mapping.mapper import XmlToDocumentMapper
from xmldoc2html.xml.parser import XmlParser
from xmldoc2html.rendering.renderer import HtmlRenderer

'''Соединение parser, mapper и renderer в один pipeline'''

class XmlDoc2HtmlConverter:
    def __init__(self, *, strict: bool = False):
        self.parser = XmlParser()
        self.mapper = XmlToDocumentMapper(strict=strict)
        self.renderer = HtmlRenderer()
        self.scanner = ProjectScanner()

    def convert_string(self, xml: str) -> str:
        root = self.parser.parse_string(xml)
        document = self.mapper.map_root(root)
        return self.renderer.render(document)

    def convert_file(self, input_path: str | Path, output_path: str | Path) -> None:
        xml_files = self.scanner.find_xml_files(input_path)

        html_parts: list[str] = []

        for xml_file in xml_files:
            root = self.parser.parse_file(xml_file)
            document = self.mapper.map_root(root)
            html_parts.append(self.renderer.render(document))

        html = "\n".join(html_parts)
        Path(output_path).write_text(html, encoding="utf-8")