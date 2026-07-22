
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ClaudeEventType(str, Enum):
    API_REQUEST = "claude_code.api_request"
    TOOL_DECISION = "claude_code.tool_decision"
    TOOL_RESULT = "claude_code.tool_result"
    USER_PROMPT = "claude_code.user_prompt"
    API_ERROR = "claude_code.api_error"


class ClaudeModel(str, Enum):
    CLAUDE_HAIKU_4_5_20251001 = "claude-haiku-4-5-20251001"
    CLAUDE_OPUS_4_6 = "claude-opus-4-6"
    CLAUDE_OPUS_4_5_20251101 = "claude-opus-4-5-20251101"
    CLAUDE_SONNET_4_5_20250929 = "claude-sonnet-4-5-20250929"
    CLAUDE_SONNET_4_6 = "claude-sonnet-4-6"


class ToolName(str, Enum):
    READ = "Read"
    BASH = "Bash"
    EDIT = "Edit"
    GREP = "Grep"
    GLOB = "Glob"
    MCP_TOOL = "mcp_tool"
    WRITE = "Write"
    TODO_WRITE = "TodoWrite"
    TASK_UPDATE = "TaskUpdate"
    TASK = "Task"
    TASK_CREATE = "TaskCreate"
    ASK_USER_QUESTION = "AskUserQuestion"
    WEB_FETCH = "WebFetch"
    TOOL_SEARCH = "ToolSearch"
    WEB_SEARCH = "WebSearch"
    NOTEBOOK_EDIT = "NotebookEdit"
    EXIT_PLAN_MODE = "ExitPlanMode"


class DecisionSource(str, Enum):
    CONFIG = "config"
    USER_TEMPORARY = "user_temporary"
    USER_PERMANENT = "user_permanent"
    USER_REJECT = "user_reject"


class DecisionType(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"


class EngineeringPractice(str, Enum):
    PLATFORM_ENGINEERING = "Platform Engineering"
    DATA_ENGINEERING = "Data Engineering"
    ML_ENGINEERING = "ML Engineering"
    BACKEND_ENGINEERING = "Backend Engineering"
    FRONTEND_ENGINEERING = "Frontend Engineering"


class SeniorityLevel(str, Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"
    L5 = "L5"
    L6 = "L6"
    L7 = "L7"
    L8 = "L8"
    L9 = "L9"
    L10 = "L10"


class Scope(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str = Field(..., description="Scope name")
    version: str = Field(..., description="Scope version")


class Resource(BaseModel):
    model_config = ConfigDict(frozen=True)
    host_arch: str = Field(..., alias="host.arch", description="Host architecture")
    host_name: str = Field(..., alias="host.name", description="Hostname")
    os_type: str = Field(..., alias="os.type", description="OS type")
    os_version: str = Field(..., alias="os.version", description="OS version")
    service_name: str = Field(..., alias="service.name", description="Service name")
    service_version: str = Field(..., alias="service.version", description="Service version")
    user_email: str = Field(..., alias="user.email", description="User email (redacted)")
    user_practice: EngineeringPractice = Field(..., alias="user.practice", description="User's practice")
    user_profile: str = Field(..., alias="user.profile", description="User profile")
    user_serial: str = Field(..., alias="user.serial", description="User serial number")


class BaseEventAttributes(BaseModel):
    model_config = ConfigDict(frozen=True)
    event_timestamp: str = Field(..., alias="event.timestamp", description="Event timestamp in ISO 8601")
    organization_id: str = Field(..., alias="organization.id", description="Organization ID")
    session_id: str = Field(..., alias="session.id", description="Session ID")
    terminal_type: str = Field(..., alias="terminal.type", description="Terminal type")
    user_account_uuid: str = Field(..., alias="user.account_uuid", description="User account UUID")
    user_email: str = Field(..., alias="user.email", description="User email")
    user_id: str = Field(..., alias="user.id", description="User ID")
    event_name: str = Field(..., alias="event.name", description="Event name")


class APIRequestAttributes(BaseEventAttributes):
    model_config = ConfigDict(frozen=True)
    cache_creation_tokens: Optional[str] = Field(None, alias="cache_creation_tokens")
    cache_read_tokens: Optional[str] = Field(None, alias="cache_read_tokens")
    cost_usd: str = Field(..., alias="cost_usd", description="Cost in USD")
    duration_ms: str = Field(..., alias="duration_ms", description="Duration in ms")
    input_tokens: str = Field(..., alias="input_tokens", description="Input tokens")
    model: ClaudeModel = Field(..., description="Model used")
    output_tokens: str = Field(..., alias="output_tokens", description="Output tokens")


class ToolDecisionAttributes(BaseEventAttributes):
    model_config = ConfigDict(frozen=True)
    decision: DecisionType = Field(..., description="Decision made")
    source: DecisionSource = Field(..., description="Source of decision")
    tool_name: ToolName = Field(..., description="Tool name")


class ToolResultAttributes(BaseEventAttributes):
    model_config = ConfigDict(frozen=True)
    decision_source: DecisionSource = Field(..., alias="decision_source", description="Decision source")
    decision_type: DecisionType = Field(..., alias="decision_type", description="Decision type")
    duration_ms: str = Field(..., alias="duration_ms", description="Duration in ms")
    success: str = Field(..., description="Success status (true/false)")
    tool_name: ToolName = Field(..., description="Tool name")
    tool_result_size_bytes: Optional[str] = Field(None, alias="tool_result_size_bytes", description="Result size in bytes")


class UserPromptAttributes(BaseEventAttributes):
    model_config = ConfigDict(frozen=True)
    prompt: str = Field(..., description="Prompt text (redacted)")
    prompt_length: str = Field(..., alias="prompt_length", description="Prompt length in chars")


class APIErrorAttributes(BaseEventAttributes):
    model_config = ConfigDict(frozen=True)
    attempt: str = Field(..., description="Attempt number")
    duration_ms: str = Field(..., alias="duration_ms", description="Duration in ms")
    error: str = Field(..., description="Error message")
    model: ClaudeModel = Field(..., description="Model used")
    status_code: str = Field(..., alias="status_code", description="HTTP status code")


class TelemetryEvent(BaseModel):
    model_config = ConfigDict(frozen=True)
    body: ClaudeEventType = Field(..., description="Event type")
    attributes: Dict[str, Any] = Field(..., description="Event attributes")
    scope: Scope = Field(..., description="Scope")
    resource: Resource = Field(..., description="Resource")


class Employee(BaseModel):
    model_config = ConfigDict(frozen=True)
    email: str = Field(..., description="Employee email")
    full_name: str = Field(..., description="Employee full name")
    practice: EngineeringPractice = Field(..., description="Engineering practice")
    level: SeniorityLevel = Field(..., description="Seniority level")
    location: str = Field(..., description="Employee location (country)")
