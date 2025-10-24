# Docker AceStream ARM

Docker containers for AceStream Engine optimized for ARM architectures (ARM32 and ARM64).

## Available Images

The images are available on Docker Hub:

- **ARM32 (ARMv7)**: `jopsis/acestream:arm32`
- **ARM64 (ARMv8)**: `jopsis/acestream:arm64`

## Usage

### Pull the image

For ARM32 devices:
```bash
docker pull jopsis/acestream:arm32
```

For ARM64 devices:
```bash
docker pull jopsis/acestream:arm64
```

### Run the container

For ARM32:
```bash
docker run -d \
  --name acestream \
  -p 6878:6878 \
  jopsis/acestream:arm32
```

For ARM64:
```bash
docker run -d \
  --name acestream \
  -p 6878:6878 \
  jopsis/acestream:arm64
```

### Using docker-compose

You can also use the included `docker-compose.yml` file:

```bash
docker-compose up -d
```

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

Images are automatically built and published to Docker Hub via GitHub Actions:
- Repository: [jopsis/acestream](https://hub.docker.com/r/jopsis/acestream)

## License

This project packages the AceStream Engine for ARM architectures. Please refer to AceStream's original license terms.
