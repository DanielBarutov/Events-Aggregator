from fastapi import APIRouter, Depends
from usecases.create_ticket import TicketUsecase
from api.deps import get_tickets_usecase

router = APIRouter(tags=["tickets"])


@router.post("/tickets")
async def create_tickets(
    event_id: str,
    first_name: str,
    last_name: str,
    email: str,
    seat: str,
    usecase: TicketUsecase = Depends(get_tickets_usecase),
):
    return await usecase.create(event_id, first_name, last_name, email, seat)


@router.delete("/tickets/{ticket_id}")
async def delete_ticket(
    ticket_id: str,
    usecase: TicketUsecase = Depends(get_tickets_usecase),
):
    return await usecase.delete(ticket_id)
