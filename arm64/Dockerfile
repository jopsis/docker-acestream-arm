# Dockerfile to recreate futebas/acestream-engine-arm:3.2.7.6 from scratch
# Based on extracted layers from the original image

# Use Alpine Linux 3.21.0 as base (ARM64)
FROM alpine:3.21.0

# Set environment variables
# ENV ACESTREAM_HOME=/acestream \
#     ANDROID_ROOT=/system \
#     ANDROID_DATA=/data \
#     PYTHONHOME=/acestream/python \
#     PYTHONPATH=/acestream/python/lib/stdlib:/acestream/python/lib/modules:/acestream/data:/acestream/modules.zip:/acestream/eggs-unpacked:/acestream/lib \
#     LD_LIBRARY_PATH=/system/lib64:/system/lib:/acestream/python/lib \
#     TEMP=/tmp \
#     PATH=/acestream/python/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
#RUN apk add --no-cache git bash build-base libffi-dev openssl-dev bzip2-dev zlib-dev xz-dev readline-dev sqlite-dev tk-dev zstd-dev

ENV ACESTREAM_HOME=/acestream \
    ANDROID_ROOT=/system \
    ANDROID_DATA=/data \
    PYTHONHOME=/acestream/python \
    PYTHONPATH=/acestream/python/lib/stdlib:/acestream/python/lib/modules:/acestream/data:/acestream/modules.zip:/acestream/eggs-unpacked:/acestream/lib \
    LD_LIBRARY_PATH=/system/lib64:/system/lib:/acestream/python/lib \
    TEMP=/tmp \
    PATH=/acestream/python/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Copy the acestream engine files
# You need to extract these from the original image or obtain the AceStream Android APK
COPY acestream_3.2.13.arm8.zip / 
RUN unzip /acestream_3.2.13.arm8.zip && rm /acestream_3.2.13.arm8.zip

# Copy Android system libraries
# These are extracted from Android system or the original image
#COPY system /system
COPY system.zip /
RUN unzip /system.zip && rm /system.zip
#RUN chmod -R 755 /acestream/python/lib

# Add main.py and dnsproxyd.py scripts
ADD main.py dnsproxyd.py /acestream/

# Set working directory
WORKDIR /acestream

# Expose AceStream ports
EXPOSE 6878 8621

# Default command to run AceStream engine
CMD ["python", "main.py", "--bind-all", "--client-console", "--live-cache-type", "memory", "--live-mem-cache-size", "104857600", "--disable-sentry", "--log-stdout" ]
