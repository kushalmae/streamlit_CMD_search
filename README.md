# 🛰️ Satellite Command Control System

A comprehensive Streamlit-based interface for satellite command lookup and parameter management. This system allows users to easily search, view, and understand satellite commands across multiple data sources.

## ✨ Features

- **🔍 Advanced Command Search**: Search commands by name or description with real-time filtering
- **📊 Interactive Dashboard**: Visual statistics and system overview
- **🎯 Detailed Command View**: Complete command information including hex codes, descriptions, and parameters
- **📋 Parameter Management**: Comprehensive parameter details with types, ranges, and enum values
- **🎮 Command Simulation**: Safe command execution simulation
- **📱 Responsive Design**: Modern, mobile-friendly interface

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone or download the project files**
2. **Create a virtual environment** (recommended):
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1  # Windows PowerShell
   # or: venv\Scripts\activate.bat  # Windows CMD
   # or: source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate sample data**:
   ```bash
   python generate_data.py
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** to `http://localhost:8501`

## 📁 Project Structure

```
streamlit_command_search/
├── app.py                    # Main Streamlit application
├── data_loader.py           # Data loading and processing functions
├── generate_data.py         # Sample data generator
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── master_commands.csv     # Command definitions (generated)
├── parameter_metadata.csv  # Parameter specifications (generated)
└── enum_definitions.csv    # Enum value mappings (generated)
```

## 📊 Data Format

### Master Commands CSV
Contains the main command definitions:
- `Command`: Command name (e.g., "CMD_ARM_SYSTEM")
- `HexCode`: Hexadecimal command code (e.g., "0xAF23")
- `Description`: Human-readable description
- `Params`: Comma-separated parameter IDs

### Parameter Metadata CSV
Defines parameter specifications:
- `ParamID`: Unique parameter identifier
- `Type`: Data type (int, float, bool, enum)
- `EnumSet`: Reference to enum definitions (for enum types)
- `Range`: Valid value range (for numeric types)

### Enum Definitions CSV
Maps enum values to labels:
- `EnumSet`: Enum set identifier
- `Value`: Numeric enum value
- `Label`: Human-readable label

## 🛠️ Usage

### Basic Operations

1. **Search Commands**: Use the sidebar search box to find commands by name or description
2. **Filter by Category**: Select specific command categories from the dropdown
3. **View Command Details**: Click on any command to see complete information
4. **Explore Parameters**: Use the detailed view or summary table tabs for parameters
5. **Simulate Execution**: Test command execution with the simulation button

### Advanced Features

- **Real-time Search**: Results update as you type
- **Parameter Analysis**: View parameter types, ranges, and enum mappings
- **System Statistics**: Monitor command database metrics
- **Error Handling**: Graceful handling of missing or corrupted data

## 🔧 Customization

### Adding New Commands

1. Edit the data in `generate_data.py`
2. Run `python generate_data.py` to regenerate CSV files
3. Refresh the Streamlit app

### Modifying the Interface

- Edit `app.py` for UI changes
- Modify `data_loader.py` for data processing logic
- Update CSS in the `st.markdown()` sections for styling

## 🐛 Troubleshooting

### Common Issues

**"Missing required files" error**:
- Run `python generate_data.py` to create CSV files

**Command not found**:
- Check that the command exists in `master_commands.csv`
- Verify CSV file formatting

**Parameter errors**:
- Ensure parameter IDs match between CSV files
- Check enum set references

### Getting Help

1. Check that all CSV files exist and have proper headers
2. Verify Python version compatibility (3.7+)
3. Ensure all dependencies are installed correctly

## 📋 Sample Commands

The system includes 14 realistic satellite commands:

- `CMD_ARM_SYSTEM` - Arms safety-critical subsystems
- `CMD_SET_MODE` - Sets operational mode
- `CMD_DEPLOY_ANTENNA` - Deploys communication antenna
- `CMD_POWER_ON_SUBSYSTEM` - Powers on subsystems
- `CMD_SET_ATTITUDE` - Controls satellite orientation
- `CMD_START_RECORDING` - Begins data recording
- `CMD_TRANSMIT_DATA` - Initiates data transmission
- And more...

## 🔒 Safety Features

- **Read-only Operations**: The interface only displays data, no actual commands are sent
- **Simulation Mode**: Safe command execution testing
- **Error Handling**: Comprehensive error checking and user feedback
- **Data Validation**: Automatic validation of CSV file structure

## 📈 Future Enhancements

- Command history tracking
- Real-time telemetry integration
- Command scheduling
- User authentication
- Audit logging
- Export functionality

---

**Built with ❤️ using Streamlit and Python** 