'''Кастомные ошибки'''
class XmlDoc2HtmlError(Exception):
    """Base application error."""


class UnsupportedTagError(XmlDoc2HtmlError):
    """Raised when XML contains an unsupported tag in strict mode."""
