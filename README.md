# Desafio 01 – Tratamento de Dados: Chamados de Suporte Técnico de TI

Projeto complementar à planilha do Google Sheets. A planilha é a entrega principal;
este repositório mostra como o **tratamento dos dados pode ser automatizado com Python básico**.

## O problema
Registros de chamados costumam vir com inconsistências: status escritos de formas diferentes,
datas em vários formatos, tempos vazios e registros duplicados. Isso distorce contagens e médias.

## O que o script faz (`src/tratar_dados.py`)
1. Lê `dados/chamados_originais.csv`: os mesmos 40 chamados da planilha, mas com **erros de digitação inseridos de propósito** (maiúsculas/minúsculas, espaços, datas em formatos diferentes) e 2 registros repetidos.
2. Remove registros duplicados e IDs repetidos.
3. Padroniza setor, tipo de problema, prioridade e status (maiúsculas, acentos, espaços).
4. Converte datas para `DD/MM/AAAA` e marca datas inválidas como vazias.
5. Valida o tempo de atendimento (vazio, negativo ou texto → vazio).
6. Gera `resultados/chamados_tratados.csv` e `resultados/relatorio_tratamento.txt`
   com os problemas corrigidos e os indicadores (total, % concluído, tempo médio, rankings).

## Como executar
Requer Python 3.8+ e nenhuma biblioteca externa.

```bash
python src/tratar_dados.py
```

## Estrutura
```
desafio-tratamento-dados-ti/
├── dados/
│   ├── chamados_originais.csv   (com erros intencionais)
│   └── chamados_planilha.csv    (referência: exportação da planilha)
├── src/tratar_dados.py
├── resultados/
│   ├── chamados_tratados.csv
│   └── relatorio_tratamento.txt
└── README.md
```

## Resultados (idênticos à planilha e à apresentação)
Após o tratamento, `chamados_tratados.csv` fica igual aos dados da aba *Chamados* da planilha:

| Indicador | Resultado |
|---|---|
| Total de chamados | 40 |
| Concluídos / Pendentes / Em andamento | 28 / 5 / 7 |
| Percentual concluído | 70% |
| Tempo médio dos concluídos | 53,2 min |
| Tipo mais frequente | Computador lento (9) |
| Setor com mais chamados | Financeiro (12) |

## Relação com a planilha
Os mesmos indicadores (total, concluídos, tempo médio, tipo mais frequente) são calculados
no Google Sheets com `CONT.VALORES`, `CONT.SE` e `MÉDIASE`.
Link da planilha: _(cole aqui)_ · Apresentação: _(cole aqui)_

## Observação
Todos os dados são fictícios.

## Próximos passos
Usar `pandas`, gerar gráficos e adicionar testes automatizados.
