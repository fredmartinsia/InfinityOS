#!/usr/bin/env bash
# ============================================================================
#  Passo 40 — AIOX (framework de agentes po/architect/dev/qa/...).
#  Instalado pelo instalador oficial via npx (não redistribuímos a cópia).
# ============================================================================
ui_header "5/8 — Framework AIOX (opcional)"

if [ "${INFINITE_OS_SKIP_AIOX:-0}" = "1" ]; then
  ui_dim "Passo do AIOX pulado (INFINITE_OS_SKIP_AIOX=1)."
  return 0 2>/dev/null || true
fi

if [ "${NODE_OK:-0}" != "1" ]; then
  ui_warn "Node/npx ausente — não dá para instalar o AIOX agora."
  ui_dim "Instale o Node e rode depois:  npx aiox-core@latest install"
  return 0 2>/dev/null || true
fi

ui_info "O AIOX adiciona um time de agentes (po, architect, dev, qa, sm, devops...)."
if [ "${ASSUME_YES:-0}" != "1" ] && ! ui_yesno "Quer instalar o AIOX agora (via npx oficial)?" "Y"; then
  ui_dim "Pulado. Quando quiser:  npx aiox-core@latest install"
  return 0 2>/dev/null || true
fi

ui_dim "Rodando: npx aiox-core@latest install  (segue o wizard do próprio AIOX)"
if npx -y aiox-core@latest install </dev/tty; then
  ui_ok "AIOX instalado."
else
  ui_warn "Instalação do AIOX não concluída (rode 'npx aiox-core@latest install' manualmente)."
fi
