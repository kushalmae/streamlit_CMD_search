import streamlit as st
from data_loader import load_data, get_command_details

# Simple page configuration
st.set_page_config(page_title="Satellite Command Lookup", page_icon="🛰️")

# Simple title and description
st.title("🛰️ Satellite Command Lookup")
st.markdown("Search and view satellite command information from CSV files.")

try:
    # Load data
    commands_df, params_df, enums_df = load_data()
    
    # Simple search functionality
    search_query = st.text_input("Search commands:", placeholder="Type to search...")
    
    # Filter commands if search query provided
    if search_query:
        filtered_commands = commands_df[
            commands_df['Command'].str.contains(search_query, case=False, na=False) |
            commands_df['Description'].str.contains(search_query, case=False, na=False)
        ]
    else:
        filtered_commands = commands_df
    
    # Command selection
    if not filtered_commands.empty:
        command_names = filtered_commands["Command"].tolist()
        selected_command = st.selectbox("Select a Command:", command_names)
        
        if selected_command:
            # Get command details
            hex_code, description, param_list = get_command_details(
                selected_command, commands_df, params_df, enums_df
            )
            
            # Display command information
            st.subheader(f"Command: {selected_command}")
            st.write(f"**Hex Code:** `{hex_code}`")
            st.write(f"**Description:** {description}")
            
            # Display parameters
            st.subheader("Parameters:")
            if not param_list:
                st.write("No parameters.")
            else:
                for param in param_list:
                    st.write(f"**{param['name']}**")
                    st.write(f"- Type: `{param['type']}`")
                    if param['range']:
                        st.write(f"- Range: `{param['range']}`")
                    if param['enum_values']:
                        st.write("- Possible values:")
                        for value, label in param['enum_values'].items():
                            st.write(f"  - `{value}`: {label}")
                    st.write("")  # Add spacing
    else:
        st.warning("No commands found matching your search.")

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Make sure CSV files exist. Run `python generate_data.py` if needed.")

