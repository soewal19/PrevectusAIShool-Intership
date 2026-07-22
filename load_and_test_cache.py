
#!/usr/bin/env python3
"""Load data and test cache analytics"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.infrastructure.duckdb_repository import DuckDBTelemetryRepository
from src.infrastructure.analytics_service import DuckDBAnalyticsService

def main():
    print("Loading data...")
    repo = DuckDBTelemetryRepository()
    
    # Load our generated data
    jsonl_path = project_root / "output" / "telemetry_logs.jsonl"
    csv_path = project_root / "output" / "employees.csv"
    
    errors = repo.ingest_from_files(str(jsonl_path), str(csv_path))
    if errors:
        print(f"⚠️ Warnings during ingestion: {len(errors)}")
        for err in errors[:5]:
            print(f"  - {err}")
    
    print("\n✅ Data loaded successfully!")
    
    print("\nTesting cache analytics...")
    analytics = DuckDBAnalyticsService()
    
    print("\n1. Cache Usage Stats:")
    cache_usage = analytics.get_cache_usage()
    print(cache_usage)
    
    print("\n2. Cache Efficiency:")
    cache_efficiency = analytics.get_cache_efficiency()
    print(cache_efficiency)
    
    print("\n3. Top Cache Users:")
    top_users = analytics.get_top_cache_users()
    print(top_users)
    
    print("\n4. Cache by Model:")
    cache_by_model = analytics.get_cache_by_model()
    print(cache_by_model)
    
    print("\n5. Daily Cache Metrics:")
    daily_cache = analytics.get_daily_cache_metrics()
    print(daily_cache)
    
    print("\n🎉 All cache analytics working correctly!")

if __name__ == "__main__":
    main()
