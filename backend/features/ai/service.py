from pydantic_ai import Agent

from backend.core.config import settings
from backend.features.ai.schema import ParsedTask
from backend.utilities.exceptions import BadRequestException


def get_task_parser() -> Agent:
    return Agent(
        settings.AI_MODEL,
        output_type=ParsedTask,
        instructions=(
            "Convert the user's productivity request into one task. "
            "Extract a concise title, useful description, status, priority, and due date. "
            "Use an ISO-8601 datetime with timezone when a date and time are present. "
            "If the user gives only a date, use the user's local date at 09:00. "
            "Keep category_name and tags as short names, and never invent a category or tag "
            "when none is suggested by the request."
        ),
    )


async def parse_task_text(text: str) -> ParsedTask:
    if not settings.OPENAI_API_KEY:
        raise BadRequestException("OPENAI_API_KEY is not configured")
    try:
        result = await get_task_parser().run(text)
        return result.output
    except Exception as exc:
        raise BadRequestException("Unable to parse task text") from exc