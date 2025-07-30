"""
Data Loader for Command Search System

This module loads and processes CSV files containing command information,
parameter metadata, and enum definitions. Provides functionality to search
and display detailed command information.

CSV Files Required:
- master_commands.csv: Command names, hex codes, descriptions, parameters
- parameter_metadata.csv: Parameter types, ranges, enum sets
- enum_definitions.csv: Enum values and labels

Usage:
    python data_loader.py [command_name]
"""

import pandas as pd
import argparse
import sys

# Global cache for data
_cached_data = None

def load_data():
    """
    Load and cache CSV data files with performance optimizations.
    
    Returns:
        Pandas DataFrame: (commands_df, params_df, enums_df) - DataFrames containing
               command data, parameter metadata, and enum definitions
    
    Note:
        Data is cached globally to avoid reloading on subsequent calls.
    """
    global _cached_data
    
    # Use cache if data already loaded
    if _cached_data is not None:
        return _cached_data
    
    # Define data types for faster loading (2-3x improvement)
    # Specifying dtypes prevents pandas from inferring types, which is slow
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
    """
    Get detailed information for a specific command.
    
    Args:
        command_name (str): Name of the command to look up
        commands_df (DataFrame): Commands data
        params_df (DataFrame): Parameter metadata
        enums_df (DataFrame): Enum definitions
    
    Returns:
        Pandas DataFrame: (hex_code, description, param_details)
            - hex_code (str): Command's hexadecimal code
            - description (str): Command description
            - param_details (list): List of parameter dictionaries with
              name, type, range, and enum_values keys
    """
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
            
            # Handle enum types - lookup enum values and labels
            if param_row["Type"] == "enum" and pd.notna(param_row["EnumSet"]):
                enum_set = param_row["EnumSet"]
                enum_vals = enums_df[enums_df["EnumSet"] == enum_set]
                if not enum_vals.empty:
                    # Create value:label mapping for display
                    param_info["enum_values"] = dict(
                        zip(enum_vals["Value"].astype(str), enum_vals["Label"])
                    )
        
        param_details.append(param_info)
    
    return hex_code, description, param_details

def main():
    """
    Main entry point for the command search tool.
    
    Handles command-line arguments and user input to search for and display
    command details. If no command is provided as an argument, prompts the
    user for input.
    """
    parser = argparse.ArgumentParser(description='Get command details')
    parser.add_argument('command', nargs='?', help='Command name to search for')
    args = parser.parse_args()
    
    # Load data
    commands_df, params_df, enums_df = load_data()
    
    # Get command name
    command_name = args.command
    if not command_name:
        command_name = input("Enter command name: ").strip()
    
    # Find and display command details
    if command_name in commands_df['Command'].values:
        hex_code, description, param_details = get_command_details(
            command_name, commands_df, params_df, enums_df
        )
        
        print(f"\nCommand: {command_name}")
        print(f"Hex Code: {hex_code}")
        print(f"Description: {description}")
        
        if param_details:
            print("\nParameters:")
            for param in param_details:
                print(f"  - {param['name']} ({param['type']})")
                if param['enum_values']:
                    for value, label in param['enum_values'].items():
                        print(f"    {value}: {label}")
    else:
        print(f"Command '{command_name}' not found")

if __name__ == "__main__":
    main()