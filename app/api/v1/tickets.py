from fastapi import APIRouter, Depends, status
from usecases.create_ticket import TicketUsecase
from api.deps import get_tickets_usecase
from shemas.tickets import TicketCreateResponse, TicketDeleteResponse

router = APIRouter(tags=["tickets"])


@router.post(
    "/tickets", status_code=status.HTTP_201_CREATED, response_model=TicketCreateResponse
)
async def create_tickets(
    event_id: str,
    first_name: str,
    last_name: str,
    email: str,
    seat: str,
    usecase: TicketUsecase = Depends(get_tickets_usecase),
):
    print("При создании тикета указано:", event_id, first_name, last_name, email, seat)
    return await usecase.create(event_id, first_name, last_name, email, seat)


@router.delete("/tickets/{ticket_id}")
async def delete_ticket(
    ticket_id: str,
    usecase: TicketUsecase = Depends(get_tickets_usecase),
):
    print("При удаление тикета:", ticket_id)
    return await usecase.delete(ticket_id)
