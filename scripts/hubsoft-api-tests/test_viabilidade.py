import pytest


def test_viabilidade_por_endereco(api):
    response = api.post(
        "/api/v1/integracao/mapeamento/viabilidade/consultar",
        json={
            "tipo_busca": "endereco",
            "raio": 250,
            "endereco": {
                "numero": "85",
                "endereco": "RUA JOSE JOAO",
                "bairro": "SAO GERALDO",
                "cidade": "Santo Antonio do Monte",
                "estado": "MG",
            },
            "detalhar_portas": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"


def test_viabilidade_por_coordenadas(api):
    response = api.post(
        "/api/v1/integracao/mapeamento/viabilidade/consultar",
        json={
            "tipo_busca": "coordenadas",
            "raio": 250,
            "latitude": -20.087333797519086,
            "longitude": -45.29056616400146,
            "detalhar_portas": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"


def test_viabilidade_sem_cobertura_nao_retorna_500(api):
    # coordenadas no meio do oceano — sem cobertura esperada
    response = api.post(
        "/api/v1/integracao/mapeamento/viabilidade/consultar",
        json={
            "tipo_busca": "coordenadas",
            "raio": 10,
            "latitude": 0.0,
            "longitude": 0.0,
            "detalhar_portas": False,
        },
    )
    assert response.status_code != 500
    data = response.json()
    assert isinstance(data, dict)
    assert "status" in data


def test_viabilidade_com_detalhar_portas(api):
    response = api.post(
        "/api/v1/integracao/mapeamento/viabilidade/consultar",
        json={
            "tipo_busca": "coordenadas",
            "raio": 250,
            "latitude": -20.087333797519086,
            "longitude": -45.29056616400146,
            "detalhar_portas": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
