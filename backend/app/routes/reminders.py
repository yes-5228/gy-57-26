from fastapi import APIRouter, Query

from app.models import ReminderStatus
from app.schemas import ReminderRead
from app.services.reminders import (
    get_reminder,
    list_reminders,
    list_upcoming_reminders,
    mark_reminder_read,
    mark_reminder_sent,
)

router = APIRouter()


@router.get("", response_model=list[ReminderRead])
def get_reminders(status: ReminderStatus | None = None) -> list[ReminderRead]:
    return list_reminders(status)


@router.get("/upcoming", response_model=list[ReminderRead])
def get_upcoming(hours_ahead: int = Query(default=24, ge=1, le=168)) -> list[ReminderRead]:
    return list_upcoming_reminders(hours_ahead)


@router.get("/{reminder_id}", response_model=ReminderRead)
def get_single_reminder(reminder_id: int) -> ReminderRead:
    return get_reminder(reminder_id)


@router.post("/{reminder_id}/send", response_model=ReminderRead)
def send_reminder(reminder_id: int) -> ReminderRead:
    return mark_reminder_sent(reminder_id)


@router.post("/{reminder_id}/read", response_model=ReminderRead)
def read_reminder(reminder_id: int) -> ReminderRead:
    return mark_reminder_read(reminder_id)
