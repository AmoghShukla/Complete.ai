import asyncio
import logging

from backend.core.session import async_session
from backend.features.reminders.repository import ReminderRepository
from datetime import datetime, timezone


logger = logging.getLogger(__name__)


async def process_due_reminders() -> int:
    processed = 0
    async with async_session() as db:
        reminders = await ReminderRepository.get_due(db, datetime.now(timezone.utc))
        for reminder in reminders:
            logger.info(
                "Processing %s reminder %s for task %s",
                reminder.reminder_type.value,
                reminder.reminder_id,
                reminder.task_id,
            )
            await ReminderRepository.mark_sent(reminder, db)
            processed += 1
    return processed


async def reminder_worker(stop_event: asyncio.Event, poll_interval: int = 30) -> None:
    while not stop_event.is_set():
        try:
            await process_due_reminders()
        except Exception:
            logger.exception("Reminder worker iteration failed")
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=poll_interval)
        except asyncio.TimeoutError:
            continue