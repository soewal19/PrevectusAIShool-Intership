from typing import List, Dict, Any
import os
from openai import OpenAI
from src.domain.ports import InsightService


class OpenAIInsightService(InsightService):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
    def _prepare_analytics_context(self, analytics_data: Dict[str, Any]) -> str:
        """Convert analytics data to a human-readable string for LLM"""
        context_parts = []
        
        if "daily_metrics" in analytics_data:
            context_parts.append("Daily Metrics:")
            context_parts.append(str(analytics_data["daily_metrics"]))
        
        if "event_distribution" in analytics_data:
            context_parts.append("\nEvent Distribution:")
            context_parts.append(str(analytics_data["event_distribution"]))
        
        if "user_role_distribution" in analytics_data:
            context_parts.append("\nUser Role Distribution:")
            context_parts.append(str(analytics_data["user_role_distribution"]))
        
        if "model_usage" in analytics_data:
            context_parts.append("\nModel Usage:")
            context_parts.append(str(analytics_data["model_usage"]))
        
        if "tool_usage" in analytics_data:
            context_parts.append("\nTool Usage:")
            context_parts.append(str(analytics_data["tool_usage"]))
        
        if "cost_by_practice" in analytics_data:
            context_parts.append("\nCost by Practice:")
            context_parts.append(str(analytics_data["cost_by_practice"]))
        
        if "cache_usage" in analytics_data:
            context_parts.append("\nCache Usage:")
            context_parts.append(str(analytics_data["cache_usage"]))
        
        if "cache_efficiency" in analytics_data:
            context_parts.append("\nCache Efficiency:")
            context_parts.append(str(analytics_data["cache_efficiency"]))
        
        return "\n".join(context_parts)
        
    def generate_executive_summary(self, analytics_data: Dict[str, Any]) -> str:
        context = self._prepare_analytics_context(analytics_data)
        prompt = f"""You are an expert product analyst for a developer platform.
Given the following Claude Code usage analytics, generate a concise, executive summary (max 300 words).
Focus on:
1. Key trends in usage and cost
2. Most/least used models and tools
3. Cache effectiveness
4. Actionable recommendations

Analytics data:
{context}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
        
    def detect_anomalies(self, analytics_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        context = self._prepare_analytics_context(analytics_data)
        prompt = f"""You are an expert anomaly detector for telemetry data.
Given the following Claude Code usage analytics, identify 3-5 anomalies or unusual patterns.
Return a JSON list of objects with:
- "description": Brief description of the anomaly
- "severity": "low", "medium", or "high"
- "potential_impact": What this might mean
- "recommendation": Suggested next steps

Do NOT include any markdown formatting, only valid JSON.
Analytics data:
{context}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result.get("anomalies", []) if "anomalies" in result else [result] if isinstance(result, dict) else []
        
    def generate_user_insights(self, analytics_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        context = self._prepare_analytics_context(analytics_data)
        prompt = f"""You are an expert in developer productivity analytics.
Given the following Claude Code usage analytics, generate 3-5 key user insights.
Return a JSON list of objects with:
- "title": Short, catchy title
- "insight": The insight itself
- "category": "usage", "cost", "cache", or "productivity"
- "actionable_step": What to do about it

Do NOT include any markdown formatting, only valid JSON.
Analytics data:
{context}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            response_format={"type": "json_object"}
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result.get("insights", []) if "insights" in result else [result] if isinstance(result, dict) else []
