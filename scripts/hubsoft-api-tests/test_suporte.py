import pytest


def test_listar_atendimentos_do_cliente(api, hubsoft_env):
    response = api.get(
        "/api/v1/integracao/cliente/atendimento",
        params={
            "busca": "cpf_cnpj",
            "termo_busca": hubsoft_env["test_cpf_cnpj"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"


def test_listar_os_do_cliente(api, hubsoft_env):
    response = api.get(
        "/api/v1/integracao/cliente/ordem_servico",
        params={
            "busca": "cpf_cnpj",
            "termo_busca": hubsoft_env["test_cpf_cnpj"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"


def test_extrato_conexao(api, hubsoft_env):
    response = api.get(
        "/api/v1/integracao/cliente/extrato_conexao",
        params={
            "busca": "id_cliente_servico",
            "termo_busca": hubsoft_env["test_id_cliente_servico"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert isinstance(data, dict)


def test_abrir_atendimento_com_os(api, hubsoft_env):
    """
    Abre protocolo real — execute apenas contra sandbox.
    Em produção, comente o skip somente quando autorizado.
    """
    pytest.skip("Abertura de atendimento: execute manualmente contra sandbox")

    response = api.post(
        "/api/v1/integracao/atendimento",
        json={
            "id_cliente_servico": hubsoft_env["test_id_cliente_servico"],
            "id_tipo_atendimento": int(hubsoft_env["test_id_tipo_atendimento"]),
            "descricao": "Teste automatizado — validação de integração Evo CRM.",
            "nome": "Cliente Teste",
            "telefone": "37999999999",
            "email": "teste@example.com",
            "abrir_os": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "protocolo" in data
    assert "id_atendimento" in data
    assert "ordens_servico" in data
    assert len(data["ordens_servico"]) > 0
