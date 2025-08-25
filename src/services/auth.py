import requests
from src.services.interfaces import IAuthorizerService

class AuthorizerService(IAuthorizerService):
    def __init__(self, base_url: str = "https://util.devi.tools/api/v2/authorize"):
        self.base_url = base_url

    def is_authorized(self) -> bool:
        response = requests.get(self.base_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("authorization", False)