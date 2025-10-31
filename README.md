# Docker AceStream ARM

Docker containers for AceStream Engine optimized for ARM architectures (ARM32 and ARM64).

## Available Images

The images are available on Docker Hub with version tags:

- **ARM32 (ARMv7)**: `jopsis/acestream:arm32-<version>`
- **ARM64 (ARMv8)**: `jopsis/acestream:arm64-<version>`

Example tags: `arm32-v3.2.14`, `arm64-v3.2.14`

## Usage

### Pull the image

For ARM32 devices:
```bash
docker pull jopsis/acestream:arm32-v3.2.14
```

For ARM64 devices:
```bash
docker pull jopsis/acestream:arm64-v3.2.14
```

### Run the container

For ARM32:
```bash
docker run -d \
  --name acestream \
  -p 6878:6878 \
  jopsis/acestream:arm32-v3.2.14
```

For ARM64:
```bash
docker run -d \
  --name acestream \
  -p 6878:6878 \
  jopsis/acestream:arm64-v3.2.14
```

### Using docker-compose

Separate docker-compose files are provided for each architecture:

For ARM32:
```bash
docker-compose -f docker-compose.arm32.yml up -d
```

For ARM64:
```bash
docker-compose -f docker-compose.arm64.yml up -d
```

**Note**: Remember to update the image tag in the docker-compose file to match the version you want to use.

## Configuration

The container exposes port 6878 by default. You can customize the AceStream engine parameters by overriding the CMD in your docker run command or docker-compose file.

Default parameters:
- `--bind-all`: Bind to all network interfaces
- `--client-console`: Enable client console
- `--live-cache-type memory`: Use memory for live cache
- `--live-mem-cache-size 104857600`: Set cache size to 100MB
- `--disable-sentry`: Disable Sentry error reporting
- `--log-stdout`: Output logs to stdout

## Compatibility

- **ARM32**: Compatible with Raspberry Pi 2/3/4 (32-bit OS), and other ARMv7 devices
- **ARM64**: Compatible with Raspberry Pi 3/4/5 (64-bit OS), and other ARMv8 devices

## Docker Hub

Images are automatically built and published to Docker Hub via GitHub Actions when a new tag is pushed:
- Repository: [jopsis/acestream](https://hub.docker.com/r/jopsis/acestream)
- Images are tagged with the git tag name (e.g., pushing tag `v3.2.14` creates `arm32-v3.2.14` and `arm64-v3.2.14`)

## License

This project packages the AceStream Engine for ARM architectures. Please refer to AceStream's original license terms.
