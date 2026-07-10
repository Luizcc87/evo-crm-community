import httpx
import pytest


def test_auth_success(hubsoft_env, hubsoft_token):
    assert hubsoft_token, "Token deve ser string não vazia"
    assert isinstance(hubsoft_token, str)


def test_auth_response_fields(hubsoft_env):
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
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"].lower() == "bearer"
    assert "expires_in" in data
    assert int(data["expires_in"]) > 0


def test_auth_invalid_credentials(hubsoft_env):
    response = httpx.post(
        f"{hubsoft_env['host']}/oauth/token",
        json={
            "grant_type": "password",
            "client_id": hubsoft_env["client_id"],
            "client_secret": "wrong-secret",
            "username": hubsoft_env["username"],
            "password": "wrong-password",
        },
        timeout=30,
    )
    assert response.status_code in (400, 401), (
        f"Credenciais inválidas devem retornar 400 ou 401, got {response.status_code}"
    )
