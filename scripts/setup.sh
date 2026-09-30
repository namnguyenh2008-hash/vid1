#!/bin/bash
# Prepare a fresh cloud session: ffmpeg, render browser, ASR model, fonts, GSAP. Idempotent.
set -e
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg >/dev/null)
python3 -c "import sherpa_onnx, soundfile" 2>/dev/null || pip install -q sherpa-onnx soundfile numpy
M=/home/user/models/sherpa-onnx-zipformer-vi-2025-04-20
[ -d "$M" ] || (mkdir -p /home/user/models && curl -sSL https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-zipformer-vi-2025-04-20.tar.bz2 | tar xj -C /home/user/models)
mkdir -p vendor/fonts
if [ ! -f vendor/gsap.min.js ]; then
  T=$(mktemp -d) && (cd "$T" && npm i --silent gsap @fontsource/be-vietnam-pro >/dev/null)
  cp "$T/node_modules/gsap/dist/gsap.min.js" vendor/
  for s in vietnamese latin; do for w in 600 800; do cp "$T/node_modules/@fontsource/be-vietnam-pro/files/be-vietnam-pro-$s-$w-normal.woff2" vendor/fonts/bvp-$s-$w.woff2; done; done
fi
npx -y hyperframes browser ensure >/dev/null 2>&1 || true
echo "setup ok"
