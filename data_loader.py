import pandas as pd

# Global cache for data
_cached_data = None

def load_data():
    """Load CSV data files with optimizations"""
    global _cached_data
    
    # Use cache if data already loaded
    if _cached_data is not None:
        return _cached_data
    
    # Define data types for faster loading (2-3x improvement)
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
        'Value': 'int32',
        'Label': 'string'
    }
    
    # Load with specified dtypes (much faster than letting pandas guess)
    commands_df = pd.read_csv("master_commands.csv", dtype=commands_dtypes)
    params_df = pd.read_csv("parameter_metadata.csv", dtype=params_dtypes)
    enums_df = pd.read_csv("enum_definitions.csv", dtype=enums_dtypes)
    
    # Cache the loaded data
    _cached_data = (commands_df, params_df, enums_df)
    return _cached_data

def get_command_details(command_name, commands_df, params_df, enums_df):
    """Get detailed information for a specific command"""
    # Find the command
    cmd = commands_df[commands_df['Command'] == command_name].iloc[0]
    hex_code = cmd['HexCode']
    description = cmd['Description']
    
    # Get parameters
    params_str = cmd['Params']
    if pd.isna(params_str) or params_str.strip() == "":
        param_ids = []
    else:
        param_ids = [p.strip() for p in params_str.split(",")]
    
    param_details = []
    for pid in param_ids:
        # Find parameter info
        param_matches = params_df[params_df['ParamID'] == pid]
        if param_matches.empty:
            param_info = {
                "name": pid,
                "type": "unknown",
                "range": None,
                "enum_values": None
            }
        else:
            param_row = param_matches.iloc[0]
            param_info = {
                "name": pid,
                "type": param_row["Type"],
                "range": param_row["Range"] if pd.notna(param_row["Range"]) else None,
                "enum_values": None
            }
            
            # Handle enum types
            if param_row["Type"] == "enum" and pd.notna(param_row["EnumSet"]):
                enum_set = param_row["EnumSet"]
                enum_vals = enums_df[enums_df["EnumSet"] == enum_set]
                if not enum_vals.empty:
                    param_info["enum_values"] = dict(
                        zip(enum_vals["Value"].astype(str), enum_vals["Label"])
                    )
        
        param_details.append(param_info)
    
    return hex_code, description, param_details