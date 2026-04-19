from pathlib import Path

import pytest
import tomli
from simplesimplestreams import __version__, SimpleStreamsClient, Product


def test_version() -> None:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    with pyproject.open("rb") as f:
        project = tomli.load(f)

    assert __version__ == project["tool"]["poetry"]["version"]


@pytest.mark.parametrize(
    "server_url",
    ["https://images.linuxcontainers.org", "https://cloud-images.ubuntu.com/releases"],
)
def test_simplestreamsclient(server_url: str) -> None:
    ss = SimpleStreamsClient(url=server_url)
    images = ss.list_images()
    assert type(images) is list
    for image in images:
        assert "aliases" in image and type(image["aliases"]) is str
        assert "arch" in image and type(image["arch"]) is str
        assert "release" in image and type(image["release"]) is str
        assert "release_title" in image and type(image["release_title"]) is str
