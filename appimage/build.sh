#!/bin/bash
# Builds dist/Papergen-x86_64.AppImage inside a pinned Debian 12 container.
# Needs docker and Internet (only on the build machine, the AppImage runs offline).
#
# usage: appimage/build.sh [--relock]
#   --relock  regenerate the hash-pinned lock files from requirements.txt

set -euo pipefail
cd "$(dirname "$0")/.."

# every external input is pinned by sha256
DEBIAN_IMAGE="debian:12@sha256:f37a335e82bca302e955fa39f9dfe28f1be618f016f8a2b56318e5a5111afc26"

PYTHON_FILE="python3.11.16-cp311-cp311-manylinux2014_x86_64.AppImage"
PYTHON_URL="https://github.com/niess/python-appimage/releases/download/python3.11/$PYTHON_FILE"
PYTHON_SHA256="f5b09b90cc91aafd2594213958d71125ddcc32110767056259890b8c02cb31d0"

APPIMAGETOOL_FILE="appimagetool-1.9.1-x86_64.AppImage"
APPIMAGETOOL_URL="https://github.com/AppImage/appimagetool/releases/download/1.9.1/appimagetool-x86_64.AppImage"
APPIMAGETOOL_SHA256="ed4ce84f0d9caff66f50bcca6ff6f35aae54ce8135408b3fa33abfc3cb384eb0"

RUNTIME_FILE="runtime-20251108-x86_64"
RUNTIME_URL="https://github.com/AppImage/type2-runtime/releases/download/20251108/runtime-x86_64"
RUNTIME_SHA256="2fca8b443c92510f1483a883f60061ad09b46b978b2631c807cd873a47ec260d"

PORTAUDIO_FILE="pa_stable_v190700_20210406.tgz"
PORTAUDIO_URL="https://files.portaudio.com/archives/$PORTAUDIO_FILE"
PORTAUDIO_SHA256="47efbf42c77c19a05d22e627d42873e991ec0c1357219c0d74ce6a2948cb2def"

CACHE=build/cache
mkdir -p "$CACHE"

fetch() {
    local url=$1 sum=$2 out="$CACHE/$3"
    if [ ! -f "$out" ]; then
        curl -sSfL -o "$out.part" "$url"
        mv "$out.part" "$out"
    fi
    if ! echo "$sum  $out" | sha256sum -c --quiet -; then
        echo "checksum mismatch for $out, removed" >&2
        rm -f "$out"
        exit 1
    fi
}

fetch "$PYTHON_URL" "$PYTHON_SHA256" "$PYTHON_FILE"
fetch "$APPIMAGETOOL_URL" "$APPIMAGETOOL_SHA256" "$APPIMAGETOOL_FILE"
fetch "$RUNTIME_URL" "$RUNTIME_SHA256" "$RUNTIME_FILE"
fetch "$PORTAUDIO_URL" "$PORTAUDIO_SHA256" "$PORTAUDIO_FILE"
chmod +x "$CACHE/$PYTHON_FILE" "$CACHE/$APPIMAGETOOL_FILE"

RELOCK=0
[ "${1:-}" = "--relock" ] && RELOCK=1

docker run --rm -v "$PWD:/src" -w /src \
    -e HOST_UID="$(id -u)" -e HOST_GID="$(id -g)" -e RELOCK="$RELOCK" \
    -e PYTHON_FILE="$PYTHON_FILE" -e APPIMAGETOOL_FILE="$APPIMAGETOOL_FILE" \
    -e RUNTIME_FILE="$RUNTIME_FILE" -e PORTAUDIO_FILE="$PORTAUDIO_FILE" \
    "$DEBIAN_IMAGE" bash appimage/build-in-container.sh
