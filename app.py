import streamlit as st
from data_loader import load_data, get_command_details

# Page configuration
st.set_page_config(
    page_title="Satellite Command Lookup", 
    page_icon="🛰️",
    layout="centered"
)

# Header with clear description
st.title("🛰️ Satellite Command Lookup")
st.markdown("**Find satellite commands and their parameters quickly**")
st.markdown("---")

try:
    # Load data with loading message
    with st.spinner("Loading satellite command database..."):
        commands_df, params_df, enums_df = load_data()
    
    # Success message
    st.success(f"✅ Loaded {len(commands_df)} commands successfully")
    
    # Search section
    st.subheader("🔍 Search Commands")
    search_query = st.text_input(
        "Type to search commands or descriptions:",
        placeholder="Example: antenna, power, mode...",
        help="Search works on both command names and descriptions"
    )
    
    # Filter commands if search query provided
    if search_query:
        filtered_commands = commands_df[
            commands_df['Command'].str.contains(search_query, case=False, na=False) |
            commands_df['Description'].str.contains(search_query, case=False, na=False)
        ]
        if not filtered_commands.empty:
            st.info(f"Found {len(filtered_commands)} matching commands")
        else:
            st.warning("No commands found. Try different search terms.")
    else:
        filtered_commands = commands_df
        st.info(f"Showing all {len(commands_df)} available commands")
    
    # Command selection
    if not filtered_commands.empty:
        st.markdown("---")
        st.subheader("📋 Select Command")
        
        # Create a more user-friendly display for the selectbox
        command_options = []
        for _, row in filtered_commands.iterrows():
            command_options.append(f"{row['Command']} - {row['Description']}")
        
        selected_display = st.selectbox(
            "Choose a command to view details:",
            command_options,
            help="Commands are shown with their descriptions for easier selection"
        )
        
        if selected_display:
            # Extract actual command name from the display string
            selected_command = selected_display.split(" - ")[0]
            
            # Get command details
            hex_code, description, param_list = get_command_details(
                selected_command, commands_df, params_df, enums_df
            )
            
            # Display command information in a clean format
            st.markdown("---")
            st.subheader("🎯 Command Details")
            
            # Command info in columns for better layout
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Command Name:**")
                st.code(selected_command)
            with col2:
                st.markdown(f"**Hex Code:**")
                st.code(hex_code)
            
            st.markdown(f"**Description:**")
            st.info(description)
            
            # Parameters section
            st.markdown("---")
            st.subheader("⚙️ Parameters")
            
            if not param_list:
                st.success("✅ This command has no parameters - ready to use!")
            else:
                st.markdown(f"This command requires **{len(param_list)} parameter(s)**:")
                
                # Display parameters in a clean, organized way
                for i, param in enumerate(param_list, 1):
                    with st.container():
                        st.markdown(f"### Parameter {i}: `{param['name']}`")
                        
                        # Parameter details in columns
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Type:**")
                            st.code(param['type'])
                            
                            if param['range']:
                                st.markdown("**Range:**")
                                st.code(param['range'])
                        
                        with col2:
                            if param['enum_values']:
                                st.markdown("**Possible Values:**")
                                for value, label in param['enum_values'].items():
                                    st.markdown(f"• `{value}` → {label}")
                            else:
                                st.markdown("**Format:**")
                                if param['type'] == 'int':
                                    st.write("Enter whole numbers")
                                elif param['type'] == 'float':
                                    st.write("Enter decimal numbers")
                                elif param['type'] == 'bool':
                                    st.write("Use true/false or 1/0")
                                else:
                                    st.write("Enter text value")
                        
                        # Add separator between parameters
                        if i < len(param_list):
                            st.markdown("---")
            
            # Quick reference section
            st.markdown("---")
            st.subheader("📖 Quick Reference")
            
            # Summary in expandable section
            with st.expander("View command summary", expanded=False):
                st.markdown(f"""
                **Command:** `{selected_command}`  
                **Hex Code:** `{hex_code}`  
                **Parameters:** {len(param_list)} parameter(s)  
                **Description:** {description}
                """)
                
                if param_list:
                    st.markdown("**Parameter List:**")
                    for param in param_list:
                        param_info = f"• `{param['name']}` ({param['type']})"
                        if param['range']:
                            param_info += f" - Range: {param['range']}"
                        st.markdown(param_info)

except FileNotFoundError:
    st.error("❌ CSV files not found!")
    st.info("💡 **Solution:** Run `python generate_data.py` to create the required data files.")
    
    # Button to generate data
    if st.button("🔄 Generate Sample Data", type="primary"):
        with st.spinner("Generating sample data..."):
            try:
                exec(open('generate_data.py').read())
                st.success("✅ Sample data generated! Please refresh the page.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.info("💡 **Troubleshooting:**")
    st.markdown("""
    1. Make sure all CSV files exist in the current directory
    2. Check that CSV files have the correct format
    3. Try running `python generate_data.py` to recreate the files
    """)

