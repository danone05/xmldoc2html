# xmldoc2html
A simple Python command-line tool to convert structured XML documents into clean HTML5. It parses a specific XML schema and renders it as a standard HTML page.

## Features

*   Converts XML to a complete HTML5 document structure.
*   Supports nested `<section>` elements with automatic heading level management (`<h1>`, `<h2>`, `<h3>`, etc.).
*   Handles common formatting tags: paragraphs (`<p>`), bold (`<b>`), italic (`<i>`), links (`<a>`), images (`<img>`), inline code (`<code>`), and line breaks (`<br>`).
*   Generates unordered (`<ul>`) and ordered (`<ol>`) lists.
*   Includes a `--strict` mode option to fail on unsupported XML tags, ensuring document validity.
*   Provides a simple and intuitive command-line interface.

## Installation

To install the necessary dependencies and the command-line tool, clone the repository and run pip from the root directory:

```bash
git clone https://github.com/danone05/xmldoc2html.git
cd xmldoc2html
pip install .
```

## Usage

The tool is operated via the command line. You must provide an input XML file and specify an output path for the generated HTML.

### Basic Conversion

To convert an XML file, use the following command:

```bash
xmldoc2html input.xml -o output.html
```

### Strict Mode

By default, the converter ignores any XML tags it does not recognize. To enforce a strict conversion where any unsupported tag will raise an error, use the `--strict` flag:

```bash
xmldoc2html input.xml -o output.html --strict
```

## Supported XML Format

The converter expects a specific XML structure for successful conversion. The root element must be `<document>`.

### Supported Tags

*   **`<document>`**: The root element for the entire document.
*   **`<title>`**: Defines the document title (becomes `<h1>` and `<title>` in HTML).
*   **`<section>`**: A content section. Sections can be nested, and their titles will be rendered with progressively deeper heading levels (`<h2>`, `<h3>`, etc.).
*   **`<p>`**: A paragraph.
*   **`<ul>` / `<ol>`**: Unordered or ordered lists.
*   **`<li>`**: A list item.
*   **`<a>`**: A hyperlink with an `href` attribute.
*   **`<b>` / `<strong>`**: Bold text.
*   **`<i>` / `<em>`**: Italic text.
*   **`<code>`**: Inline code.
*   **`<br>`**: A line break.
*   **`<img>`**: An image, with `src` and `alt` attributes.

### Example Input (`input.xml`)

```xml
<document>
    <title>XML to HTML Demo</title>

    <section>
        <title>Introduction</title>

        <p>
            This is a simple <b>XML</b> document converted to
            <i>HTML</i>.
        </p>

        <p>
            Visit
            <a href="https://example.com">
                Example Website
            </a>
        </p>
    </section>

    <section>
        <title>Features</title>

        <ul>
            <li>Paragraph support</li>
            <li>Bold and italic text</li>
            <li>Links</li>
            <li>Lists</li>
            <li>sections</li>
        </ul>

        <section>
            <title>Example</title>
            <p>
                Example inline code:
                <code>print(&quot;Hello World&quot;)</code>
            </p>
            <p>
                First line<br/>
                Second line
            </p>
        </section>
        <section>
            <title>Image Example</title>
            <p>Here is an image:</p>
            <img src="images/logo.png" alt="Project logo"/>
        </section>
    </section>
</document>