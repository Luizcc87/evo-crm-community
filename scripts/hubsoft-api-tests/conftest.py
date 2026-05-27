import os
import pytest
import httpx
from dotenv import load_dotenv

load_dotenv()


def _required_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Required env var not set: {key}")
    return value


@pytest.fixture(scope="session")
def hubsoft_env():
    return {
        "host": _required_env("HUBSOFT_HOST").rstrip("/"),
        "client_id": _required_env("HUBSOFT_CLIENT_ID"),
        "client_secret": _required_env("HUBSOFT_CLIENT_SECRET"),
        "username": _required_env("HUBSOFT_USERNAME"),
        "password": _required_env("HUBSOFT_PASSWORD"),
        "test_cpf_cnpj": _required_env("TEST_CPF_CNPJ"),
        "test_codigo_cliente": _required_env("TEST_CODIGO_CLIENTE"),
        "test_id_cliente_servico": _required_env("TEST_ID_CLIENTE_SERVICO"),
        "test_id_tipo_atendimento": _required_env("TEST_ID_TIPO_ATENDIMENTO"),
        "test_cep": _required_env("TEST_CEP"),
    }


@pytest.fixture(scope="session")
def hubsoft_token(hubsoft_env):
    response = httpx.post(
        f"{hubsoft_env['host']}/oauth/token",
        json={
            "grant_type": "password",
            "client_id": int(hubsoft_env["client_id"]),
            "client_secret": hubsoft_env["client_secret"],
            "username": hubsoft_env["username"],
            "password": hubsoft_env["password"],
        },
        timeout=30,
    )
    assert response.status_code == 200, f"Auth failed: {response.text}"
    data = response.json()
    assert "access_token" in data, "No access_token in auth response"
    return data["access_token"]


@pytest.fixture(scope="session")
def api(hubsoft_env, hubsoft_token):
    return httpx.Client(
        base_url=hubsoft_env["host"],
        headers={
            "Authorization": f"Bearer {hubsoft_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
