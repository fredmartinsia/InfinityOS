# Dev Squad — Time de Desenvolvimento de Software

Squad de desenvolvimento reutilizável em qualquer projeto. Planeja, arquiteta, implementa, revisa código, audita segurança e faz QA com gate do Juiz (nota mínima 9.0).

A definição executável (pipeline Opensquad) vive em `{{HOME}}/squads/dev-squad/`. Estes comandos são os atalhos conversacionais (slashes) pra acionar o chefe e os especialistas direto.

## Elenco (clones reais)

Os papéis são clones completos de lendas reais da engenharia (12 módulos no vault, validados nos 2 juízes >= 9.0). Cada um tem slash própria; a slash namespaced do papel carrega o mesmo clone.

| Papel | Clone real | Slash direta | Slash do papel |
|-------|-----------|--------------|----------------|
| Chefe | (sintético) | `/devsquad-chief` | `/dev-squad:agents:devsquad-chief` |
| 🗺️ Planejador | Kent Beck | `/kent-beck` | `/dev-squad:agents:plano` |
| 🏛️ Arquiteto | Martin Fowler | `/martin-fowler` | `/dev-squad:agents:arquiteta` |
| ⌨️ Implementador | Guillermo Rauch | `/guillermo-rauch` | `/dev-squad:agents:dev` |
| 🔍 Revisor | Robert C. Martin | `/robert-c-martin` | `/dev-squad:agents:revisor` |
| 🛡️ Segurança | Jim Manico | `/jim-manico` | `/dev-squad:agents:seguranca` |
| ✅ QA / Juiz | Kent C. Dodds | `/kent-c-dodds` | `/dev-squad:agents:qa` |

## Modos

- **Pipeline completo (automático):** `/opensquad run dev-squad` — ciclo inteiro com checkpoints.
- **Chefe:** `/devsquad-chief` — orquestra e roteia conforme a tarefa.
- **Especialista direto:** use a slash do agente pra um pedido pontual (só um review, só o plano, etc).
