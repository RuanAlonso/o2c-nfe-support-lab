# o2c-nfe-support-lab

[![tests](https://github.com/RuanAlonso/o2c-nfe-support-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/RuanAlonso/o2c-nfe-support-lab/actions/workflows/tests.yml)

Laboratório de estudo para suporte de sistemas ERP no processo **Order-to-Cash** (pedido → remessa → faturamento → NF-e).
Reúne três coisas: um mini banco em PostgreSQL com problemas comuns, um validador simplificado de NF-e em Python e runbooks de atendimento.

> **Aviso:** este é um projeto educacional e **não é SAP** nem usa código ou material do SAP. É uma simulação simplificada,
> inspirada nos processos comuns de ERP. Todos os dados (clientes, notas, chaves) são **fictícios**.
> Os códigos de rejeição de NF-e são exemplos: confirme sempre na tabela oficial da SEFAZ.

## O que tem aqui

| Pasta | Conteúdo |
|---|---|
| `sql/` | Esquema, dados fictícios e 6 consultas de investigação de incidentes |
| `nfe_validator/` | Validador de NF-e em Python (NCM, CFOP, CST, ICMS, totais, dígito verificador da chave) e XMLs de exemplo |
| `runbooks/` | 4 guias de atendimento: sintoma, causa provável, análise, resolução e escalonamento |
| `tests/` | Testes automatizados (pytest) e CI no GitHub Actions |

## Como rodar

### Banco de dados (PostgreSQL)
```bash
createdb o2c_lab
psql -d o2c_lab -f sql/01_schema.sql
psql -d o2c_lab -f sql/02_seed.sql
psql -d o2c_lab -f sql/03_support_queries.sql
```

Os dados trazem problemas propositais, um por consulta:

| Consulta | O que encontra | Resultado esperado |
|---|---|---|
| Q1 | Pedido aberto sem remessa há mais de 3 dias | Pedido 4 |
| Q2 | Remessa sem faturamento | Remessa 4 (pedido 5) |
| Q3 | Valor da fatura diferente do pedido | Pedido 6: 200,00 contra 190,00 |
| Q4 | NF-e rejeitada ou pendente | Pedido 7 (rejeição 778) e pedido 9 (pendente) |
| Q5 | CFOP incompatível com a UF do cliente | Pedido 7 (CFOP 6102 para cliente de SP) |
| Q6 | Pedido bloqueado | Pedido 8 (limite de crédito) |

### Validador de NF-e
```bash
python -m nfe_validator.validator nfe_validator/samples
```

Exemplo de saída:
```text
== nfe_cfop_errado.xml: COM PROBLEMAS
   [ERRO] CFOP: Item 1: CFOP 6102 é interestadual, mas emitente e destinatário estão na mesma UF (SP)

== nfe_ok.xml: OK

== nfe_total_divergente.xml: COM PROBLEMAS
   [ERRO] TOTAL: vNF (190.00) diferente de vProd - vDesc (200.00)
```

### Testes
```bash
pip install -r requirements.txt
pytest
```

## Limitações
- O XML das amostras é simplificado e não substitui a validação oficial (schema e assinatura) da SEFAZ.
- Só cobre ICMS básico (CST 00 e CSTs sem imposto). IPI, PIS, COFINS e ICMS-ST ficam para as próximas versões.

## Próximos passos
- [ ] Validar PIS e COFINS
- [ ] Tratar ICMS-ST
- [ ] Gerar relatório em CSV
- [ ] Novos runbooks (devolução, intercompany)

## Licença
MIT
