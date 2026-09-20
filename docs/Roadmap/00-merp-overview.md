# MockERP — Mock Enterprise Resource Planner

## O que é

Com o intuito de estudar e aprofundar meus conhecimentos em Databricks, resolvi começar um projeto um pouco mais audacioso: o MERP, Mock Enterprise Resource Planner.

A ideia do MERP é criar um ambiente sintético que simule um ERP e que possa ser utilizado não apenas no desenvolvimento do projeto, mas também por outras pessoas que estejam estudando desenvolvimento, programação, engenharia de dados, análise de dados, BI e áreas relacionadas.

## Diferencial: erros controlados

Um dos principais objetivos é trabalhar com erros controlados. Em vez de disponibilizar apenas um dataset perfeito, a ideia é criar cenários em que os problemas possam ser reproduzidos propositalmente:

- Dados duplicados
- Inconsistências
- Registros faltantes
- Relacionamentos inválidos
- Alterações de estrutura
- Divergências entre documentos
- Outros problemas comuns em ambientes reais

## Ponto de partida

A v0.1 começa pelo núcleo comercial do MERP:

```
Orçamento → Venda → Devolução
```

## Evolução prevista

A partir dessa base, novas versões irão adicionar outros módulos:

- Movimentações de estoque
- Entradas e saídas
- Contas a receber
- Pagamentos
- Integração entre módulos
- Cenários de inconsistência e erro controlado

## Visão de produto

Com a evolução do projeto, a intenção é disponibilizar essa estrutura para que outras pessoas possam utilizá-la como um laboratório prático, criando seus próprios exercícios, pipelines, consultas, dashboards, análises e aplicações sobre uma base que simula problemas mais próximos dos encontrados em sistemas reais.

Esse documento é o ponto de entrada do projeto. Os demais arquivos deste conjunto detalham cada entrega, do núcleo comercial até a camada de plataforma de dados construída sobre o MERP.

## Mapa de entregas

| Arquivo | Entrega |
|---|---|
| `01-v0.1-nucleo-comercial.md` | Orçamento, Venda, Devolução |
| `02-v0.2-estoque.md` | Movimentações de estoque, entradas e saídas |
| `03-v0.3-financeiro.md` | Contas a receber e pagamentos |
| `04-v0.4-integracao-modulos.md` | Integração entre módulos |
| `05-v0.5-erro-controlado.md` | Cenários de inconsistência e erro controlado |
| `06-v1.0-plataforma-bronze.md` | Ingestão Bronze no Databricks |
| `07-v1.1-plataforma-silver.md` | Limpeza, deduplicação, integridade |
| `08-v1.2-plataforma-gold.md` | Métricas de negócio e reconciliação |
| `09-v1.3-plataforma-avancada.md` | Auto Loader, schema evolution, MERGE, SCD2, orquestração |
| `10-v2.0-lab-publico.md` | Documentação, dashboard final, abertura para uso externo |

MERP v0.1, núcleo comercial: Orçamento → Venda → Devolução. Esse é apenas o começo.
