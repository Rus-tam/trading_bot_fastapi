import httpx


async def fetch_bybit_data(endpoint: str, params: dict):
    async with httpx.AsyncClient() as client:
        url = f"https://api.bybit.com/{endpoint}"

        try:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            result = response.json()
            return result["result"]

        except httpx.RequestError as e:
            return {"error": f"Request failed: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {str(e)}"}
