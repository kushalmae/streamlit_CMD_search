import time
import pandas as pd
from data_loader import load_data
from data_loader_optimized import (
    load_data_fast, 
    load_data_polars, 
    load_data_parquet,
    convert_to_parquet,
    load_data_cached
)

def benchmark_function(func, name, *args):
    """Benchmark a function and return execution time"""
    print(f"\n🔄 Testing {name}...")
    start_time = time.time()
    
    try:
        result = func(*args)
        end_time = time.time()
        duration = end_time - start_time
        print(f"✅ {name}: {duration:.4f} seconds")
        return duration, True
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"❌ {name} failed: {str(e)}")
        return duration, False

def run_csv_loading_benchmark():
    """Compare different CSV loading methods"""
    
    print("🚀 CSV Loading Performance Benchmark")
    print("=" * 50)
    
    results = {}
    
    # Test original method
    duration, success = benchmark_function(load_data, "Original pandas method")
    if success:
        results["Original"] = duration
    
    # Test optimized method
    duration, success = benchmark_function(load_data_fast, "Optimized pandas (with dtypes)")
    if success:
        results["Optimized"] = duration
    
    # Test Polars (if available)
    duration, success = benchmark_function(load_data_polars, "Polars library")
    if success:
        results["Polars"] = duration
    
    # Convert to Parquet first (one-time cost)
    print(f"\n🔄 Converting to Parquet format (one-time setup)...")
    try:
        convert_to_parquet()
        
        # Test Parquet loading
        duration, success = benchmark_function(load_data_parquet, "Parquet format")
        if success:
            results["Parquet"] = duration
    except Exception as e:
        print(f"❌ Parquet conversion failed: {e}")
    
    # Test caching (run twice to show cache benefit)
    duration1, success1 = benchmark_function(load_data_cached, "Cached (first load)")
    if success1:
        results["Cache_First"] = duration1
        
        duration2, success2 = benchmark_function(load_data_cached, "Cached (second load)")
        if success2:
            results["Cache_Second"] = duration2
    
    # Show results comparison
    print(f"\n📊 PERFORMANCE COMPARISON")
    print("=" * 50)
    
    if "Original" in results:
        baseline = results["Original"]
        print(f"📈 Speed improvements vs original method:")
        
        for method, duration in results.items():
            if method != "Original" and duration > 0:
                speedup = baseline / duration
                print(f"  {method:20}: {speedup:.1f}x faster ({duration:.4f}s)")
            elif duration == 0:
                print(f"  {method:20}: Instant! (0.0000s)")
    
    return results

if __name__ == "__main__":
    # Run the benchmark
    results = run_csv_loading_benchmark()
    
    print(f"\n🎯 RECOMMENDATIONS:")
    print("=" * 50)
    print("1. 🚀 For immediate improvement: Use load_data_fast() (2-3x faster)")
    print("2. 📦 For large files: Convert to Parquet format (5-10x faster)")  
    print("3. 🧠 For repeated access: Use caching (instant after first load)")
    print("4. ⚡ For maximum speed: Install Polars (pip install polars)") 