#!/bin/bash
# Runs inside the Debian 12 container started by build.sh, do not call directly.

set -euo pipefail

CACHE=build/cache
APPDIR=build/AppDir
TMP=build/tmp

trap 'chown -R "$HOST_UID:$HOST_GID" build dist appimage 2>/dev/null || true' EXIT

echo "== build tools"
apt-get -qq update
apt-get -qq install -y --no-install-recommends build-essential libasound2-dev file >/dev/null

rm -rf "$APPDIR" "$TMP"
mkdir -p "$TMP" dist

echo "== python runtime"
(cd "$TMP" && "../../$CACHE/$PYTHON_FILE" --appimage-extract >/dev/null)
mv "$TMP/squashfs-root" "$APPDIR"
PY="$APPDIR/opt/python3.11/bin/python3.11"
export SSL_CERT_FILE="$PWD/$APPDIR/opt/_internal/certs.pem"
export PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_ROOT_USER_ACTION=ignore

if [ "$RELOCK" = 1 ] || [ ! -f appimage/requirements.lock ] || [ ! -f appimage/build-requirements.lock ]; then
    echo "== regenerating lock files"
    "$PY" -m pip download -q --no-cache-dir -d "$TMP/wheels" -r requirements.txt
    "$PY" -m pip download -q --no-cache-dir -d "$TMP/build-wheels" setuptools wheel
    "$PY" appimage/mklock.py "$TMP/wheels" > appimage/requirements.lock
    "$PY" appimage/mklock.py "$TMP/build-wheels" > appimage/build-requirements.lock
fi

echo "== python packages (hash checked)"
"$PY" -m pip install -q --no-cache-dir --require-hashes -r appimage/build-requirements.lock
"$PY" -m pip install -q --no-cache-dir --require-hashes --no-build-isolation -r appimage/requirements.lock
"$PY" -m pip uninstall -q -y setuptools wheel

echo "== portaudio (ALSA only)"
tar xzf "$CACHE/$PORTAUDIO_FILE" -C "$TMP"
(cd "$TMP/portaudio" && ./configure -q --without-jack --without-oss --disable-static >/dev/null && make -s -j"$(nproc)" >/dev/null 2>&1)
mkdir -p "$APPDIR/opt/papergen/lib"
install -m 755 "$TMP/portaudio/lib/.libs/libportaudio.so.2.0.0" "$APPDIR/opt/papergen/lib/libportaudio.so.2"
strip "$APPDIR/opt/papergen/lib/libportaudio.so.2"

echo "== papergen"
cp -r papergen.py pg LICENSE "$APPDIR/opt/papergen/"
find "$APPDIR/opt/papergen" -name __pycache__ -prune -exec rm -rf {} +

# replace the python runtime metadata with ours
rm -rf "$APPDIR/AppRun" "$APPDIR/.DirIcon" "$APPDIR"/python*.desktop "$APPDIR/python.png" \
       "$APPDIR/usr/share/applications" "$APPDIR/usr/share/icons" "$APPDIR/usr/share/metainfo"
install -m 755 appimage/AppRun "$APPDIR/AppRun"
install -m 644 appimage/papergen.desktop appimage/papergen.png "$APPDIR/"
ln -s papergen.png "$APPDIR/.DirIcon"

echo "== AppImage"
ARCH=x86_64 "$CACHE/$APPIMAGETOOL_FILE" --appimage-extract-and-run --no-appstream \
    --runtime-file "$CACHE/$RUNTIME_FILE" "$APPDIR" dist/Papergen-x86_64.AppImage >/dev/null 2>&1
(cd dist && sha256sum Papergen-x86_64.AppImage > Papergen-x86_64.AppImage.sha256 && cat Papergen-x86_64.AppImage.sha256)
