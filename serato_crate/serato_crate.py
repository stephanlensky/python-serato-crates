from __future__ import annotations

from pathlib import Path
from typing import Any

from serato_crate.crate_file import read_crate_file, write_crate_file


class SeratoCrate:
    """
    Class representing a Serato Scratch Live (a.k.a. Serato DJ) crate file.

    Tracks in the crate are exposed with the `tracks` attribute as a list of relative `Paths`.

    Note, track paths must be specified relative to the root of the drive the crate is
    located on. For crates with tracks on multiple drives, multiple crate files should be
    used. Crates on different drives with the same name are merged by Serato DJ.
    """

    def __init__(self, crate_data: list[tuple[str, Any]] | None = None) -> None:
        """
        Create a new SeratoCrate instance.

        :param crate_data: Decoded crate data to initialize the crate with. If not specified, a new
            crate will be created with no tracks.
        """
        crate_data = crate_data or []
        self.tracks: list[Path] = [
            Path(next(item[1] for item in record[1] if item[0] == "ptrk"))
            for record in crate_data
            if record[0] == "otrk"
        ]

    @property
    def crate_data(self) -> list[tuple[str, Any]]:
        """
        Return this crate in the Serato database format, ready to be encoded into a .crate file.

        Called internally by `write()` when saving the crate to disk.

        :return: Crate data in the Serato database format.
        """
        return [
            ("vrsn", "1.0/Serato ScratchLive Crate"),
            *[("otrk", [("ptrk", str(track))]) for track in self.tracks],
        ]

    @classmethod
    def load(cls, path: Path) -> SeratoCrate:
        """
        Load a SeratoCrate from a .crate file.

        :param path: Path to the .crate file to load.
        :return: SeratoCrate instance loaded from the .crate file.
        """
        crate_data = read_crate_file(path)
        return SeratoCrate(crate_data)

    def write(self, path: Path) -> None:
        """
        Write this crate to a .crate file.

        :param path: Path to the .crate file to write.
        """
        write_crate_file(path, self.crate_data)
