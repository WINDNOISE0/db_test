import httpx


class PaymentClient:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def health(self) -> httpx.Response:
        return self._client.get("/health")

    def version(self) -> httpx.Response:
        return self._client.get("/version")

    def close(self) -> None:
        self._client.close()