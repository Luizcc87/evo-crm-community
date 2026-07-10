import pytest


def test_busca_por_cpf_cnpj(api, hubsoft_env):
    response = api.get(
        "/api/v1/integracao/cliente",
        params={
            "busca": "cpf_cnpj",
            "termo_busca": hubsoft_env["test_cpf_cnpj"],
            "limit": 5,
            "cancelado": "nao",
            "ultima_conexao": "sim",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"
    clientes = data.get("clientes", [])
    assert len(clientes) >= 1, "Deve retornar ao menos um cliente para o CPF/CNPJ de teste"

    cliente = clientes[0]
    assert "id_cliente" in cliente
    assert "nome_razaosocial" in cliente
    assert "cpf_cnpj" in cliente
    assert "servicos" in cliente

    for servico in cliente["servicos"]:
        assert "id_cliente_servico" in servico
        assert "status_prefixo" in servico


def test_busca_por_codigo_cliente(api, hubsoft_env):
    response = api.get(
        "/api/v1/integracao/cliente",
        params={
            "busca": "codigo_cliente",
            "termo_busca": hubsoft_env["test_codigo_cliente"],
            "limit": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"


def test_busca_cpf_inexistente_nao_retorna_500(api):
    response = api.get(
        "/api/v1/integracao/cliente",
        params={
            "busca": "cpf_cnpj",
            "termo_busca": "00000000000",
            "limit": 1,
        },
    )
    assert response.status_code != 500, "CPF inexistente não deve causar erro 500"
    data = response.json()
    clientes = data.get("clientes", [])
    assert isinstance(clientes, list)


def test_cliente_com_ultima_conexao(api, hubsoft_env):
    response = api.get(
        "/api/v1/integracao/cliente",
        params={
            "busca": "cpf_cnpj",
            "termo_busca": hubsoft_env["test_cpf_cnpj"],
            "ultima_conexao": "sim",
            "limit": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    clientes = data.get("clientes", [])
    if clientes:
        for servico in clientes[0].get("servicos", []):
            if "ultima_conexao" in servico:
                uc = servico["ultima_conexao"]
                assert "conectado" in uc
