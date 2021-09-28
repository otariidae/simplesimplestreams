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

## Development

Install dependencies with poetry: `poetry install` \
Run type check: `poetry run mypy . --strict` \
Run tests: `poetry run pytest` \
Format code: `poetry run black .`

## License

Apache-2.0
