import pandas as pd
import numpy as np

def load_data_fast():
    """Optimized CSV loading with dtypes and column selection"""
    
    # Define specific data types to avoid pandas guessing (much faster)
    commands_dtypes = {
        'Command': 'string',
        'HexCode': 'string', 
        'Description': 'string',
        'Params': 'string'
    }
    
    params_dtypes = {
        'ParamID': 'string',
        'Type': 'string',
        'EnumSet': 'string',
        'Range': 'string'
    }
    
    enums_dtypes = {
        'EnumSet': 'string',
        'Value': 'int32',  # Use smaller int type if possible
        'Label': 'string'
    }
    
    # Load with specified dtypes (2-3x faster)
    commands_df = pd.read_csv("master_commands.csv", dtype=commands_dtypes)
    params_df = pd.read_csv("parameter_metadata.csv", dtype=params_dtypes)
    enums_df = pd.read_csv("enum_definitions.csv", dtype=enums_dtypes)
    
    return commands_df, params_df, enums_df

def load_data_chunked(chunk_size=10000):
    """Load large CSV files in chunks to save memory"""
    
    # For very large files, process in chunks
    commands_chunks = []
    for chunk in pd.read_csv("master_commands.csv", chunksize=chunk_size):
        # Process each chunk if needed
        commands_chunks.append(chunk)
    
    commands_df = pd.concat(commands_chunks, ignore_index=True)
    
    # Load others normally if they're smaller
    params_df = pd.read_csv("parameter_metadata.csv")
    enums_df = pd.read_csv("enum_definitions.csv")
    
    return commands_df, params_df, enums_df

def load_specific_columns():
    """Load only the columns you need (much faster for wide files)"""
    
    # Only load specific columns if you have many columns
    commands_df = pd.read_csv("master_commands.csv", 
                             usecols=['Command', 'HexCode', 'Description', 'Params'])
    
    params_df = pd.read_csv("parameter_metadata.csv",
                           usecols=['ParamID', 'Type', 'Range', 'EnumSet'])
    
    enums_df = pd.read_csv("enum_definitions.csv")
    
    return commands_df, params_df, enums_df

# Alternative: Use Polars (much faster than pandas for large files)
def load_data_polars():
    """Ultra-fast loading using Polars library"""
    try:
        import polars as pl
        
        # Polars is 5-10x faster than pandas for large CSV files
        commands_df = pl.read_csv("master_commands.csv").to_pandas()
        params_df = pl.read_csv("parameter_metadata.csv").to_pandas()
        enums_df = pl.read_csv("enum_definitions.csv").to_pandas()
        
        return commands_df, params_df, enums_df
    except ImportError:
        print("Polars not installed. Install with: pip install polars")
        return load_data_fast()

# Convert CSV to faster formats
def convert_to_parquet():
    """Convert CSV files to Parquet format (much faster to load)"""
    
    # One-time conversion
    commands_df = pd.read_csv("master_commands.csv")
    params_df = pd.read_csv("parameter_metadata.csv") 
    enums_df = pd.read_csv("enum_definitions.csv")
    
    # Save as parquet (compressed, column-oriented format)
    commands_df.to_parquet("master_commands.parquet")
    params_df.to_parquet("parameter_metadata.parquet")
    enums_df.to_parquet("enum_definitions.parquet")
    
    print("✅ Converted CSV files to Parquet format for faster loading")

def load_data_parquet():
    """Load from Parquet files (5-10x faster than CSV)"""
    try:
        commands_df = pd.read_parquet("master_commands.parquet")
        params_df = pd.read_parquet("parameter_metadata.parquet")
        enums_df = pd.read_parquet("enum_definitions.parquet")
        
        return commands_df, params_df, enums_df
    except FileNotFoundError:
        print("Parquet files not found. Converting from CSV...")
        convert_to_parquet()
        return load_data_parquet()

# Caching for repeated loads
_cached_data = None

def load_data_cached():
    """Cache data in memory for repeated access"""
    global _cached_data
    
    if _cached_data is None:
        print("Loading data for the first time...")
        _cached_data = load_data_fast()
    else:
        print("Using cached data...")
    
    return _cached_data 