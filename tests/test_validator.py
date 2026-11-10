from pathlib import Path

from nfe_validator.validator import dv_chave, validar_arquivo

AMOSTRAS = Path(__file__).resolve().parent.parent / "nfe_validator" / "samples"


def codigos(nome):
    return {a.codigo for a in validar_arquivo(AMOSTRAS / nome)}


def test_nota_correta_nao_tem_achados():
    assert validar_arquivo(AMOSTRAS / "nfe_ok.xml") == []


def test_cfop_interestadual_para_cliente_da_mesma_uf():
    assert "CFOP" in codigos("nfe_cfop_errado.xml")


def test_total_da_nota_divergente():
    achados = validar_arquivo(AMOSTRAS / "nfe_total_divergente.xml")
    assert any(a.codigo == "TOTAL" and "vNF" in a.mensagem for a in achados)


def test_ncm_cst_e_chave_invalidos():
    assert {"NCM", "CST", "CHAVE"} <= codigos("nfe_ncm_cst_chave_invalidos.xml")


def test_digito_verificador_esta_entre_0_e_9():
    base = "3526101111111111111155001000000123112345678"
    assert dv_chave(base) in range(10)
