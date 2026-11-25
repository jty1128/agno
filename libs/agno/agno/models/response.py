from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from time import time
from typing import Any, Optional

from agno.media import AudioResponse, ImageArtifact
from agno.models.message import Citations, MessageMetrics
from agno.tools.function import UserInputField


class ModelResponseEvent(str, Enum):
    """Events that can be sent by the model provider"""

    tool_call_paused = "ToolCallPaused"
    tool_call_started = "ToolCallStarted"
    tool_call_completed = "ToolCallCompleted"
    assistant_response = "AssistantResponse"


@dataclass
class ToolExecution:
    """Execution of a tool"""

    tool_call_id: Optional[str] = None
    tool_name: Optional[str] = None
    tool_args: Optional[dict[str, Any]] = None
    tool_call_error: Optional[bool] = None
    result: Optional[str] = None
    metrics: Optional[MessageMetrics] = None

    # If True, the agent will stop executing after this tool call.
    stop_after_tool_call: bool = False

    created_at: int = int(time())

    requires_confirmation: Optional[bool] = None
    confirmed: Optional[bool] = None
    confirmation_note: Optional[str] = None

    requires_user_input: Optional[bool] = None
    user_input_schema: Optional[list[UserInputField]] = None

    external_execution_required: Optional[bool] = None

    @property
    def is_paused(self) -> bool:
        return bool(self.requires_confirmation or self.requires_user_input or self.external_execution_required)

    def to_dict(self) -> dict[str, Any]:
        _dict = asdict(self)
        if self.metrics is not None:
            _dict["metrics"] = self.metrics._to_dict()

        if self.user_input_schema is not None:
            _dict["user_input_schema"] = [field.to_dict() for field in self.user_input_schema]

        return _dict

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ToolExecution:
        return cls(
            tool_call_id=data.get("tool_call_id"),
            tool_name=data.get("tool_name"),
            tool_args=data.get("tool_args"),
            tool_call_error=data.get("tool_call_error"),
            result=data.get("result"),
            stop_after_tool_call=data.get("stop_after_tool_call", False),
            requires_confirmation=data.get("requires_confirmation"),
            confirmed=data.get("confirmed"),
            confirmation_note=data.get("confirmation_note"),
            requires_user_input=data.get("requires_user_input"),
            user_input_schema=[UserInputField.from_dict(field) for field in data.get("user_input_schema", [])],
            external_execution_required=data.get("external_execution_required"),
            metrics=MessageMetrics(**data.get("metrics", {})),
        )


@dataclass
class ModelResponse:
    """Response from the model provider"""

    role: Optional[str] = None

    content: Optional[str] = None
    parsed: Optional[Any] = None
    audio: Optional[AudioResponse] = None
    image: Optional[ImageArtifact] = None

    # Model tool calls
    tool_calls: list[dict[str, Any]] = field(default_factory=list)

    # Actual tool executions
    tool_executions: Optional[list[ToolExecution]] = field(default_factory=list)

    event: str = ModelResponseEvent.assistant_response.value

    provider_data: Optional[dict[str, Any]] = None

    thinking: Optional[str] = None
    redacted_thinking: Optional[str] = None
    reasoning_content: Optional[str] = None

    citations: Optional[Citations] = None

    response_usage: Optional[Any] = None

    created_at: int = int(time())

    extra: Optional[dict[str, Any]] = None


class FileType(str, Enum):
    MP4 = "mp4"
    GIF = "gif"
    MP3 = "mp3"
