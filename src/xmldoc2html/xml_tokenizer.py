import re


TOKEN_REGEX = re.compile(r"(<[^>]+>|[^<]+)")


class XmlTokenizer:
    def tokenize(self, xml: str) -> list[str]:
        tokens = TOKEN_REGEX.findall(xml)
        return [token.strip() for token in tokens if token.strip()]

