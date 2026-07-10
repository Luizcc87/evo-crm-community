import pytest


def test_listar_cpes(api):
    # endpoint requer pagina e itens_por_pagina obrigatórios
    response = api.get("/api/v1/integracao/rede/cpe/todos", params={"pagina": 0, "itens_por_pagina": 10})
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_listar_cpes_estrutura_paginacao(api):
    response = api.get("/api/v1/integracao/rede/cpe/todos", params={"pagina": 0, "itens_por_pagina": 10})
    data = response.json()
    # se houver paginação, validar estrutura base-zero
    if "paginacao" in data:
        pag = data["paginacao"]
        assert "primeira_pagina" in pag
        assert pag["primeira_pagina"] == 0
        assert "ultima_pagina" in pag
        assert "total_registros" in pag


def test_reiniciar_cpe_requer_phy_addr(api):
    """
    Reiniciar CPE com phy_addr inválido — HubSoft retorna 200 com status error.
    Valida que a API responde sem crash (não 500) e retorna json com status.
    """
    response = api.post("/api/v1/integracao/rede/reiniciar_cpe/00-00-00-00-00-00")
    assert response.status_code != 500
    data = response.json()
    assert "status" in data


def test_gerenciar_cpe_requer_id_valido(api):
    """
    Gerenciar CPE com id_cpe inexistente deve retornar 4xx ou error de negócio, não 500.
    Não altera configuração real.
    """
    response = api.post(
        "/api/v1/integracao/rede/cpe/gerenciar",
        json={
            "id_cpe": 0,
            "parametros": [{"prefixo": "wifi_ssid", "valor": "TesteEvo"}],
        },
    )
    assert response.status_code != 500
    data = response.json()
    assert isinstance(data, dict)
    assert "status" in data
