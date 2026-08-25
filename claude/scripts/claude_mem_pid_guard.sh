#!/bin/sh
# claude-mem stale-PID guard
#
# Problema que isto resolve:
#   O supervisor do claude-mem confia no ~/.claude-mem/worker.pid e so verifica
#   se aquele PID esta vivo, nao se o processo vivo e REALMENTE o worker. Apos um
#   reboot, o macOS recicla o numero do PID para outro processo do sistema
#   (ex: distnoted agent). O supervisor entao acha que "o worker ja existe" e se
#   recusa a subir um worker novo, travando o claude-mem (sem recall de memoria).
#
# O que este guard faz, no SessionStart, antes do hook do proprio plugin:
#   1. Se o worker ja responde saudavel na porta, nao faz nada.
#   2. Se ha worker.pid apontando para um PID que esta morto, OU vivo mas que nao
#      e o worker-service.cjs (PID reciclado), remove o pidfile obsoleto.
#   3. Sobe o worker (idempotente: o start do plugin ignora spawn duplicado).
#
# Seguro rodar em toda sessao. Nao bloqueia o prompt (start vai para background).

PIDFILE="$HOME/.claude-mem/worker.pid"
PORT=37777

# 1) Worker ja saudavel? Nada a fazer.
if curl -s -m 2 "http://127.0.0.1:$PORT/api/health" 2>/dev/null | grep -q '"status":"ok"'; then
  exit 0
fi

# 2) O health-check ja falhou acima, entao o pidfile esta obsoleto em QUALQUER
#    caso: PID morto, PID reciclado para outro processo, OU PID vivo que ainda e o
#    worker-service.cjs mas esta zumbi (vivo e nao responde na porta). Este ultimo
#    caso travava o claude-mem por horas: o "start" idempotente via o PID vivo e
#    pulava o spawn. Aqui derrubamos o worker zumbi e sempre limpamos o pidfile,
#    para o passo 3 subir um worker fresco.
if [ -f "$PIDFILE" ]; then
  PID=$(sed -n 's/.*"pid"[: ]*\([0-9][0-9]*\).*/\1/p' "$PIDFILE" | head -1)
  if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null \
        && ps -p "$PID" -o command= 2>/dev/null | grep -q "worker-service.cjs"; then
    # Worker vivo mas nao-saudavel (zumbi): derruba para liberar a porta.
    pkill -f "worker-service.cjs" 2>/dev/null
    sleep 1
  fi
  rm -f "$PIDFILE"
fi

# 3) Subir o worker (descobre a versao instalada mais recente dinamicamente).
PLUG=$(ls -d "$HOME/.claude/plugins/cache/thedotmack/claude-mem/"*/ 2>/dev/null | sort -V | tail -1)
if [ -n "$PLUG" ] && [ -f "$PLUG/scripts/worker-service.cjs" ]; then
  ( node "$PLUG/scripts/bun-runner.js" "$PLUG/scripts/worker-service.cjs" start >/dev/null 2>&1 & ) >/dev/null 2>&1
fi

exit 0
