
#!/usr/bin/env python3
"""Test script for cache analytics"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.infrastructure.analytics_service import DuckDBAnalyticsService

def test_cache_analytics():
    print("Testing cache analytics...")
    analytics = DuckDBAnalyticsService()
    
    print("\n1. Testing get_cache_usage()")
    cache_usage = analytics.get_cache_usage()
    print(f"✓ Success: {cache_usage.shape[0]} rows")
    print(cache_usage)
    
    print("\n2. Testing get_cache_efficiency()")
    cache_efficiency = analytics.get_cache_efficiency()
    print(f"✓ Success: {cache_efficiency.shape[0]} rows")
    print(cache_efficiency)
    
    print("\n3. Testing get_top_cache_users()")
    top_users = analytics.get_top_cache_users(5)
    print(f"✓ Success: {top_users.shape[0]} rows")
    print(top_users)
    
    print("\n4. Testing get_cache_by_model()")
    cache_by_model = analytics.get_cache_by_model()
    print(f"✓ Success: {cache_by_model.shape[0]} rows")
    print(cache_by_model)
    
    print("\n5. Testing get_daily_cache_metrics()")
    daily_cache = analytics.get_daily_cache_metrics()
    print(f"✓ Success: {daily_cache.shape[0]} rows")
    print(daily_cache)
    
    print("\n✅ All cache analytics tests passed!")

if __name__ == "__main__":
    test_cache_analytics()
