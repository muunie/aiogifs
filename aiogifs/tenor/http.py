import aiohttp
from typing import Optional


class Route:
    BASE = "https://g.tenor.com/v1"
    def __init__(self, endpoint: str, params: dict, method: str = "GET", **kwargs):
        self.method = method
        self.endpoint = endpoint
        self.url = self.BASE + endpoint.format(**kwargs)
        self.params = params



class HTTPClient:
    def __init__(self, *, api_key: Optional[str] = None):
        self.__session = None
        self._auth = api_key
    
    async def open_session(self):
        self.__session = aiohttp.ClientSession()

    async def request(self, route: Route) -> dict:
        if self._auth and route.params.get("key") is None:
            route.params.update(key = self._auth)
        async with self.__session.request(route.method, route.url, params = route.params) as resp:
            data = await resp.json()
        return data

    async def cleanup(self):
        await self.__session.close()
        self.__session = None
    
