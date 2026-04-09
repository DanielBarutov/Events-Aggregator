from fastapi import APIRouter, Depends, status

from src.application.usecases.create_ticket import TicketUsecase
from src.presentation.deps import get_tickets_usecase
from src.presentation.shemas.tickets import TicketCreateRequest

router = APIRouter(tags=["tickets"])


@router.post(
    "/tickets",
    status_code=status.HTTP_201_CREATED,
)
async def create_tickets(
    request_data: TicketCreateRequest,
    usecase: TicketUsecase = Depends(get_tickets_usecase),
):
    return await usecase.create(
        event_id=request_data.event_id,
        first_name=request_data.first_name,
        last_name=request_data.last_name,
        email=request_data.email,
        seat=request_data.seat,
    )


@router.delete("/tickets/{ticket_id}")
async def delete_ticket(
    ticket_id: str,
    usecase: TicketUsecase = Depends(get_tickets_usecase),
):
    return await usecase.delete(ticket_id)
