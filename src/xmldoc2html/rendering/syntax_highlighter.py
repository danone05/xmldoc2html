import re

KEYWORDS = {
    "public",
    "private",
    "class",
    "void",
    "string",
    "int",
    "return",
    "static",
}


class SyntaxHighlighter:
    def highlight(self, code: str) -> str:
        parts = []

        for token in re.split(r"(\W+)", code):
            if token in KEYWORDS:
                parts.append(f'<span class="kw">{token}</span>')
            else:
                parts.append(token)

        return "".join(parts)