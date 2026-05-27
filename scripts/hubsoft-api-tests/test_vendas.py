import pytest


def test_planos_por_cep(api, hubsoft_env):
    response = api.get(
        "/api/v1/integracao/prospecto/create",
        params={"cep": hubsoft_env["test_cep"]},
    )
    assert response.status_code == 200
    data = response.json()
    # CEP sem cobertura retorna status error — isso é comportamento válido da API
    # Para validar planos reais, configure TEST_CEP com um CEP coberto pelo tenant
    if data.get("status") == "error":
        pytest.skip(f"CEP {hubsoft_env['test_cep']} sem cobertura neste tenant — ajuste TEST_CEP no .env")

    assert data.get("status") == "success"
    servicos = data.get("servicos", [])
    assert isinstance(servicos, list)
    assert len(servicos) >= 1, "Nenhum plano retornado para o CEP de teste"

    for plano in servicos:
        assert "id_servico" in plano
        assert "descricao" in plano or "nome" in plano
        assert "valor" in plano


def test_campos_plano(api, hubsoft_env):
    response = api.get(
        "/api/v1/integracao/prospecto/create",
        params={"cep": hubsoft_env["test_cep"]},
    )
    data = response.json()
    for plano in data.get("servicos", []):
        assert isinstance(plano["valor"], (int, float))
        assert plano["valor"] > 0


def test_cep_sem_cobertura_nao_retorna_500(api):
    response = api.get(
        "/api/v1/integracao/prospecto/create",
        params={"cep": "00000000"},
    )
    assert response.status_code != 500


def test_listar_crms(api):
    response = api.get("/api/v1/integracao/crm/all")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"


def test_criar_prospecto(api, hubsoft_env):
    """
    Cria prospecto real — execute apenas contra sandbox.
    """
    pytest.skip("Criação de prospecto: execute manualmente contra sandbox")

    planos_resp = api.get(
        "/api/v1/integracao/prospecto/create",
        params={"cep": hubsoft_env["test_cep"]},
    )
    planos = planos_resp.json().get("servicos", [])
    assert planos, "Sem planos para criar prospecto de teste"
    plano = planos[0]

    response = api.post(
        "/api/v1/integracao/prospecto",
        json={
            "cep": hubsoft_env["test_cep"],
            "servico": {"id_servico": plano["id_servico"], "valor": plano["valor"]},
            "cpf_cnpj": "68346567000158",
            "telefone": "37999999999",
            "nome_razaosocial": "Empresa Teste LTDA",
            "tipo_pessoa": "pj",
            "bairro": "Centro",
            "endereco": "Rua Teste",
            "numero": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "id_prospecto" in data
    assert "prospecto_servico" in data
