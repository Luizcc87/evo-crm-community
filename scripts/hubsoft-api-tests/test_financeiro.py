import pytest


def test_faturas_por_id_cliente_servico(api, hubsoft_env):
    response = api.get(
        "/api/v1/integracao/cliente/financeiro",
        params={
            "busca": "id_cliente_servico",
            "termo_busca": hubsoft_env["test_id_cliente_servico"],
            "apenas_pendente": "sim",
            "limit": 10,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"
    assert "faturas" in data
    assert isinstance(data["faturas"], list)


def test_fatura_campos_pagamento(api, hubsoft_env):
    response = api.get(
        "/api/v1/integracao/cliente/financeiro",
        params={
            "busca": "id_cliente_servico",
            "termo_busca": hubsoft_env["test_id_cliente_servico"],
            "limit": 5,
        },
    )
    assert response.status_code == 200
    data = response.json()
    faturas = data.get("faturas", [])

    for fatura in faturas:
        assert "id_fatura" in fatura
        assert "valor" in fatura
        assert "data_vencimento" in fatura
        # ao menos um método de pagamento deve estar presente
        tem_pagamento = any(
            k in fatura for k in ("linha_digitavel", "pix_copia_cola", "link")
        )
        assert tem_pagamento, f"Fatura {fatura.get('id_fatura')} sem campo de pagamento"


def test_fatura_pendente_sem_data_pagamento(api, hubsoft_env):
    response = api.get(
        "/api/v1/integracao/cliente/financeiro",
        params={
            "busca": "id_cliente_servico",
            "termo_busca": hubsoft_env["test_id_cliente_servico"],
            "apenas_pendente": "sim",
            "limit": 10,
        },
    )
    data = response.json()
    for fatura in data.get("faturas", []):
        assert fatura.get("data_pagamento") is None, (
            f"Fatura pendente {fatura.get('id_fatura')} tem data_pagamento preenchida"
        )


def test_desbloqueio_confianca_payload(api, hubsoft_env):
    """
    Valida apenas o shape da resposta — não executa desbloqueio real em tenant produção.
    Comente o skip e ajuste TEST_ID_CLIENTE_SERVICO para rodar contra sandbox.
    """
    pytest.skip("Desbloqueio em confiança: execute manualmente contra sandbox")

    response = api.post(
        "/api/v1/integracao/cliente/desbloqueio_confianca",
        json={
            "id_cliente_servico": hubsoft_env["test_id_cliente_servico"],
            "dias_desbloqueio": "1",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"
