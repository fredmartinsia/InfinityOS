# Requisitos de hardware e modelos locais

O instalador mede seu computador de verdade (RAM total e livre, nucleos, GPU ou
Apple Silicon, e espaco livre em disco) antes de sugerir qualquer modelo local.
A recomendacao usa o menor entre dois limites: memoria disponivel pro modelo e
espaco em disco disponivel pro download. Voce sempre confirma antes de baixar.

## Minimo para o InfinityOS

- macOS, Linux ou WSL
- Python 3.9+, git
- Node/npx (para AIOX e algumas CLIs)
- Claude Code CLI (recomendado)

Modelos locais sao **opcionais**: sem eles, o roteador usa a nuvem (Claude/Gemini).
Se a maquina nao comportar nem o menor modelo da escada, o instalador avisa e
segue de boa com nuvem, isso nao e um erro.

## Escada de modelos locais (Ollama)

Do maior para o menor. O instalador recomenda a maior opcao que caiba com folga.

| Modelo | Parametros | Tamanho (disco/memoria) |
|---|---|---|
| `qwen3-coder:30b` | 30B (MoE, ~3.3B ativos) | ~19 GB |
| `qwen2.5-coder:14b` | 14B | ~9 GB |
| `qwen2.5-coder:7b` | 7B | ~4.7 GB |
| `qwen2.5-coder:3b` | 3B | ~1.9 GB |
| `qwen2.5-coder:1.5b` | 1.5B | ~1 GB |
| `qwen2.5-coder:0.5b` | 0.5B | ~0.5 GB |

Regra usada pelo instalador (passo `20-models.sh`):

1. Memoria disponivel = RAM total menos 8 GB reservados pro sistema. Se houver
   GPU NVIDIA dedicada com VRAM maior que essa sobra, usa a VRAM no lugar.
2. Disco disponivel = espaco livre em `$HOME` menos 2 GB de margem de seguranca.
3. Limite = o menor dos dois valores acima.
4. Recomenda a maior linha da tabela cujo tamanho cabe dentro do limite.
5. A pessoa pode aceitar, trocar por outra opcao da escada (com aviso de risco
   se nao couber com folga) ou nao instalar modelo local nenhum.

A escada fica em `routing/hardware-tiers.yaml` (editavel, mesma fonte de numeros
usada pelo script). O instalador roda `ollama pull <modelo>` so depois da sua
confirmacao, e mostra o tamanho do download antes de perguntar.
