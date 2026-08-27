#!/usr/bin/env bash
# ==========================================
#   SYNC My-CV -> Sitio web (macOS/Linux)
# ==========================================
# My-CV/data/cv-data.json es la FUENTE DE VERDAD. Este script:
#   1. Copia el JSON de My-CV a _data/cv.json y verifica que queden idénticos
#   2. Regenera _publications/ y _data/cv.yml (modo seguro, por defecto)
#   3. Con --pdfs: copia los PDFs compilados de My-CV a files/
#   4. Con --all:  corre el generador COMPLETO (cv_json_to_markdown_html.py)
#      ⚠️  --all también regenera homepage (_pages/about.md), experiencia,
#          teaching y talks: pisa cualquier edición manual en esos archivos.
#
# Uso típico tras editar el CV:
#   cd My-CV && ./create_all.sh
#   cd ../SantiagoM99.github.io && scripts/sync_from_mycv.sh --pdfs
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MYCV_DIR="$BASE_DIR/../My-CV"
MYCV_JSON="$MYCV_DIR/data/cv-data.json"
SITE_JSON="$BASE_DIR/_data/cv.json"

DO_ALL=false
DO_PDFS=false
for arg in "$@"; do
  case "$arg" in
    --all)  DO_ALL=true ;;
    --pdfs) DO_PDFS=true ;;
    *) echo "Uso: $0 [--all] [--pdfs]"; exit 1 ;;
  esac
done

if [ ! -f "$MYCV_JSON" ]; then
  echo "ERROR: No se encuentra $MYCV_JSON"
  exit 1
fi

# --- 1. Entorno python con PyYAML (venv local del repo) ---
VENV="$BASE_DIR/.venv"
if [ ! -x "$VENV/bin/python3" ]; then
  echo "[setup] Creando venv en .venv con PyYAML..."
  python3 -m venv "$VENV"
fi
"$VENV/bin/python3" -c "import yaml" 2>/dev/null || "$VENV/bin/pip" install -q pyyaml

# --- 2. Sincronizar JSON (My-CV es la fuente de verdad) ---
echo "[1/3] Copiando cv-data.json de My-CV a _data/cv.json..."
cp "$MYCV_JSON" "$SITE_JSON"
if cmp -s "$MYCV_JSON" "$SITE_JSON"; then
  echo "      JSONs idénticos ✓"
else
  echo "ERROR: los JSONs difieren tras la copia (¿problema de permisos?)"
  exit 1
fi

# --- 3. Regenerar contenido del sitio ---
cd "$BASE_DIR"
if [ "$DO_ALL" = true ]; then
  echo "[2/3] Regenerando TODO el sitio (--all)..."
  "$VENV/bin/python3" cv_json_to_markdown_html.py
else
  echo "[2/3] Regenerando publications, experience, teaching, talks y cv.yml (modo seguro)..."
  "$VENV/bin/python3" - <<'PY'
import json, importlib.util
spec = importlib.util.spec_from_file_location('gen', 'cv_json_to_markdown_html.py')
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)
cv = json.load(open('_data/cv.json', encoding='utf-8'))
gen.generate_publications(cv)
gen.generate_talks(cv)
gen.generate_experience(cv)
gen.generate_teaching(cv)
gen.generate_data_files(cv)
# Solo homepage (_pages/about.md) y cv-template quedan fuera: tienen ediciones a mano
PY
fi
rm -rf "$BASE_DIR/__pycache__"

# --- 4. PDFs ---
if [ "$DO_PDFS" = true ]; then
  echo "[3/3] Copiando PDFs compilados a files/..."
  copied=false
  if [ -f "$MYCV_DIR/output/CV.pdf" ]; then
    cp "$MYCV_DIR/output/CV.pdf" "$BASE_DIR/files/CV.pdf" && echo "      files/CV.pdf ✓" && copied=true
  fi
  if [ -f "$MYCV_DIR/output_resume/Resume.pdf" ]; then
    cp "$MYCV_DIR/output_resume/Resume.pdf" "$BASE_DIR/files/Resume.pdf" && echo "      files/Resume.pdf ✓" && copied=true
  fi
  if [ "$copied" = false ]; then
    echo "      No hay PDFs en My-CV/output — corre primero My-CV/create_all.sh"
  fi
else
  echo "[3/3] PDFs no copiados (usa --pdfs para actualizar files/CV.pdf y files/Resume.pdf)"
fi

echo
echo "✅ Sync completo. Revisa 'git status' y commitea cuando estés conforme."
