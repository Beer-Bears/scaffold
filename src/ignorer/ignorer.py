from pathlib import Path
from pathspec import PathSpec

from pathlib import Path
from pathspec import PathSpec


def _locate_ignore_files(starting_path: Path, project_root: Path) -> list[Path]:
    ignore_files = []
    current_path = starting_path
    while current_path.is_dir() and current_path != project_root.parent:
        ignore_file = current_path / ".scaffoldignore"
        if ignore_file.exists():
            ignore_files.append(ignore_file)
        if current_path == project_root:
            break
        current_path = current_path.parent
    return ignore_files


class Ignorer:
    ignore_files: list[Path]

    def __init__(self, starting_path: Path, project_root: Path):
        self.ignore_files = _locate_ignore_files(starting_path, project_root)
        self.lines = self._load_ignore_files()
        self.spec = self._parse_ignore_rules()

    def _load_ignore_files(self) -> list[str]:
        all_lines = []
        for ignore_file in self.ignore_files:
            all_lines.extend(ignore_file.read_text().splitlines())
        return all_lines

    def _parse_ignore_rules(self) -> PathSpec:
        cleaned = [
            line.strip()
            for line in self.lines
            if line.strip() and not line.strip().startswith("#")
        ]
        return PathSpec.from_lines("gitwildmatch", cleaned)

    def is_ignore(self, path: Path | str) -> bool:
        return self.spec.match_file(str(path))