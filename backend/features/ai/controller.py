from fastapi import APIRouter, Depends

from backend.core.dependencies import get_current_user
from backend.features.ai.schema import TaskParseRequest, TaskParseResponse
from backend.features.ai.service import parse_task_text
from backend.models.user import User


router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/tasks/parse", response_model=TaskParseResponse)
async def parse_task(data: TaskParseRequest, current_user: User = Depends(get_current_user)):
    return TaskParseResponse(
        input_text=data.text,
        task=await parse_task_text(data.text),
    )