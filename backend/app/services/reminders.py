from datetime import datetime, timedelta

from fastapi import HTTPException, status

from app.models import Reminder, ReminderStatus
from app.schemas import ReminderRead
from app.store import reminders


def reminder_to_read(reminder: Reminder) -> ReminderRead:
    return ReminderRead(
        id=reminder.id,
        appointment_id=reminder.appointment_id,
        student_id=reminder.student_id,
        student_name=reminder.student_name,
        coach_id=reminder.coach_id,
        coach_name=reminder.coach_name,
        car_no=reminder.car_no,
        start_time=reminder.start_time,
        end_time=reminder.end_time,
        status=reminder.status,
        created_at=reminder.created_at,
        sent_at=reminder.sent_at,
    )


def list_reminders(status_filter: ReminderStatus | None = None) -> list[ReminderRead]:
    values = sorted(reminders.values(), key=lambda item: item.start_time)
    if status_filter:
        values = [item for item in values if item.status == status_filter]
    return [reminder_to_read(item) for item in values]


def get_reminder(reminder_id: int) -> ReminderRead:
    reminder = reminders.get(reminder_id)
    if not reminder:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Reminder not found")
    return reminder_to_read(reminder)


def mark_reminder_sent(reminder_id: int) -> ReminderRead:
    reminder = reminders.get(reminder_id)
    if not reminder:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Reminder not found")
    reminder.status = ReminderStatus.sent
    reminder.sent_at = datetime.now()
    reminders[reminder.id] = reminder
    return reminder_to_read(reminder)


def mark_reminder_read(reminder_id: int) -> ReminderRead:
    reminder = reminders.get(reminder_id)
    if not reminder:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Reminder not found")
    reminder.status = ReminderStatus.read
    reminders[reminder.id] = reminder
    return reminder_to_read(reminder)


def list_upcoming_reminders(hours_ahead: int = 24) -> list[ReminderRead]:
    now = datetime.now()
    cutoff = now + timedelta(hours=hours_ahead)
    values = [
        item
        for item in reminders.values()
        if item.status != ReminderStatus.read and now <= item.start_time <= cutoff
    ]
    values.sort(key=lambda item: item.start_time)
    return [reminder_to_read(item) for item in values]
