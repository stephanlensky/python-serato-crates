from __future__ import annotations

from pathlib import Path
from typing import Any

from serato_crate.crate_file import read_crate_file, write_crate_file


class SeratoCrate:
    def __init__(self, crate_data: list[tuple[str, Any]] | None = None) -> None:
        crate_data = crate_data or []
        self.tracks: list[Path] = [
            Path(next(item[1] for item in record[1] if item[0] == "ptrk"))
            for record in crate_data
            if record[0] == "otrk"
        ]

    @property
    def crate_data(self) -> list[tuple[str, Any]]:
        return [
            ("vrsn", "1.0/Serato ScratchLive Crate"),
            *[("otrk", [("ptrk", str(track))]) for track in self.tracks],
        ]

    @classmethod
    def load(cls, path: Path) -> SeratoCrate:
        crate_data = read_crate_file(path)
        return SeratoCrate(crate_data)

    def write(self, path: Path) -> None:
        write_crate_file(path, self.crate_data)
