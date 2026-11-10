"""Validador simplificado de NF-e (laboratório educacional, dados fictícios).

Não substitui a validação oficial da SEFAZ. Confere apenas regras básicas
que ajudam a entender por que uma nota pode ser rejeitada ou apresentar erro.
Uso:  python -m nfe_validator.validator nfe_validator/samples
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

CST_ICMS_VALIDOS = {"00", "10", "20", "30", "40", "41", "50", "51", "60", "70", "90"}
CST_SEM_ICMS = {"40", "41", "50"}
TOLERANCIA = Decimal("0.01")


@dataclass
class Achado:
    severidade: str  # ERRO ou AVISO
    codigo: str
    mensagem: str


def _local(tag: str) -> str:
    return tag.split("}")[-1]


def _filho(el: ET.Element, nome: str) -> ET.Element | None:
    for ch in el:
        if _local(ch.tag) == nome:
            return ch
    return None


def _caminho(el: ET.Element, caminho: str) -> ET.Element | None:
    atual: ET.Element | None = el
    for parte in caminho.split("/"):
        if atual is None:
            return None
        atual = _filho(atual, parte)
    return atual


def _texto(el: ET.Element, caminho: str) -> str | None:
    n = _caminho(el, caminho)
    return n.text.strip() if n is not None and n.text else None


def _dec(valor: str | None) -> Decimal | None:
    if valor is None:
        return None
    try:
        return Decimal(valor)
    except InvalidOperation:
        return None


def _arred(v: Decimal) -> Decimal:
    return v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def dv_chave(chave43: str) -> int:
    """Dígito verificador da chave de acesso (módulo 11, pesos de 2 a 9)."""
    pesos = [2, 3, 4, 5, 6, 7, 8, 9]
    soma = sum(int(d) * pesos[i % 8] for i, d in enumerate(reversed(chave43)))
    resto = soma % 11
    return 0 if resto in (0, 1) else 11 - resto


def validar_arquivo(caminho: Path) -> list[Achado]:
    achados: list[Achado] = []
    try:
        raiz = ET.parse(caminho).getroot()
    except ET.ParseError as e:
        return [Achado("ERRO", "XML", f"XML malformado: {e}")]

    inf = next((e for e in raiz.iter() if _local(e.tag) == "infNFe"), None)
    if inf is None:
        return [Achado("ERRO", "XML", "Elemento infNFe não encontrado")]

    chave = inf.get("Id", "").removeprefix("NFe")
    if len(chave) != 44 or not chave.isdigit():
        achados.append(Achado("ERRO", "CHAVE", "Chave de acesso deve ter 44 dígitos numéricos"))
    elif int(chave[43]) != dv_chave(chave[:43]):
        achados.append(Achado("ERRO", "CHAVE", "Dígito verificador da chave de acesso inválido"))

    uf_emit = _texto(inf, "emit/enderEmit/UF")
    uf_dest = _texto(inf, "dest/enderDest/UF")

    soma_vprod = Decimal("0")
    soma_vicms = Decimal("0")

    for det in (e for e in inf if _local(e.tag) == "det"):
        n = det.get("nItem", "?")
        ncm = _texto(det, "prod/NCM")
        cfop = _texto(det, "prod/CFOP")
        vprod = _dec(_texto(det, "prod/vProd"))
        qcom = _dec(_texto(det, "prod/qCom"))
        vun = _dec(_texto(det, "prod/vUnCom"))

        if not ncm or len(ncm) != 8 or not ncm.isdigit():
            achados.append(Achado("ERRO", "NCM", f"Item {n}: NCM deve ter 8 dígitos (recebido: {ncm})"))

        if not cfop or len(cfop) != 4 or not cfop.isdigit():
            achados.append(Achado("ERRO", "CFOP", f"Item {n}: CFOP deve ter 4 dígitos (recebido: {cfop})"))
        elif uf_emit and uf_dest:
            if cfop[0] == "5" and uf_emit != uf_dest:
                achados.append(Achado("ERRO", "CFOP", f"Item {n}: CFOP {cfop} é de operação interna, mas emitente ({uf_emit}) e destinatário ({uf_dest}) estão em UFs diferentes"))
            if cfop[0] == "6" and uf_emit == uf_dest:
                achados.append(Achado("ERRO", "CFOP", f"Item {n}: CFOP {cfop} é interestadual, mas emitente e destinatário estão na mesma UF ({uf_emit})"))

        if vprod is not None:
            soma_vprod += vprod
            if qcom is not None and vun is not None and abs(_arred(qcom * vun) - vprod) > TOLERANCIA:
                achados.append(Achado("ERRO", "VALOR", f"Item {n}: vProd ({vprod}) diferente de quantidade x valor unitário ({_arred(qcom * vun)})"))

        icms = _caminho(det, "imposto/ICMS")
        grupo = next(iter(icms), None) if icms is not None else None
        cst = _texto(grupo, "CST") if grupo is not None else None
        if cst not in CST_ICMS_VALIDOS:
            achados.append(Achado("ERRO", "CST", f"Item {n}: CST de ICMS inválido (recebido: {cst})"))
        else:
            vicms = _dec(_texto(grupo, "vICMS")) or Decimal("0")
            soma_vicms += vicms
            if cst == "00":
                vbc = _dec(_texto(grupo, "vBC"))
                p = _dec(_texto(grupo, "pICMS"))
                if vbc is None or p is None:
                    achados.append(Achado("ERRO", "ICMS", f"Item {n}: CST 00 exige vBC e pICMS"))
                elif abs(_arred(vbc * p / 100) - vicms) > TOLERANCIA:
                    achados.append(Achado("ERRO", "ICMS", f"Item {n}: vICMS ({vicms}) diferente de vBC x pICMS ({_arred(vbc * p / 100)})"))
            if cst in CST_SEM_ICMS and vicms > 0:
                achados.append(Achado("ERRO", "ICMS", f"Item {n}: CST {cst} não deve ter valor de ICMS"))

    tot = _caminho(inf, "total/ICMSTot")
    if tot is None:
        achados.append(Achado("ERRO", "TOTAL", "Grupo total/ICMSTot não encontrado"))
    else:
        t_vprod = _dec(_texto(tot, "vProd"))
        t_vdesc = _dec(_texto(tot, "vDesc")) or Decimal("0")
        t_vnf = _dec(_texto(tot, "vNF"))
        t_vicms = _dec(_texto(tot, "vICMS")) or Decimal("0")
        if t_vprod is not None and abs(t_vprod - soma_vprod) > TOLERANCIA:
            achados.append(Achado("ERRO", "TOTAL", f"vProd total ({t_vprod}) diferente da soma dos itens ({soma_vprod})"))
        if t_vprod is not None and t_vnf is not None and abs((t_vprod - t_vdesc) - t_vnf) > TOLERANCIA:
            achados.append(Achado("ERRO", "TOTAL", f"vNF ({t_vnf}) diferente de vProd - vDesc ({t_vprod - t_vdesc})"))
        if abs(t_vicms - soma_vicms) > TOLERANCIA:
            achados.append(Achado("ERRO", "TOTAL", f"vICMS total ({t_vicms}) diferente da soma dos itens ({soma_vicms})"))

    return achados


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Uso: python -m nfe_validator.validator <arquivo.xml | pasta>")
        return 2
    alvo = Path(argv[1])
    arquivos = sorted(alvo.glob("*.xml")) if alvo.is_dir() else [alvo]
    tem_erro = False
    for arq in arquivos:
        achados = validar_arquivo(arq)
        status = "OK" if not achados else "COM PROBLEMAS"
        print(f"\n== {arq.name}: {status}")
        for a in achados:
            print(f"   [{a.severidade}] {a.codigo}: {a.mensagem}")
            tem_erro = tem_erro or a.severidade == "ERRO"
    return 1 if tem_erro else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
