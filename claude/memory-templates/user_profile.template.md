---
name: Perfil do Usuario
description: Quem e {{USER_NAME}} - portfolio de negocios, stakeholders, setup tecnologico
type: user
---

## Quem e {{USER_NAME}}

{{USER_BIO}}

## Portfolio de Negocios

{{BUSINESSES_LIST}}

## Stakeholders / Pessoas-Chave

{{STAKEHOLDERS_LIST}}

## Setup Tecnologico

{{TECH_SETUP}}

## Projetos Ativos

> Projetos detalhados ficam em `{{VAULT_PATH}}/Projetos/` e sao carregados via RAG.

{{ACTIVE_PROJECTS_SUMMARY}}

## Como Aplicar

Use este perfil para adaptar respostas ao contexto real do usuario. Para informacoes especificas sobre projetos ou clientes, confie no RAG hook que injeta chunks relevantes do vault Obsidian automaticamente.
