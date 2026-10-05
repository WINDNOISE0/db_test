def test_payments_health(payment_client):
    response = payment_client.health()

    assert response.status_code == 200, response.text

    response_dct = response.json()
    assert response_dct["status"] == "ok", response.text


def test_version(payment_client):
    response = payment_client.version()

    assert response.status_code == 200, response.text

    response_dct = response.json()

    assert "version" in response_dct
    assert isinstance(response_dct["version"], str) and response_dct["version"], response.text
