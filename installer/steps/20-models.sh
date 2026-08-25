#!/usr/bin/env bash
# ============================================================================
#  Passo 20 - Modelos locais: mede a maquina de verdade (RAM, nucleos, GPU e
#  espaco livre em disco), recomenda o maior modelo Ollama que cabe com folga,
#  deixa a pessoa escolher e baixa. Exporta CHOSEN_LOCAL_MODEL (usado no
#  passo 30). Se nada for instalado, exporta CHOSEN_LOCAL_MODEL vazio (o
#  roteador entao usa nuvem, e nao um nome de modelo inexistente).
#
#  A escada de modelos abaixo espelha routing/hardware-tiers.yaml (mesma
#  fonte de numeros). Tamanhos em disco/memoria sao os publicados pelo
#  proprio Ollama (ollama.com/library), nao estimativa as cegas.
# ============================================================================
ui_header "4/11 · Modelo local (opcional)"

CHOSEN_LOCAL_MODEL=""

if [ "${INFINITY_OS_SKIP_MODELS:-0}" = "1" ]; then
  ui_dim "Passo de modelos locais pulado (INFINITY_OS_SKIP_MODELS=1)."
  export CHOSEN_LOCAL_MODEL
  return 0 2>/dev/null || true
fi

# HAS_OLLAMA vem do passo 10. Se este passo for rodado sozinho, com
# ./install.sh --step=20, aquela variavel nao existe: entao detectamos aqui.
if [ -z "${HAS_OLLAMA:-}" ]; then
  if command -v ollama >/dev/null 2>&1; then HAS_OLLAMA=1; else HAS_OLLAMA=0; fi
fi

if [ "${HAS_OLLAMA:-0}" != "1" ]; then
  ui_dim "Ollama nao esta instalado, pulando modelos locais. (O roteador usa nuvem.)"
  ui_dim "Se quiser modelo local depois: instale o Ollama e rode ./install.sh --step=20"
  export CHOSEN_LOCAL_MODEL
  return 0 2>/dev/null || true
fi

# --- Escada de modelos (do maior para o menor) -------------------------------
# tag ollama | parametros (texto) | tamanho em disco/memoria, em decimos de GB
LADDER_TAGS=(qwen3-coder:30b qwen2.5-coder:14b qwen2.5-coder:7b qwen2.5-coder:3b qwen2.5-coder:1.5b qwen2.5-coder:0.5b)
LADDER_PARAMS=("30 bilhoes de parametros" "14 bilhoes de parametros" "7 bilhoes de parametros" "3 bilhoes de parametros" "1,5 bilhao de parametros" "0,5 bilhao de parametros")
LADDER_SIZE_X10=(190 90 50 20 10 5)   # 19.0GB 9.0GB 5.0GB 2.0GB 1.0GB 0.5GB

fmt_gb() { # imprime decimos de GB como "X.Y"
  local x10="$1"
  printf '%d.%d' "$(( x10 / 10 ))" "$(( x10 % 10 ))"
}

# --- 1) Analise real da maquina ----------------------------------------------
ui_step "Medindo sua maquina..."

# RAM, nucleos e tipo de processador vem do passo 00. Se este passo rodar
# sozinho (./install.sh --step=20), aquelas variaveis nao existem, entao
# medimos aqui na hora. Sem isso a conta daria zero e recusaria modelo local
# ate numa maquina folgada.
if [ -z "${OS_KIND:-}" ]; then
  case "$(uname -s)" in
    Darwin) OS_KIND="macos" ;;
    Linux)  OS_KIND="linux" ;;
    *)      OS_KIND="outro" ;;
  esac
fi

if [ -z "${RAM_GB:-}" ] || [ "${RAM_GB:-0}" -eq 0 ] 2>/dev/null; then
  if [ "$OS_KIND" = "macos" ]; then
    _bytes=$(sysctl -n hw.memsize 2>/dev/null)
    [ -n "$_bytes" ] && RAM_GB=$(( _bytes / 1024 / 1024 / 1024 ))
  elif [ -r /proc/meminfo ]; then
    _kb=$(awk '/MemTotal/ {print $2}' /proc/meminfo)
    [ -n "$_kb" ] && RAM_GB=$(( _kb / 1024 / 1024 ))
  fi
fi
: "${RAM_GB:=0}"

if [ -z "${CPU_CORES:-}" ]; then
  if [ "$OS_KIND" = "macos" ]; then
    CPU_CORES=$(sysctl -n hw.ncpu 2>/dev/null)
  elif command -v nproc >/dev/null 2>&1; then
    CPU_CORES=$(nproc)
  fi
fi

if [ -z "${IS_APPLE_SILICON:-}" ] && [ "$OS_KIND" = "macos" ]; then
  case "$(uname -m)" in
    arm64) IS_APPLE_SILICON=1 ;;
    *)     IS_APPLE_SILICON=0 ;;
  esac
fi

if [ -z "${HAS_NVIDIA:-}" ]; then
  if command -v nvidia-smi >/dev/null 2>&1; then
    HAS_NVIDIA=1
    if [ -z "${VRAM_GB:-}" ]; then
      _vram=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
      [ -n "$_vram" ] && VRAM_GB=$(( _vram / 1024 ))
    fi
  else
    HAS_NVIDIA=0
  fi
fi

ram_total="${RAM_GB:-0}"

# RAM livre agora (so informativo; a conta usa RAM total menos reserva, porque
# RAM livre varia o tempo todo e nao e base confiavel pra decisao).
ram_free_gb=""
if [ "${OS_KIND:-}" = "macos" ] && command -v vm_stat >/dev/null 2>&1; then
  page_size=$(vm_stat | head -1 | grep -o '[0-9]\+' | head -1)
  free_pages=$(vm_stat | awk '/Pages free/ {gsub("\\.", ""); print $3}')
  inactive_pages=$(vm_stat | awk '/Pages inactive/ {gsub("\\.", ""); print $3}')
  if [ -n "$page_size" ] && [ -n "$free_pages" ] && [ -n "$inactive_pages" ]; then
    ram_free_gb=$(( (free_pages + inactive_pages) * page_size / 1024 / 1024 / 1024 ))
  fi
elif [ -r /proc/meminfo ]; then
  avail_kb=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
  [ -n "$avail_kb" ] && ram_free_gb=$(( avail_kb / 1024 / 1024 ))
fi

# Espaco livre em disco (onde o Ollama guarda os modelos: $HOME). df -Pk existe
# tanto no macOS quanto no Linux, formato POSIX estavel.
disk_free_kb=$(df -Pk "$HOME" 2>/dev/null | awk 'NR==2 {print $4}')
[ -z "$disk_free_kb" ] && disk_free_kb=0
disk_free_x10=$(( disk_free_kb * 10 / 1048576 ))

ui_info "Memoria (RAM) total: ${ram_total} GB"
if [ -n "$ram_free_gb" ]; then
  ui_info "Memoria livre agora: ${ram_free_gb} GB"
fi
ui_info "Nucleos de processador: ${CPU_CORES:-?}"
if [ "${IS_APPLE_SILICON:-0}" = "1" ]; then
  ui_info "Placa de video: Apple Silicon (memoria unificada: processador e video usam a mesma RAM)"
elif [ "${HAS_NVIDIA:-0}" = "1" ]; then
  ui_info "Placa de video dedicada: NVIDIA, com ${VRAM_GB:-0} GB de memoria de video (VRAM)"
else
  ui_info "Placa de video: nenhuma dedicada encontrada (o modelo roda no processador, mais devagar)"
fi
ui_info "Espaco livre em disco (em \$HOME): $(fmt_gb "$disk_free_x10") GB"

# --- 2) Regra de recomendacao -------------------------------------------------
# Memoria disponivel pro modelo: RAM total menos 8 GB reservados pro resto do
# sistema (SO, apps, o proprio Claude Code). Se houver GPU NVIDIA dedicada com
# mais memoria de video do que essa sobra, o modelo roda nela em vez de disputar
# RAM do sistema, entao a VRAM vira o teto.
# A reserva pro sistema e proporcional, nao fixa. Reservar 8 GB fixos faria uma
# maquina de 8 GB ficar sem nada, quando ela aguenta bem um modelo pequeno.
# Regra: metade da RAM, limitada a no maximo 8 GB e no minimo 3 GB.
mem_reserve_gb=$(( ram_total / 2 ))
[ "$mem_reserve_gb" -gt 8 ] && mem_reserve_gb=8
[ "$mem_reserve_gb" -lt 3 ] && mem_reserve_gb=3

mem_budget_gb=$(( ram_total - mem_reserve_gb ))
[ "$mem_budget_gb" -lt 0 ] && mem_budget_gb=0
mem_budget_reason="memoria (RAM total menos ${mem_reserve_gb} GB reservados pro sistema)"
if [ "${HAS_NVIDIA:-0}" = "1" ] && [ "${VRAM_GB:-0}" -gt "$mem_budget_gb" ]; then
  mem_budget_gb="${VRAM_GB:-0}"
  mem_budget_reason="memoria de video (VRAM) da GPU NVIDIA"
fi
mem_budget_x10=$(( mem_budget_gb * 10 ))

# Espaco em disco disponivel pro download, com 2 GB de margem de seguranca
# (o Ollama tambem usa disco temporario durante o download).
disk_budget_x10=$(( disk_free_x10 - 20 ))
[ "$disk_budget_x10" -lt 0 ] && disk_budget_x10=0

ui_info "Memoria disponivel pro modelo (${mem_budget_reason}): $(fmt_gb "$mem_budget_x10") GB"
ui_info "Disco disponivel pro download (com margem de seguranca): $(fmt_gb "$disk_budget_x10") GB"

if [ "$mem_budget_x10" -le "$disk_budget_x10" ]; then
  limiting_x10="$mem_budget_x10"; limiting_desc="memoria"
else
  limiting_x10="$disk_budget_x10"; limiting_desc="disco"
fi

# Escolhe a maior opcao da escada que cabe com folga no limite calculado.
rec_idx=-1
i=0
while [ "$i" -lt "${#LADDER_TAGS[@]}" ]; do
  if [ "${LADDER_SIZE_X10[$i]}" -le "$limiting_x10" ]; then
    rec_idx=$i
    break
  fi
  i=$(( i + 1 ))
done

echo

# --- 3) Apresenta a escolha e deixa a pessoa decidir --------------------------
do_pull=0
final_choice=""

if [ "$rec_idx" -ge 0 ]; then
  rec_tag="${LADDER_TAGS[$rec_idx]}"
  rec_size_gb="$(fmt_gb "${LADDER_SIZE_X10[$rec_idx]}")"
  ui_ok "Recomendo: ${rec_tag} (${LADDER_PARAMS[$rec_idx]})"
  ui_dim "Motivo: voce tem $(fmt_gb "$limiting_x10") GB livres em ${limiting_desc}, e esse modelo ocupa ${rec_size_gb} GB (em disco e em memoria)."

  if [ "${ASSUME_YES:-0}" = "1" ]; then
    # No modo automatico NAO baixamos: um download de varios GB sem ninguem
    # olhando e surpresa ruim, ainda mais em internet limitada ou paga por uso.
    # Recomendamos e deixamos o comando pronto.
    ui_info "Modo automatico: nao vou baixar nada sem voce ver."
    ui_dim "Quando quiser o modelo recomendado, rode:  ollama pull ${rec_tag}"
    ui_dim "Ou rode este passo de novo no modo normal:  ./install.sh --step=20"
    CHOSEN_LOCAL_MODEL=""
    export CHOSEN_LOCAL_MODEL
    log "models: recomendado=$rec_tag (nao baixado, modo automatico)"
    return 0 2>/dev/null || true
  else
    if ui_yesno "Baixar o modelo recomendado agora (download de ~${rec_size_gb} GB)?" "Y"; then
      final_choice="$rec_tag"; do_pull=1
    elif ui_yesno "Quer escolher outro modelo da lista (inclusive um maior, por sua conta e risco)?" "N"; then
      opts=()
      k=0
      while [ "$k" -lt "${#LADDER_TAGS[@]}" ]; do
        tag="${LADDER_TAGS[$k]}"
        size_gb="$(fmt_gb "${LADDER_SIZE_X10[$k]}")"
        if [ "${LADDER_SIZE_X10[$k]}" -le "$limiting_x10" ]; then
          opts+=("$tag (${size_gb} GB) - cabe")
        else
          opts+=("$tag (${size_gb} GB) - NAO cabe com folga, risco de travar ou o download falhar")
        fi
        k=$(( k + 1 ))
      done
      opts+=("Nao instalar modelo local (usar so nuvem)")
      picked="$(ui_choice "Qual modelo?" "${opts[@]}")"
      picked_idx=$(( picked - 1 ))
      if [ "$picked_idx" -ge "${#LADDER_TAGS[@]}" ]; then
        do_pull=0
      else
        cand_tag="${LADDER_TAGS[$picked_idx]}"
        if [ "${LADDER_SIZE_X10[$picked_idx]}" -gt "$limiting_x10" ]; then
          if ui_yesno "Esse modelo pode nao caber (risco real de travar a maquina ou o download falhar). Confirma mesmo assim?" "N"; then
            final_choice="$cand_tag"; do_pull=1
          fi
        else
          final_choice="$cand_tag"; do_pull=1
        fi
      fi
    fi
  fi
else
  ui_warn "Sua maquina nao comporta nem o menor modelo local com folga (limite: $(fmt_gb "$limiting_x10") GB em ${limiting_desc})."
  ui_dim "Sem problema: o sistema vai funcionar com modelo em nuvem (Claude/Gemini), que e o caminho normal."
  if [ "${ASSUME_YES:-0}" != "1" ]; then
    last_i=$(( ${#LADDER_TAGS[@]} - 1 ))
    smallest_tag="${LADDER_TAGS[$last_i]}"
    smallest_gb="$(fmt_gb "${LADDER_SIZE_X10[$last_i]}")"
    if ui_yesno "Mesmo assim quer tentar o menor modelo (${smallest_tag}, ${smallest_gb} GB, risco de nao caber)?" "N"; then
      final_choice="$smallest_tag"; do_pull=1
    fi
  fi
fi

# --- 4) Baixa o modelo escolhido (se houver) ----------------------------------
if [ "$do_pull" = "1" ] && [ -n "$final_choice" ]; then
  ui_dim "Baixando ${final_choice} (pode levar alguns minutos, depende da sua internet)..."
  if log_run ollama pull "$final_choice"; then
    ui_ok "Modelo ${final_choice} pronto."
    CHOSEN_LOCAL_MODEL="$final_choice"
  else
    ui_warn "Falha no download de ${final_choice} (veja o log). Sem modelo local por enquanto, o roteador usa nuvem."
    CHOSEN_LOCAL_MODEL=""
  fi
else
  ui_dim "Nenhum modelo local instalado agora. O roteador usa nuvem ate voce baixar um (ollama pull <modelo>)."
fi

export CHOSEN_LOCAL_MODEL
log "models: ram=${ram_total}GB disk_free=$(fmt_gb "$disk_free_x10")GB mem_budget=$(fmt_gb "$mem_budget_x10")GB disk_budget=$(fmt_gb "$disk_budget_x10")GB limiting=$limiting_desc chosen=$CHOSEN_LOCAL_MODEL"
