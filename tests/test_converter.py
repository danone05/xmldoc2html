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

def test_converts_csharp_xml_doc_member():
    html = convert("""
    <doc>
      <members>
        <member name="T:Demo.Calculator">
          <summary>Calculator class.</summary>
          <param name="value">Input value.</param>
          <returns>Result value.</returns>
        </member>
      </members>
    </doc>
    """)

    assert "<title>C# Documentation</title>" in html
    assert 'id="T-Demo-Calculator"' in html
    assert "T:Demo.Calculator" in html
    assert "Summary:" in html
    assert "Calculator class." in html
    assert "value:" in html
    assert "Input value." in html
    assert "Returns:" in html
    assert "Result value." in html

def test_generates_table_of_contents():
    html = convert("""
    <doc>
      <members>
        <member name="T:Demo.Calculator">
          <summary>Calculator class.</summary>
        </member>
      </members>
    </doc>
    """)

    assert "Table of Contents" in html
    assert 'href="#T-Demo-Calculator"' in html

def test_converts_cref_links():
    html = convert("""
    <doc>
      <members>
        <member name="T:Demo.Calculator">
          <summary>
            Uses <see cref="T:Demo.Math"/>.
          </summary>
        </member>
      </members>
    </doc>
    """)

    assert 'href="#T-Demo-Math"' in html
    assert "Demo.Math" in html

def test_highlights_code_keywords():
    html = convert("""
    <document>
      <p><code>public class Test</code></p>
    </document>
    """)

    assert '<span class="kw">public</span>' in html
    assert '<span class="kw">class</span>' in html
from xmldoc2html.project_scanner import ProjectScanner


def test_finds_documentation_file_from_csproj(tmp_path):
    csproj = tmp_path / "Demo.csproj"
    xml_doc = tmp_path / "bin" / "Debug" / "Demo.xml"

    csproj.write_text(
        """
        <Project>
          <PropertyGroup>
            <DocumentationFile>bin/Debug/Demo.xml</DocumentationFile>
          </PropertyGroup>
        </Project>
        """,
        encoding="utf-8",
    )

    result = ProjectScanner().find_xml_files(csproj)

    assert result == [xml_doc]

def test_finds_xml_files_from_sln(tmp_path):
    project_dir = tmp_path / "Demo"
    project_dir.mkdir()

    csproj = project_dir / "Demo.csproj"

    csproj.write_text(
        """
        <Project>
          <PropertyGroup>
            <DocumentationFile>bin/Debug/Demo.xml</DocumentationFile>
          </PropertyGroup>
        </Project>
        """,
        encoding="utf-8",
    )

    sln = tmp_path / "Demo.sln"

    sln.write_text(
        """
        Project("{GUID}") = "Demo", "Demo/Demo.csproj", "{GUID}"
        """,
        encoding="utf-8",
    )

    result = ProjectScanner().find_xml_files(sln)

    expected = [
        project_dir / "bin" / "Debug" / "Demo.xml"
    ]

    assert result == expected