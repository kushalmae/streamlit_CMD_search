"""
Simple tests for data_loader.py using real CSV files

Test Strategy:
- Uses actual CSV files instead of mock data for realistic testing
- Tests core functions: load_data() and get_command_details()
- Focuses on structure validation rather than specific data values
- Keeps tests simple and maintainable

Test Structure:
1. test_load_data_returns_dataframes: Validates load_data() returns correct types
2. test_load_data_has_expected_columns: Checks CSV files have required columns
3. test_get_command_details_with_real_data: Tests command lookup with real data

How to run:
- All tests: pytest test_data_loader.py
- Individual test: pytest test_data_loader.py::test_name
- By pattern: pytest test_data_loader.py -k "pattern"
- With details: pytest test_data_loader.py -v
  (verbose mode shows test names, PASSED/FAILED status, and execution time)

Examples:
- pytest test_data_loader.py::test_load_data_returns_dataframes
- pytest test_data_loader.py -k "load_data"
- pytest test_data_loader.py::test_load_data_returns_dataframes -v
- pytest test_data_loader.py::test_get_command_details_with_real_data -s
"""

import pandas as pd
import data_loader


def test_load_data_returns_dataframes():
    """Test that load_data returns three DataFrames"""
    commands_df, params_df, enums_df = data_loader.load_data()
    
    assert isinstance(commands_df, pd.DataFrame)
    assert isinstance(params_df, pd.DataFrame)
    assert isinstance(enums_df, pd.DataFrame)
    assert len(commands_df) > 0
    assert len(params_df) > 0
    assert len(enums_df) > 0


def test_load_data_has_expected_columns():
    """Test that DataFrames have expected columns"""
    commands_df, params_df, enums_df = data_loader.load_data()
    
    # Check commands columns
    assert 'Command' in commands_df.columns
    assert 'HexCode' in commands_df.columns
    assert 'Description' in commands_df.columns
    assert 'Params' in commands_df.columns
    
    # Check params columns
    assert 'ParamID' in params_df.columns
    assert 'Type' in params_df.columns
    
    # Check enums columns
    assert 'EnumSet' in enums_df.columns
    assert 'Value' in enums_df.columns
    assert 'Label' in enums_df.columns


def test_get_command_details_with_real_data():
    """Test get_command_details with first command from real data"""
    commands_df, params_df, enums_df = data_loader.load_data()
    
    # Get first command
    first_command = commands_df.iloc[0]['Command']
    print(f"\nTesting command: {first_command}")
    
    hex_code, description, param_details = data_loader.get_command_details(
        first_command, commands_df, params_df, enums_df
    )
    
    # Detailed assertions
    assert isinstance(hex_code, str)
    assert len(hex_code) > 0, "Hex code should not be empty"
    print(f"Hex code: {hex_code}")
    
    assert isinstance(description, str)
    assert len(description) > 0, "Description should not be empty"
    print(f"Description: {description}")
    
    assert isinstance(param_details, list)
    print(f"Number of parameters: {len(param_details)}")
    
    # Check parameter structure if parameters exist
    for i, param in enumerate(param_details):
        assert isinstance(param, dict), f"Parameter {i} should be a dictionary"
        assert 'name' in param, f"Parameter {i} should have 'name' key"
        assert 'type' in param, f"Parameter {i} should have 'type' key"
        print(f"  Param {i+1}: {param['name']} ({param['type']})")
        
        if param.get('enum_values'):
            print(f"    Enum values: {list(param['enum_values'].keys())}")
        if param.get('range'):
            print(f"    Range: {param['range']}")
    
    print("✓ Command details test passed")