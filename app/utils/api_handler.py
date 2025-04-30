import httpx

import httpx


class _Request:
    def __init__(self, base_url: str = "", headers: dict = None, timeout: int = 10):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
        )

    async def get(self, endpoint: str, params: dict = None) -> dict:
        resp = await self.client.get(endpoint, params=params)
        resp.raise_for_status()
        return resp.json()

    async def post(self, endpoint: str, json: dict = None, data: dict = None) -> dict:
        resp = await self.client.post(endpoint, json=json, data=data)
        resp.raise_for_status()
        return resp.json()

    async def put(self, endpoint: str, json: dict = None) -> dict:
        resp = await self.client.put(endpoint, json=json)
        resp.raise_for_status()
        return resp.json()

    async def delete(self, endpoint: str) -> dict:
        resp = await self.client.delete(endpoint)
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
