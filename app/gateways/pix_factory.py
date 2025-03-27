from .inter_pix_gateway import InterPixGateway
from .mock_pix_gateway import MockPixGateway
from .pix_gateway_interface import PixGateway

def get_pix_gateway(bank: str = "inter") -> PixGateway:
    bank = bank.lower()

    if bank == "inter":
        return InterPixGateway()
    elif bank == "mock":
        return MockPixGateway()
    else:
        raise ValueError(f"Banco '{bank}' não suportado. Use 'inter' ou 'mock'.")
