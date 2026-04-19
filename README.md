# Simple SimpleStreams

A simple client for LXD SimpleStreams, port of lxc/lxd/shared/simplesreams.go

🚧 Under Development 🚧 \
Only a few APIs are implemented

## Usage

```python
from simplesimplestreams import SimpleStreamsClient

client = SimpleStreamsClient(url="https://images.linuxcontainers.org")
images = client.list_images()
```

See [API docs](https://otariidae.github.io/simplesimplestreams/) for more infomation.

## Development

Supported Python versions: 3.10-3.14

Sync dependencies with poetry: `poetry sync` \
Run type check: `poetry run mypy . --strict` \
Run tests: `poetry run pytest` \
Format code: `poetry run black .`

## Publishing

PyPI releases are published by `.github/workflows/python-publish.yml` using PyPI trusted publishing.
After registering this repository, workflow file, and the `pypi` GitHub Actions environment as a trusted publisher on PyPI, push a version tag such as `0.1.2`.

## License

Apache-2.0
