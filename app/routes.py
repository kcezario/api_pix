from fastapi import APIRouter, HTTPException
from typing import Optional
from .models import PixPayment
from .gateways.pix_factory import get_pix_gateway

router = APIRouter()

@router.post("/pay")
def pay_pix(
    payload: PixPayment,
    bank: str = "inter",
    account_number: Optional[str] = None
):
    """
    Process a Pix payment using the selected bank integration.
    Optional query param: account_number
    """
    try:
        gateway = get_pix_gateway(bank, account_number)
        result = gateway.process_payment(
            key=payload.key,
            amount=payload.amount,
            description=payload.description
        )
        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{transaction_id}")
def get_pix_status(
    transaction_id: str,
    bank: str = "inter",
    account_number: Optional[str] = None
):
    """
    Get the status of a Pix payment using the transaction ID (codigoSolicitacao).
    Optional query param: account_number
    """
    try:
        gateway = get_pix_gateway(bank, account_number)
        result = gateway.get_payment_status(transaction_id)
        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
