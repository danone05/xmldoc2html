from pathlib import Path
import re


DOCUMENTATION_FILE_REGEX = re.compile(
    r"<DocumentationFile>(.*?)</DocumentationFile>",
    re.IGNORECASE | re.DOTALL,
)
SLN_PROJECT_REGEX = re.compile(
    r'Project\(.*?\)\s*=\s*".*?",\s*"(.*?\.csproj)"',
    re.IGNORECASE,
)


class ProjectScanner:
    def find_xml_files(self, input_path: str | Path) -> list[Path]:
        path = Path(input_path)

        if path.suffix.lower() == ".xml":
            return [path]

        if path.suffix.lower() == ".csproj":
            return self._find_from_csproj(path)
        if path.suffix.lower() == ".sln":
            return self._find_from_sln(path)

        raise ValueError("Input must be .xml or .csproj file")

    def _find_from_csproj(self, csproj_path: Path) -> list[Path]:
        content = csproj_path.read_text(encoding="utf-8")

        matches = DOCUMENTATION_FILE_REGEX.findall(content)
        result: list[Path] = []

        for match in matches:
            xml_path = Path(match.strip())

            if not xml_path.is_absolute():
                xml_path = csproj_path.parent / xml_path

            result.append(xml_path)

        if not result:
            raise ValueError("No DocumentationFile found in .csproj")

        return result

    def _find_from_sln(self, sln_path: Path) -> list[Path]:
        content = sln_path.read_text(encoding="utf-8")

        matches = SLN_PROJECT_REGEX.findall(content)

        xml_files: list[Path] = []

        for match in matches:
            csproj_path = sln_path.parent / match

            xml_files.extend(self._find_from_csproj(csproj_path))

        return xml_files