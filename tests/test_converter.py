import pytest

from xmldoc2html.converter import XmlDoc2HtmlConverter
from xmldoc2html.exceptions import UnsupportedTagError


def convert(xml: str) -> str:
    return XmlDoc2HtmlConverter().convert_string(xml)


def test_converts_title_and_paragraph():
    html = convert("""
    <document>
      <title>My Doc</title>
      <p>Hello world</p>
    </document>
    """)

    assert "<title>My Doc</title>" in html
    assert "<h1>My Doc</h1>" in html
    assert "<p>Hello world</p>" in html


def test_converts_section_title_to_h2():
    html = convert("""
    <document>
      <title>My Doc</title>
      <section>
        <title>Intro</title>
        <p>Hello</p>
      </section>
    </document>
    """)

    assert "<section>" in html
    assert "<h2>Intro</h2>" in html
    assert "<p>Hello</p>" in html


def test_converts_nested_sections_to_deeper_headings():
    html = convert("""
    <document>
      <section>
        <title>Level 2</title>
        <section>
          <title>Level 3</title>
        </section>
      </section>
    </document>
    """)

    assert "<h2>Level 2</h2>" in html
    assert "<h3>Level 3</h3>" in html


def test_converts_inline_formatting_links_code_and_br():
    html = convert("""
    <document>
      <p>Hello <b>bold</b> and <i>italic</i> and <code>x = 1</code><br/><a href="https://example.com">link</a></p>
    </document>
    """)

    assert "<strong>bold</strong>" in html
    assert "<em>italic</em>" in html
    assert "<code>x = 1</code>" in html
    assert "<br>" in html
    assert '<a href="https://example.com">link</a>' in html


def test_converts_lists():
    html = convert("""
    <document>
      <ul>
        <li>One</li>
        <li>Two</li>
      </ul>
    </document>
    """)

    assert "<ul>" in html
    assert "<li>One</li>" in html
    assert "<li>Two</li>" in html


def test_escapes_html_text_and_attributes():
    html = convert("""
    <document>
      <p>5 &lt; 10 and <a href="https://example.com?a=1&amp;b=2">safe</a></p>
    </document>
    """)

    assert "5 &lt; 10" in html
    assert 'href="https://example.com?a=1&amp;b=2"' in html


def test_requires_document_root():
    with pytest.raises(ValueError, match="Root tag must be"):
        convert("<root><p>Hello</p></root>")


def test_invalid_xml_raises_value_error():
    with pytest.raises(ValueError, match="Invalid XML"):
        convert("<document><p>broken</document>")


def test_unknown_tags_are_ignored_by_default():
    html = convert("""
    <document>
      <unknown>Hello</unknown>
      <p>Known</p>
    </document>
    """)

    assert "Known" in html
    assert "Hello" not in html


def test_strict_mode_fails_on_unsupported_tags():
    xml = """
    <document>
      <unknown>Hello</unknown>
    </document>
    """

    with pytest.raises(UnsupportedTagError):
        XmlDoc2HtmlConverter(strict=True).convert_string(xml)
        
def test_converts_images():
    html = convert("""
    <document>
      <img src="images/logo.png" alt="Logo"/>
    </document>
    """)

    assert '<img src="images/logo.png" alt="Logo">' in html