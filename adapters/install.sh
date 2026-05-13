#!/usr/bin/env bash
# install.sh — instala HackingWebbyDM20911 en el host de IA correcto.
# Auto-detecta Claude Code, Gemini CLI, Cursor, Aider, OpenAI Codex CLI o cae a generic.
# Uso:
#   bash adapters/install.sh                     # auto-detección
#   bash adapters/install.sh --host gemini       # forzar host
#   bash adapters/install.sh --host cursor --project-dir /ruta
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
HOST=""
PROJECT_DIR="$PWD"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host) HOST="$2"; shift 2;;
    --project-dir) PROJECT_DIR="$2"; shift 2;;
    --help|-h)
      sed -n '2,7p' "$0"; exit 0;;
    *) echo "Argumento desconocido: $1" >&2; exit 1;;
  esac
done

c_green=$'\033[0;32m'; c_yellow=$'\033[0;33m'; c_red=$'\033[0;31m'; c_reset=$'\033[0m'
say()  { echo "${c_green}[ok]${c_reset} $*"; }
warn() { echo "${c_yellow}[--]${c_reset} $*"; }
err()  { echo "${c_red}[!!]${c_reset} $*" >&2; }

detect_host() {
  local found=()
  command -v claude >/dev/null 2>&1 && found+=("claude")
  command -v gemini >/dev/null 2>&1 && found+=("gemini")
  command -v cursor-agent >/dev/null 2>&1 || command -v cursor >/dev/null 2>&1 && found+=("cursor")
  command -v aider >/dev/null 2>&1 && found+=("aider")
  command -v codex >/dev/null 2>&1 && found+=("openai-codex")

  if [[ -z "${found[*]:-}" ]]; then
    [[ -n "${ANTHROPIC_API_KEY:-}" ]] && found+=("claude")
    [[ -n "${GEMINI_API_KEY:-}${GOOGLE_API_KEY:-}" ]] && found+=("gemini")
    [[ -n "${OPENAI_API_KEY:-}" ]] && found+=("openai-codex")
  fi

  if [[ ${#found[@]} -eq 0 ]]; then
    echo "generic"; return
  elif [[ ${#found[@]} -eq 1 ]]; then
    echo "${found[0]}"; return
  else
    warn "Detectados varios hosts: ${found[*]}"
    echo "Selecciona uno:" >&2
    select h in "${found[@]}" "generic"; do
      [[ -n "$h" ]] && { echo "$h"; return; }
    done
  fi
}

[[ -z "$HOST" ]] && HOST="$(detect_host)"
say "Host objetivo: $HOST"
say "Skill source:  $SKILL_DIR"

case "$HOST" in
  claude)
    target="$HOME/.claude/skills/HackingWebbyDM20911"
    mkdir -p "$(dirname "$target")"
    if [[ -e "$target" && ! -L "$target" ]]; then
      warn "Ya existe $target — haciendo backup a ${target}.bak"
      mv "$target" "${target}.bak.$(date +%s)"
    fi
    [[ "$SKILL_DIR" == "$target" ]] || ln -sfn "$SKILL_DIR" "$target"
    say "Listo. Reinicia Claude Code o Claude Desktop. Invocala con /hackweb."
    ;;

  gemini)
    target="$HOME/.gemini/extensions/HackingWebbyDM20911"
    mkdir -p "$target"
    cp "$SCRIPT_DIR/gemini/GEMINI.md" "$target/GEMINI.md"
    cp "$SCRIPT_DIR/gemini/gemini-extension.json" "$target/gemini-extension.json"
    ln -sfn "$SKILL_DIR/references" "$target/references"
    ln -sfn "$SKILL_DIR/scripts" "$target/scripts"
    ln -sfn "$SKILL_DIR/assets" "$target/assets"
    say "Listo. Reinicia 'gemini'. Invocala diciendo: 'usa HackingWebbyDM20911 para auditar X'."
    ;;

  cursor)
    mkdir -p "$PROJECT_DIR"
    target="$PROJECT_DIR/.cursorrules"
    cat "$SCRIPT_DIR/cursor/.cursorrules" > "$target"
    echo "" >> "$target"
    echo "# === HackingWebbyDM20911 references path ===" >> "$target"
    echo "# Skill base: $SKILL_DIR" >> "$target"
    say "Escrito $target. Reinicia Cursor en $PROJECT_DIR."
    ;;

  aider)
    mkdir -p "$PROJECT_DIR"
    cat "$SCRIPT_DIR/aider/CONVENTIONS.md" > "$PROJECT_DIR/CONVENTIONS.md"
    cp "$SCRIPT_DIR/aider/.aider.conf.yml" "$PROJECT_DIR/.aider.conf.yml" 2>/dev/null || true
    say "Escrito CONVENTIONS.md y .aider.conf.yml en $PROJECT_DIR."
    say "Lánzalo con: aider --read CONVENTIONS.md"
    ;;

  openai-codex|generic)
    mkdir -p "$PROJECT_DIR"
    target="$PROJECT_DIR/AGENTS.md"
    src="$SCRIPT_DIR/${HOST}/AGENTS.md"
    [[ -f "$src" ]] || src="$SCRIPT_DIR/generic/AGENTS.md"
    cat "$src" > "$target"
    echo "" >> "$target"
    echo "# Skill base: $SKILL_DIR" >> "$target"
    say "Escrito $target. Cualquier agente que lea AGENTS.md lo recogerá."
    ;;

  *)
    err "Host '$HOST' no soportado. Usa uno de: claude, gemini, cursor, aider, openai-codex, generic"
    exit 1;;
esac

echo
say "Adapter '${HOST}' instalado. Ver adapters/README.md para detalles."
