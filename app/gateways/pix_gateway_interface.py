from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class PixGateway(ABC):
    client_id: str
    client_secret: str
    cert_path: str
    key_path: str
    token_url: str
    payment_url: str

    @abstractmethod
    def get_config(self) -> dict:
        pass

    @abstractmethod
    def get_access_token(self) -> str:
        pass

    @abstractmethod
    def process_payment(self, key: str, amount: float, description: str) -> dict:
        pass
