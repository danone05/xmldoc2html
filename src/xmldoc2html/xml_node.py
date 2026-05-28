from dataclasses import dataclass, field

@dataclass
class XmlNode:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    children: list["XmlNode"] = field(default_factory=list)
    text: str = ""

    def __iter__(self):
        return iter(self.children)
