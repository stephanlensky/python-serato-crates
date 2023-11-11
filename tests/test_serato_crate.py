from pathlib import Path

from serato_crate.serato_crate import SeratoCrate

TEST_CRATE_FILE = Path("test.crate")


def test_serato_crate_can_be_written_and_read_back():
    tracks = [
        Path("Some/Path/Relative/To/Root/Drive/song_1.ogg"),
        Path("Some/Path/Relative/To/Root/Drive/song_2.ogg"),
    ]
    crate = SeratoCrate()
    crate.tracks = list(tracks)
    crate.write(TEST_CRATE_FILE)

    loaded_crate = SeratoCrate.load(TEST_CRATE_FILE)
    assert loaded_crate.tracks == tracks

    TEST_CRATE_FILE.unlink()
