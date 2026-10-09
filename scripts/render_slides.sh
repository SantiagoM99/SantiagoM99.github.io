#!/usr/bin/env bash
# Convierte un PDF de slides en las imagenes del visor del sitio.
#   scripts/render_slides.sh files/slides/weef-2026-sasp.pdf
# Deja images/slides/<nombre>/slide-NN.jpg, que es donde las busca
# presentation_media() en cv_json_to_markdown_html.py.
# Requiere pdftoppm (brew install poppler).
set -euo pipefail

PDF="$1"
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$BASE_DIR/images/slides/$(basename "$PDF" .pdf)"

rm -rf "$OUT"
mkdir -p "$OUT"
# 96 dpi y ancho maximo de 1400px: legible en el visor, ~80 KB por slide
pdftoppm -r 96 -jpeg -jpegopt quality=82 -scale-to-x 1400 -scale-to-y -1 "$PDF" "$OUT/slide"
echo "$(ls "$OUT" | wc -l | tr -d ' ') slides en ${OUT#$BASE_DIR/}"
