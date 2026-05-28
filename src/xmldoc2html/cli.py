import argparse

from xmldoc2html.converter import XmlDoc2HtmlConverter

'''Точка входа'''

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="xmldoc2html")
    parser.add_argument("input", help="Input XML file")
    parser.add_argument("-o", "--output", required=True, help="Output HTML file")
    parser.add_argument("--strict", action="store_true", help="Fail on unsupported tags")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    converter = XmlDoc2HtmlConverter(strict=args.strict)
    converter.convert_file(args.input, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
