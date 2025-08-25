import requests
from src.services.interfaces import INotifyService

class NotifyService(INotifyService):
    def __init__(self, base_url: str = "https://util.devi.tools/api/v1/notify"):
        self.base_url = base_url
    
    def notify(self, message: str) -> None:
        response = requests.post(self.base_url, json={"message": message}, timeout=5)
        response.raise_for_status()
        return response.json()