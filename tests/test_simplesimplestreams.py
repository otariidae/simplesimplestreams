from importlib import import_module
import sys
from pathlib import Path

import pytest
import requests
import responses
from responses import matchers
from simplesimplestreams import Products, SimpleStreamsClient, Stream, __version__

tomllib = import_module("tomllib" if sys.version_info >= (3, 11) else "tomli")


SAMPLE_STREAM: Stream = {
    "format": "index:1.0",
    "updated": "2026-04-20T00:00:00Z",
    "index": {
        "images": {
            "datatype": "image-downloads",
            "path": "streams/v1/images.json",
            "updated": None,
            "products": ["ubuntu:noble:amd64"],
            "format": "products:1.0",
        },
        "empty-images": {
            "datatype": "image-downloads",
            "path": "streams/v1/empty.json",
            "updated": None,
            "products": [],
            "format": "products:1.0",
        },
        "non-images": {
            "datatype": "other",
            "path": "streams/v1/other.json",
            "updated": None,
            "products": ["ignored"],
            "format": "products:1.0",
        },
    },
}

SAMPLE_PRODUCTS: Products = {
    "content_id": "images",
    "datatype": "image-downloads",
    "format": "products:1.0",
    "license": None,
    "updated": "2026-04-20T00:00:00Z",
    "products": {
        "ubuntu:noble:amd64": {
            "aliases": "24.04,noble",
            "arch": "amd64",
            "os": "ubuntu",
            "release": "24.04",
            "release_codename": "noble",
            "release_title": "Ubuntu 24.04 LTS",
            "supported": True,
            "supported_eol": None,
            "version": "20260420",
            "versions": {},
        }
    },
}


def test_version() -> None:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    with pyproject.open("rb") as f:
        project = tomllib.load(f)

    assert __version__ == project["project"]["version"]


@responses.activate
def test_get_stream_uses_index_endpoint() -> None:
    responses.get(
        "https://example.test/streams/v1/index.json",
        json=SAMPLE_STREAM,
        status=200,
        match=[matchers.request_kwargs_matcher({"timeout": 30})],
    )

    client = SimpleStreamsClient(url="https://example.test/")
    stream = client.get_stream()

    assert stream == SAMPLE_STREAM
    assert len(responses.calls) == 1
    assert (
        responses.calls[0].request.url == "https://example.test/streams/v1/index.json"
    )


@responses.activate
def test_list_images_filters_non_image_entries() -> None:
    responses.get(
        "https://example.test/streams/v1/index.json",
        json=SAMPLE_STREAM,
        status=200,
        match=[matchers.request_kwargs_matcher({"timeout": 30})],
    )
    responses.get(
        "https://example.test/streams/v1/images.json",
        json=SAMPLE_PRODUCTS,
        status=200,
        match=[matchers.request_kwargs_matcher({"timeout": 30})],
    )

    client = SimpleStreamsClient(url="https://example.test")
    images = client.list_images()

    assert [call.request.url for call in responses.calls] == [
        "https://example.test/streams/v1/index.json",
        "https://example.test/streams/v1/images.json",
    ]
    assert images == list(SAMPLE_PRODUCTS["products"].values())

    image = images[0]
    for field in ("aliases", "arch", "release", "release_title"):
        assert isinstance(image[field], str)


@responses.activate
def test_get_products_uses_relative_path_with_timeout() -> None:
    payload: Products = {
        "content_id": "images",
        "datatype": "image-downloads",
        "format": "products:1.0",
        "license": None,
        "products": {},
        "updated": None,
    }
    responses.get(
        "https://example.test/streams/v1/images.json",
        json=payload,
        status=200,
        match=[matchers.request_kwargs_matcher({"timeout": 30})],
    )

    client = SimpleStreamsClient(url="https://example.test")

    assert client.get_products("streams/v1/images.json") == payload
    assert len(responses.calls) == 1
    assert (
        responses.calls[0].request.url == "https://example.test/streams/v1/images.json"
    )


@responses.activate
def test_get_stream_raises_for_http_errors() -> None:
    responses.get(
        "https://example.test/streams/v1/index.json",
        status=503,
        match=[matchers.request_kwargs_matcher({"timeout": 30})],
    )

    client = SimpleStreamsClient(url="https://example.test")

    with pytest.raises(requests.HTTPError):
        client.get_stream()
