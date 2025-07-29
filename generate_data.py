
import pandas as pd
import os

# Create CSV files in current directory
print("Generating satellite command data...")

# 1. Master Command CSV - Expanded with more realistic satellite commands
master_command_data = pd.DataFrame({
    "Command": [
        "CMD_ARM_SYSTEM", "CMD_SET_MODE", "CMD_DEPLOY_ANTENNA", 
        "CMD_POWER_ON_SUBSYSTEM", "CMD_POWER_OFF_SUBSYSTEM", 
        "CMD_SET_ATTITUDE", "CMD_START_RECORDING", "CMD_STOP_RECORDING",
        "CMD_TRANSMIT_DATA", "CMD_ENTER_SAFE_MODE", "CMD_CALIBRATE_SENSOR",
        "CMD_UPDATE_ORBIT", "CMD_ACTIVATE_PAYLOAD", "CMD_SHUTDOWN_PAYLOAD"
    ],
    "HexCode": [
        "0xAF23", "0xB104", "0xC302", "0xD405", "0xD406", 
        "0xE507", "0xF608", "0xF609", "0xG710", "0xH811",
        "0xI912", "0xJ013", "0xK114", "0xK115"
    ],
    "Description": [
        "Arms the safety-critical subsystems for operation",
        "Sets the system operational mode (SAFE/LIVE/TEST)",
        "Deploys the primary communication antenna",
        "Powers on specified subsystem with safety checks",
        "Powers off specified subsystem gracefully",
        "Sets satellite attitude using reaction wheels",
        "Starts data recording from all active sensors",
        "Stops data recording and closes files",
        "Initiates data transmission to ground station",
        "Forces satellite into safe mode immediately",
        "Calibrates specified sensor with reference values",
        "Updates orbital parameters and trajectory",
        "Activates scientific payload instruments",
        "Shuts down payload to conserve power"
    ],
    "Params": [
        "Mode,Delay", "Mode", "DeployType,Confirm", 
        "SubsystemID,PowerLevel", "SubsystemID,Confirm",
        "Roll,Pitch,Yaw,Duration", "DataType,Compression", "Confirm",
        "GroundStation,Frequency,PowerLevel", "Reason", "SensorID,CalType",
        "Altitude,Inclination,RAAN", "PayloadID,Config", "PayloadID,SaveState"
    ]
})

# 2. Parameter Metadata CSV - Expanded with more parameter types
parameter_metadata = pd.DataFrame({
    "ParamID": [
        "Mode", "Delay", "DeployType", "Confirm", "SubsystemID", "PowerLevel",
        "Roll", "Pitch", "Yaw", "Duration", "DataType", "Compression",
        "GroundStation", "Frequency", "Reason", "SensorID", "CalType",
        "Altitude", "Inclination", "RAAN", "PayloadID", "Config", "SaveState"
    ],
    "Type": [
        "enum", "int", "enum", "bool", "enum", "float",
        "float", "float", "float", "int", "enum", "enum",
        "enum", "float", "enum", "enum", "enum",
        "float", "float", "float", "enum", "enum", "bool"
    ],
    "EnumSet": [
        "ARM_MODE", None, "DEPLOY_TYPE", None, "SUBSYSTEM_ID", None,
        None, None, None, None, "DATA_TYPE", "COMPRESSION_TYPE",
        "GROUND_STATION", None, "SAFE_REASON", "SENSOR_ID", "CAL_TYPE",
        None, None, None, "PAYLOAD_ID", "PAYLOAD_CONFIG", None
    ],
    "Range": [
        None, "0-300", None, None, None, "0.0-1.0",
        "-180.0-180.0", "-90.0-90.0", "-180.0-180.0", "1-3600", None, None,
        None, "2000.0-2500.0", None, None, None,
        "200.0-2000.0", "0.0-180.0", "0.0-360.0", None, None, None
    ]
})

# 3. Enum Definitions CSV - Comprehensive enum values
enum_definitions = pd.DataFrame({
    "EnumSet": [
        # ARM_MODE enum
        "ARM_MODE", "ARM_MODE", "ARM_MODE",
        # DEPLOY_TYPE enum  
        "DEPLOY_TYPE", "DEPLOY_TYPE",
        # SUBSYSTEM_ID enum
        "SUBSYSTEM_ID", "SUBSYSTEM_ID", "SUBSYSTEM_ID", "SUBSYSTEM_ID", "SUBSYSTEM_ID",
        # DATA_TYPE enum
        "DATA_TYPE", "DATA_TYPE", "DATA_TYPE", "DATA_TYPE",
        # COMPRESSION_TYPE enum
        "COMPRESSION_TYPE", "COMPRESSION_TYPE", "COMPRESSION_TYPE",
        # GROUND_STATION enum
        "GROUND_STATION", "GROUND_STATION", "GROUND_STATION",
        # SAFE_REASON enum
        "SAFE_REASON", "SAFE_REASON", "SAFE_REASON", "SAFE_REASON",
        # SENSOR_ID enum
        "SENSOR_ID", "SENSOR_ID", "SENSOR_ID", "SENSOR_ID",
        # CAL_TYPE enum
        "CAL_TYPE", "CAL_TYPE", "CAL_TYPE",
        # PAYLOAD_ID enum
        "PAYLOAD_ID", "PAYLOAD_ID", "PAYLOAD_ID",
        # PAYLOAD_CONFIG enum
        "PAYLOAD_CONFIG", "PAYLOAD_CONFIG", "PAYLOAD_CONFIG"
    ],
    "Value": [
        # ARM_MODE values
        0, 1, 2,
        # DEPLOY_TYPE values
        0, 1,
        # SUBSYSTEM_ID values
        1, 2, 3, 4, 5,
        # DATA_TYPE values
        0, 1, 2, 3,
        # COMPRESSION_TYPE values
        0, 1, 2,
        # GROUND_STATION values
        1, 2, 3,
        # SAFE_REASON values
        0, 1, 2, 3,
        # SENSOR_ID values
        1, 2, 3, 4,
        # CAL_TYPE values
        0, 1, 2,
        # PAYLOAD_ID values
        1, 2, 3,
        # PAYLOAD_CONFIG values
        0, 1, 2
    ],
    "Label": [
        # ARM_MODE labels
        "SAFE", "LIVE", "TEST",
        # DEPLOY_TYPE labels
        "MAIN", "BACKUP",
        # SUBSYSTEM_ID labels
        "COMMS", "POWER", "ATTITUDE", "THERMAL", "PAYLOAD",
        # DATA_TYPE labels
        "TELEMETRY", "SCIENCE", "HOUSEKEEPING", "LOGS",
        # COMPRESSION_TYPE labels
        "NONE", "LOSSLESS", "LOSSY",
        # GROUND_STATION labels
        "HOUSTON", "MADRID", "CANBERRA",
        # SAFE_REASON labels
        "POWER_LOW", "TEMP_HIGH", "COMM_LOSS", "MANUAL",
        # SENSOR_ID labels
        "GYRO", "MAGNETOMETER", "SUN_SENSOR", "STAR_TRACKER",
        # CAL_TYPE labels
        "FACTORY", "FIELD", "DRIFT",
        # PAYLOAD_ID labels
        "CAMERA", "SPECTROMETER", "RADAR",
        # PAYLOAD_CONFIG labels
        "LOW_POWER", "NORMAL", "HIGH_RESOLUTION"
    ]
})

# Save all CSV files to current directory
master_command_data.to_csv("master_commands.csv", index=False)
parameter_metadata.to_csv("parameter_metadata.csv", index=False)
enum_definitions.to_csv("enum_definitions.csv", index=False)

print("✅ Generated 3 CSV files:")
print("  - master_commands.csv (14 satellite commands)")
print("  - parameter_metadata.csv (23 parameter definitions)")
print("  - enum_definitions.csv (comprehensive enum mappings)")
print("\nRun 'streamlit run app.py' to start the application!")


