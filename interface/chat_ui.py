import streamlit as st
import os
import sys
from datetime import datetime
import json

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from circuit_generator import CircuitGenerator
from llm_engine import LLMEngine
from generate_circuit import setup_kicad_env

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'circuit_history' not in st.session_state:
        st.session_state.circuit_history = []
    if 'llm_engine' not in st.session_state:
        st.session_state.llm_engine = None
    if 'circuit_generator' not in st.session_state:
        st.session_state.circuit_generator = None

def setup_kicad_environment():
    """Setup KiCad environment"""
    try:
        setup_kicad_env()
        return True
    except Exception as e:
        st.error(f"Error setting up KiCad environment: {str(e)}")
        return False

def initialize_llm_engine():
    """Initialize the LLM engine"""
    if st.session_state.llm_engine is None:
        try:
            st.session_state.llm_engine = LLMEngine()
            return True
        except Exception as e:
            st.error(f"Error initializing LLM engine: {str(e)}")
            return False
    return True

def initialize_circuit_generator():
    """Initialize the circuit generator"""
    try:
        if 'circuit_generator' not in st.session_state:
            from generate_circuit import CircuitGenerator
            st.session_state.circuit_generator = CircuitGenerator()
        return True
    except Exception as e:
        st.error(f"Failed to initialize circuit generator: {str(e)}")
        return False

def generate_circuit_from_llm(user_request: str):
    """Generate circuit using LLM"""
    try:
        # Initialize circuit generator if not already done
        if not initialize_circuit_generator():
            st.error("Failed to initialize circuit generator")
            return None
        
        # Get the circuit generator from session state
        circuit_generator = st.session_state.circuit_generator
        if not circuit_generator:
            st.error("Circuit generator not available")
            return None
        
        # Generate custom circuit using LLM
        result = circuit_generator.generate_custom_circuit(user_request)
        
        if result and 'error' not in result:
            # Add to circuit history
            st.session_state.circuit_history.append(result)
            return result
        else:
            error_msg = result.get('error', 'Failed to generate circuit') if result else 'Failed to generate circuit'
            st.error(f"Error generating circuit: {error_msg}")
            return None
            
    except Exception as e:
        st.error(f"Error generating circuit: {str(e)}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")
        return None

def generate_simple_circuit(circuit_type: str):
    """Generate a simple circuit based on type"""
    try:
        # Initialize circuit generator (this sets up the environment)
        if not initialize_circuit_generator():
            st.error("Failed to initialize circuit generator")
            return None
        
        # Import circuit creation functions directly
        from generate_circuit import create_voltage_divider, create_rc_low_pass_filter, create_led_circuit
        
        # Generate circuit based on type
        if circuit_type == "voltage_divider":
            result = create_voltage_divider(input_voltage=5.0, output_voltage=3.3)
        elif circuit_type == "rc_filter":
            result = create_rc_low_pass_filter(1000.0)
        elif circuit_type == "led_circuit":
            result = create_led_circuit(5.0)
        else:
            st.error(f"Unknown circuit type: {circuit_type}")
            return None
        
        # Check for errors
        if 'error' in result:
            st.error(f"Failed to generate circuit: {result['error']}")
            return None
        
        # Add to circuit history
        st.session_state.circuit_history.append(result)
        
        return result
        
    except Exception as e:
        st.error(f"Error generating circuit: {str(e)}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")
        return None

def display_circuit_info(circuit_info, inside_expander=False):
    """Display circuit information and provide download links for all generated files"""
    if circuit_info and 'generated_files' in circuit_info:
        generated_files = circuit_info['generated_files']
        circuit_dir = circuit_info.get('circuit_dir', '')
        
        st.subheader("📁 Generated Files")
        if circuit_dir:
            st.write(f"**Circuit Directory:** {circuit_dir}")
        st.write(f"**Total Files:** {len(generated_files)}")
        
        # Display the main download file (ZIP or fallback)
        if generated_files:
            main_file = generated_files[0]
            if os.path.exists(main_file):
                file_name = os.path.basename(main_file)
                
                # Determine file type and description
                if file_name.endswith('.kicad_project.zip'):
                    file_type = "KiCad Project"
                    file_description = "Complete KiCad project with schematic (.kicad_sch) and project file (.kicad_pro)"
                    mime_type = "application/zip"
                elif file_name.endswith('.net'):
                    file_type = "Netlist"
                    file_description = "Component connection netlist (fallback - KiCad CLI not available)"
                    mime_type = "text/plain"
                else:
                    file_type = "Circuit File"
                    file_description = "Generated circuit file"
                    mime_type = "application/octet-stream"
                
                try:
                    with open(main_file, 'rb') as f:
                        file_content = f.read()
                    
                    # Create download button
                    download_label = circuit_info.get('download_label', file_name)
                    st.download_button(
                        label=f"📥 Download {download_label}",
                        data=file_content,
                        file_name=download_label,
                        mime=mime_type,
                        key=f"download_{file_name}_{circuit_info['timestamp']}"
                    )
                    
                    # Show file info
                    st.write(f"**File Type:** {file_type}")
                    st.write(f"**Description:** {file_description}")
                    st.write(f"**Size:** {os.path.getsize(main_file)} bytes")
                    
                    # Show usage instructions
                    if not inside_expander:
                        if file_name.endswith('.kicad_project.zip'):
                            with st.expander("📋 How to use this KiCad project"):
                                st.markdown("""
                                **To use this KiCad project:**
                                
                                1. **Download and extract** the ZIP file
                                2. **Open KiCad** (version 7 or later)
                                3. **File → Open Project** → Select the `.kicad_pro` file
                                4. **Double-click** the `.kicad_pro` file to open directly
                                5. **View the schematic** in the Schematic Editor
                                6. **Create PCB** from the schematic if needed
                                
                                **Note:** This is a complete KiCad project with both schematic and project files.
                                """)
                        elif file_name.endswith('.net'):
                            st.markdown("**Note:** This is a netlist file. Install KiCad CLI to get full schematic projects.")
                    else:
                        # Show condensed instructions when inside expander
                        if file_name.endswith('.kicad_project.zip'):
                            st.markdown("**Usage:** Extract ZIP → Open `.kicad_pro` in KiCad → View schematic")
                        elif file_name.endswith('.net'):
                            st.markdown("**Note:** Netlist file - KiCad CLI needed for full projects")
                    
                except Exception as e:
                    st.error(f"Error reading file {file_name}: {str(e)}")
            else:
                st.warning(f"File not found: {main_file}")
        
        # Show circuit details
        st.subheader("🔧 Circuit Details")
        if circuit_info['type'] == 'voltage_divider':
            st.write("**Type:** Voltage Divider")
            st.write("**Purpose:** Converts higher voltage to lower voltage")
            st.write("**Components:** 2 Resistors")
            st.write("**Use Case:** Logic level conversion, sensor interfacing")
        elif circuit_info['type'] == 'rc_filter':
            st.write("**Type:** RC Low-Pass Filter")
            st.write("**Purpose:** Filters high-frequency signals")
            st.write("**Components:** 1 Resistor, 1 Capacitor")
            st.write("**Use Case:** Signal conditioning, noise reduction")
        elif circuit_info['type'] == 'led_circuit':
            st.write("**Type:** LED Circuit")
            st.write("**Purpose:** Drives an LED with current limiting")
            st.write("**Components:** 1 Resistor, 1 LED")
            st.write("**Use Case:** Status indicators, lighting")
        elif circuit_info['type'] == 'ai_generated':
            st.write("**Type:** AI-Generated Circuit")
            st.write("**Purpose:** Custom circuit based on user request")
            st.write("**Generated by:** LLM with SKiDL")
            st.write("**Use Case:** Custom electronics projects")
            
            # Show AI-generated code if available - only if not inside expander
            if circuit_info.get('ai_code') and not inside_expander:
                with st.expander("🤖 View AI-Generated Code"):
                    st.code(circuit_info['ai_code'], language='python')
            elif circuit_info.get('ai_code'):
                st.markdown("**AI-Generated Code:** Available (view in main chat)")
        
        # Show timestamp
        st.write(f"**Generated:** {circuit_info['timestamp']}")

def main():
    st.set_page_config(
        page_title="KiCad AI Circuit Generator",
        page_icon="⚡",
        layout="wide"
    )
    
    st.title("⚡ KiCad AI Circuit Generator")
    st.markdown("Generate electronic circuits using AI and download KiCad files!")
    
    # Initialize session state
    initialize_session_state()
    
    # Setup KiCad environment
    if setup_kicad_environment():
        st.success("✅ KiCad environment ready")
    
    # Sidebar for quick circuit generation
    with st.sidebar:
        st.header("🚀 Quick Generate")
        st.markdown("Generate common circuits instantly:")
        
        if st.button("🔌 Voltage Divider (5V→3.3V)"):
            circuit_info = generate_simple_circuit("voltage_divider")
            if circuit_info:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": circuit_info['response']
                })
                st.rerun()
        
        if st.button("🔊 RC Low-Pass Filter (1kHz)"):
            circuit_info = generate_simple_circuit("rc_filter")
            if circuit_info:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": circuit_info['response']
                })
                st.rerun()
        
        if st.button("💡 LED Circuit"):
            circuit_info = generate_simple_circuit("led_circuit")
            if circuit_info:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": circuit_info['response']
                })
                st.rerun()
        
        st.markdown("---")
        st.markdown("**Or use AI to generate custom circuits!**")
    
    # Main chat interface
    st.header("💬 AI Circuit Generator")
    st.markdown("Describe any circuit you want to create, and AI will generate it for you!")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # If this is an assistant message with circuit info, show download links
            if message["role"] == "assistant" and "✅ Circuit generated successfully" in message["content"]:
                # Find the corresponding circuit info
                for circuit_info in st.session_state.circuit_history:
                    if circuit_info['response'] == message["content"]:
                        display_circuit_info(circuit_info)
                        break
    
    # Chat input
    if prompt := st.chat_input("Describe the circuit you want to create..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response using AI
        with st.chat_message("assistant"):
            with st.spinner("🤖 AI is thinking..."):
                circuit_info = generate_circuit_from_llm(prompt)
                
                if circuit_info:
                    st.markdown(circuit_info['response'])
                    display_circuit_info(circuit_info)
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": circuit_info['response']
                    })
                else:
                    error_msg = "❌ Sorry, I couldn't generate that circuit. Please try a different description."
                    st.markdown(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    
    # Circuit history
    if st.session_state.circuit_history:
        st.header("📚 Circuit History")
        for i, circuit_info in enumerate(reversed(st.session_state.circuit_history)):
            with st.expander(f"🔧 {circuit_info['name']} - {circuit_info['timestamp']}"):
                st.markdown(circuit_info['response'])
                display_circuit_info(circuit_info, inside_expander=True)

if __name__ == "__main__":
    main() 