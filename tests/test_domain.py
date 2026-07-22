
from datetime import datetime
from src.domain.models import (
    TelemetryEvent,
    Employee,
    ClaudeEventType,
    ClaudeModel,
    ToolName,
    EngineeringPractice,
    SeniorityLevel,
    Scope,
    Resource
)


def test_claude_event_type_enum():
    assert ClaudeEventType.API_REQUEST == "claude_code.api_request"
    assert ClaudeEventType.TOOL_DECISION == "claude_code.tool_decision"


def test_claude_model_enum():
    assert ClaudeModel.CLAUDE_HAIKU_4_5_20251001 == "claude-haiku-4-5-20251001"
    assert ClaudeModel.CLAUDE_OPUS_4_6 == "claude-opus-4-6"


def test_tool_name_enum():
    assert ToolName.READ == "Read"
    assert ToolName.BASH == "Bash"


def test_employee_creation():
    employee = Employee(
        email="test@example.com",
        full_name="Test User",
        practice=EngineeringPractice.DATA_ENGINEERING,
        level=SeniorityLevel.L3,
        location="USA"
    )
    assert employee.email == "test@example.com"
    assert employee.full_name == "Test User"
    assert employee.practice == EngineeringPractice.DATA_ENGINEERING
    assert employee.level == SeniorityLevel.L3
    assert employee.location == "USA"


def test_scope_creation():
    scope = Scope(name="test_scope", version="1.0.0")
    assert scope.name == "test_scope"
    assert scope.version == "1.0.0"


def test_resource_creation():
    resource = Resource(
        **{
            "host.arch": "x86_64",
            "host.name": "test-host",
            "os.type": "Linux",
            "os.version": "22.04",
            "service.name": "claude_code",
            "service.version": "1.0.0",
            "user.email": "test@example.com",
            "user.practice": EngineeringPractice.DATA_ENGINEERING,
            "user.profile": "developer",
            "user.serial": "12345"
        }
    )
    assert resource.host_arch == "x86_64"
    assert resource.host_name == "test-host"
    assert resource.os_type == "Linux"
    assert resource.os_version == "22.04"
    assert resource.user_email == "test@example.com"


def test_telemetry_event_creation():
    scope = Scope(name="test_scope", version="1.0.0")
    resource = Resource(
        **{
            "host.arch": "x86_64",
            "host.name": "test-host",
            "os.type": "Linux",
            "os.version": "22.04",
            "service.name": "claude_code",
            "service.version": "1.0.0",
            "user.email": "test@example.com",
            "user.practice": EngineeringPractice.DATA_ENGINEERING,
            "user.profile": "developer",
            "user.serial": "12345"
        }
    )
    
    event = TelemetryEvent(
        body=ClaudeEventType.API_REQUEST,
        attributes={
            "event.timestamp": "2026-01-01T00:00:00.000Z",
            "organization.id": "test_org",
            "session.id": "test_session",
            "terminal.type": "vscode",
            "user.account_uuid": "test_uuid",
            "user.email": "test@example.com",
            "user.id": "test_user",
            "event.name": "api_request",
            "input_tokens": "100",
            "output_tokens": "200",
            "cost_usd": "0.01",
            "duration_ms": "1000",
            "model": ClaudeModel.CLAUDE_HAIKU_4_5_20251001
        },
        scope=scope,
        resource=resource
    )
    assert event.body == ClaudeEventType.API_REQUEST
    assert event.attributes["event.name"] == "api_request"
    assert event.scope.name == "test_scope"
    assert event.resource.user_email == "test@example.com"

