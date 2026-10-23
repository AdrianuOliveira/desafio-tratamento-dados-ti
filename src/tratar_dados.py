"""Tratamento e análise de chamados de suporte técnico (Python básico, sem bibliotecas externas)."""
import csv
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "chamados_originais.csv"
SAIDA_CSV = RAIZ / "resultados" / "chamados_tratados.csv"
SAIDA_REL = RAIZ / "resultados" / "relatorio_tratamento.txt"

STATUS = {"concluido": "Concluído", "pendente": "Pendente", "em andamento": "Em andamento"}
PRIORIDADES = {"baixa": "Baixa", "media": "Média", "alta": "Alta"}
SETORES = {"administrativo": "Administrativo", "atendimento": "Atendimento", "financeiro": "Financeiro",
           "logistica": "Logística", "rh": "RH", "vendas": "Vendas"}
TIPOS = {"impressora": "Impressora", "acesso ao sistema": "Acesso ao sistema",
         "rede/internet": "Rede/Internet", "computador lento": "Computador lento",
         "e-mail": "E-mail", "perifericos": "Periféricos"}
FORMATOS_DATA = ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y")


def chave(texto):
    """Minúsculas, sem acentos e sem espaços extras."""
    texto = unicodedata.normalize("NFKD", texto.strip().lower())
    return "".join(c for c in texto if not unicodedata.combining(c))


def padronizar(valor, tabela):
    return tabela.get(chave(valor))


def tratar_data(valor):
    for fmt in FORMATOS_DATA:
        try:
            return datetime.strptime(valor.strip(), fmt).strftime("%d/%m/%Y")
        except ValueError:
            continue
    return None


def tratar_tempo(valor):
    try:
        t = int(valor.strip())
    except ValueError:
        return None
    return t if t >= 0 else None


def main():
    with open(ENTRADA, encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))

    problemas = Counter()
    vistos_linha, vistos_id, tratados = set(), set(), []

    for l in linhas:
        bruto = tuple(l.values())
        if bruto in vistos_linha:
            problemas["Registros duplicados removidos"] += 1
            continue
        vistos_linha.add(bruto)

        id_ = l["ID"].strip()
        if id_ in vistos_id:
            problemas["IDs repetidos removidos"] += 1
            continue
        vistos_id.add(id_)

        novo = {"ID": id_}
        for campo, tabela, rotulo in (("Setor", SETORES, "Setores fora do padrão"),
                                      ("Tipo de problema", TIPOS, "Tipos fora do padrão"),
                                      ("Prioridade", PRIORIDADES, "Prioridades fora do padrão"),
                                      ("Status", STATUS, "Status fora do padrão")):
            padrao = padronizar(l[campo], tabela)
            if padrao != l[campo]:
                problemas[rotulo] += 1
            novo[campo] = padrao or "Não informado"

        data = tratar_data(l["Data"])
        if data != l["Data"]:
            problemas["Datas fora do padrão ou inválidas"] += 1
        novo["Data"] = data or ""

        tempo = tratar_tempo(l["Tempo de atendimento (min)"])
        if tempo is None:
            problemas["Tempos vazios ou inválidos"] += 1
        novo["Tempo de atendimento (min)"] = "" if tempo is None else tempo
        tratados.append(novo)

    colunas = ["ID", "Data", "Setor", "Tipo de problema", "Prioridade", "Status", "Tempo de atendimento (min)"]
    with open(SAIDA_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=colunas)
        w.writeheader()
        w.writerows(tratados)

    total = len(tratados)
    concl = [t for t in tratados if t["Status"] == "Concluído"]
    tempos = [t["Tempo de atendimento (min)"] for t in concl if t["Tempo de atendimento (min)"] != ""]
    media = sum(tempos) / len(tempos) if tempos else 0

    def top(campo):
        return Counter(t[campo] for t in tratados).most_common()

    rel = ["RELATÓRIO DE TRATAMENTO DE DADOS - CHAMADOS DE TI", "=" * 50,
           f"Registros lidos: {len(linhas)}", f"Registros após tratamento: {total}", "",
           "PROBLEMAS ENCONTRADOS E CORRIGIDOS"]
    rel += [f"- {k}: {v}" for k, v in problemas.items()] or ["- Nenhum"]
    rel += ["", "INDICADORES",
            f"Total de chamados: {total}",
            f"Concluídos: {len(concl)} ({len(concl) / total:.1%})",
            f"Tempo médio dos concluídos: {media:.1f} min", ""]
    for campo in ("Status", "Tipo de problema", "Setor", "Prioridade"):
        rel.append(f"CHAMADOS POR {campo.upper()}")
        rel += [f"- {nome}: {qtd}" for nome, qtd in top(campo)]
        rel.append("")
    texto = "\n".join(rel)
    SAIDA_REL.write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
