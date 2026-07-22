
import json
import csv
from typing import List, Tuple, Dict, Any
import os
from src.domain.models import (
    TelemetryEvent,
    Employee,
    ClaudeEventType,
    Scope,
    Resource
)


class JSONLIngestor:
    """Ingest telemetry from telemetry_logs.jsonl and employees.csv"""

    def __init__(self):
        pass

    def _parse_resource(self, resource_dict: Dict[str, Any]) -> Resource:
        """Parse resource from dict using alias handling"""
        return Resource(
            **{
                "host.arch": resource_dict.get("host.arch"),
                "host.name": resource_dict.get("host.name"),
                "os.type": resource_dict.get("os.type"),
                "os.version": resource_dict.get("os.version"),
                "service.name": resource_dict.get("service.name"),
                "service.version": resource_dict.get("service.version"),
                "user.email": resource_dict.get("user.email", ""),
                "user.practice": resource_dict.get("user.practice"),
                "user.profile": resource_dict.get("user.profile"),
                "user.serial": resource_dict.get("user.serial"),
            }
        )

    def _parse_scope(self, scope_dict: Dict[str, Any]) -> Scope:
        return Scope(**scope_dict)

    def ingest_telemetry_logs(self, jsonl_path: str) -> Tuple[List[TelemetryEvent], List[str]]:
        """Ingest telemetry_logs.jsonl (which contains log batches with logEvents), returns events and errors"""
        events: List[TelemetryEvent] = []
        errors: List[str] = []

        if not os.path.exists(jsonl_path):
            return [], [f"File not found: {jsonl_path}"]

        with open(jsonl_path, "r", encoding="utf-8") as f:
            line_num = 0
            for line in f:
                line_num += 1
                line = line.strip()
                if not line:
                    continue

                try:
                    # Each line is a log batch
                    batch = json.loads(line)
                    log_events = batch.get("logEvents", [])
                    if not log_events:
                        continue

                    for log_event in log_events:
                        try:
                            # The "message" in log_event is a JSON string, parse it
                            message_str = log_event.get("message")
                            if not message_str:
                                errors.append(f"Line {line_num}: log event missing 'message'")
                                continue

                            message = json.loads(message_str)

                            event = TelemetryEvent(
                                body=message.get("body"),
                                attributes=message.get("attributes", {}),
                                scope=self._parse_scope(message.get("scope", {})),
                                resource=self._parse_resource(message.get("resource", {}))
                            )
                            events.append(event)
                        except Exception as e:
                            errors.append(f"Line {line_num} log event: {str(e)}")

                except Exception as e:
                    errors.append(f"Line {line_num}: {str(e)}")

        return events, errors

    def ingest_employees(self, csv_path: str) -> Tuple[List[Employee], List[str]]:
        """Ingest employees.csv, returns employees and errors"""
        employees: List[Employee] = []
        errors: List[str] = []

        if not os.path.exists(csv_path):
            return [], [f"File not found: {csv_path}"]

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            row_num = 0
            for row in reader:
                row_num += 1
                try:
                    emp = Employee(**row)
                    employees.append(emp)
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")

        return employees, errors

    def ingest_all(self, jsonl_path: str, csv_path: str) -> Tuple[List[TelemetryEvent], List[Employee], List[str]]:
        """Ingest both telemetry and employees, returns combined errors"""
        all_errors: List[str] = []

        events, telemetry_errors = self.ingest_telemetry_logs(jsonl_path)
        all_errors.extend(telemetry_errors)

        employees, employee_errors = self.ingest_employees(csv_path)
        all_errors.extend(employee_errors)

        return events, employees, all_errors
