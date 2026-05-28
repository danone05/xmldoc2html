from xmldoc2html.cli import main


def test_cli_writes_output_file(tmp_path):
    input_file = tmp_path / "input.xml"
    output_file = tmp_path / "output.html"

    input_file.write_text(
        """
        <document>
          <title>CLI Doc</title>
          <p>Hello from CLI</p>
        </document>
        """,
        encoding="utf-8",
    )

    exit_code = main([str(input_file), "-o", str(output_file)])

    assert exit_code == 0
    html = output_file.read_text(encoding="utf-8")
    assert "<h1>CLI Doc</h1>" in html
    assert "<p>Hello from CLI</p>" in html
