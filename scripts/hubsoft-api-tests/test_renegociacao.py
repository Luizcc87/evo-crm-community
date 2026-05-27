import pytest
from datetime import date, timedelta


def _vencimento_futuro() -> str:
    return (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")


def test_listar_renegociacoes(api):
    response = api.get(
        "/api/v1/integracao/financeiro/renegociacao",
        params={
            "pagina": 0,
            "itens_por_pagina": 10,
            "data_inicio": "2024-01-01",
            "data_fim": "2026-12-31",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"
    if "paginacao" in data:
        pag = data["paginacao"]
        assert pag["primeira_pagina"] == 0
        assert "ultima_pagina" in pag
        assert "total_registros" in pag


def test_listar_cobranca_avulsa(api):
    response = api.get(
        "/api/v1/integracao/financeiro/cobranca/cobranca_avulsa",
        params={
            "pagina": 0,
            "itens_por_pagina": 10,
            "tipo_data": "data_vencimento",
            "data_inicio": "2024-01-01",
            "data_fim": "2026-12-31",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"


def test_simular_renegociacao(api, hubsoft_env):
    """
    Simula renegociação com ids_faturas fictícios.
    API revelou: tipo_dados_cliente aceita "codigo_cliente" ou "id_cliente" (não "cpf_cnpj").
    Espera erro de negócio (status error) ou sucesso — nunca 500.
    Para teste real, substitua ids_faturas por IDs de faturas pendentes do tenant.
    """
    response = api.post(
        "/api/v1/integracao/financeiro/renegociacao/simular",
        json={
            "vencimento": _vencimento_futuro(),
            "faturas": "definir_faturas",
            "quantidade_parcelas": 2,
            "ids_faturas": [999999998, 999999999],
            "tipo_dados_cliente": "codigo_cliente",
            "dado_cliente": hubsoft_env["test_codigo_cliente"],
        },
    )
    assert response.status_code != 500
    data = response.json()
    assert "status" in data or "errors" in data or "msg" in data


def test_efetivar_renegociacao_sandbox_only(api, hubsoft_env):
    """
    Efetivar renegociação cria registro real — execute apenas contra sandbox.
    """
    pytest.skip("Efetivar renegociação: execute manualmente contra sandbox")

    response = api.post(
        "/api/v1/integracao/financeiro/renegociacao/efetivar",
        json={
            "vencimento": _vencimento_futuro(),
            "faturas": "definir_faturas",
            "quantidade_parcelas": 2,
            "ids_faturas": [999999998, 999999999],
            "tipo_dados_cliente": "cpf_cnpj",
            "documento_cliente": hubsoft_env["test_cpf_cnpj"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"
