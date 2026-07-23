
from abc import ABC, abstractmethod
from typing import List
from src.domain.models import TelemetryEvent


class TelemetryRepository(ABC):
    @abstractmethod
    def save_events(self, events: List[TelemetryEvent]) -> None:
        pass

    @abstractmethod
    def get_all_events(self) -> List[TelemetryEvent]:
        pass


class AnalyticsService(ABC):
    @abstractmethod
    def get_daily_metrics(self):
        pass

    @abstractmethod
    def get_event_distribution(self):
        pass

    @abstractmethod
    def get_user_role_distribution(self):
        pass
    
    @abstractmethod
    def get_model_usage(self):
        pass
    
    @abstractmethod
    def get_tool_usage(self):
        pass
    
    @abstractmethod
    def get_cost_by_practice(self):
        pass
    
    @abstractmethod
    def get_cache_usage(self):
        pass
    
    @abstractmethod
    def get_cache_efficiency(self):
        pass
    
    @abstractmethod
    def get_top_cache_users(self, limit: int = 10):
        pass
    
    @abstractmethod
    def get_cache_by_model(self):
        pass
    
    @abstractmethod
    def get_daily_cache_metrics(self):
        pass


class InsightService(ABC):
    @abstractmethod
    def generate_executive_summary(self, analytics_data: dict) -> str:
        pass
    
    @abstractmethod
    def detect_anomalies(self, analytics_data: dict) -> List[dict]:
        pass
    
    @abstractmethod
    def generate_user_insights(self, analytics_data: dict) -> List[dict]:
        pass

