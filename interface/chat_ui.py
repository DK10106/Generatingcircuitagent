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
    if st.session_state.circuit_generator is None:
        try:
            st.session_state.circuit_generator = CircuitGenerator()
            return True
        except Exception as e:
            st.error(f"Error initializing circuit generator: {str(e)}")
            return False
    return True

def generate_circuit_from_llm(user_request: str):
    """Generate circuit using LLM and execute the code"""
    try:
        # Initialize LLM engine if not already done
        if not initialize_llm_engine():
            return None
            
        with st.spinner("🤖 AI is generating circuit code..."):
            # Use LLM to generate and execute circuit code
            result = st.session_state.llm_engine.generate_and_execute_circuit(user_request)
            
            if result['success']:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                circuit_name = result['circuit_name']
                
                # Create response
                response = f"✅ Circuit generated successfully using AI!\n\n"
                response += f"**Circuit Name:** {circuit_name}\n"
                response += f"**Description:** {user_request}\n"
                response += f"**Generated:** {timestamp}\n"
                response += f"**Files Created:** {len(result['generated_files'])} files\n\n"
                response += f"**AI Response:**\n{result['message']}\n\n"
                
                if result['generated_files']:
                    response += f"Circuit files have been saved to: `{os.path.dirname(result['generated_files'][0])}`"
                
                # Add to circuit history
                circuit_info = {
                    'name': circuit_name,
                    'type': 'ai_generated',
                    'description': user_request,
                    'timestamp': timestamp,
                    'circuit_dir': os.path.dirname(result['generated_files'][0]) if result['generated_files'] else '',
                    'generated_files': result['generated_files'],
                    'response': response,
                    'ai_code': result.get('code', ''),
                    'ai_response': result.get('response', '')
                }
                st.session_state.circuit_history.append(circuit_info)
                
                return circuit_info
            else:
                st.error(f"❌ Circuit generation failed: {result['message']}")
                if result.get('response'):
                    st.text_area("AI Response:", result['response'], height=200)
                return None
            
    except Exception as e:
        st.error(f"Error generating circuit: {str(e)}")
        return None

def generate_simple_circuit(circuit_type: str):
    """Generate a simple circuit using predefined functions"""
    try:
        # Initialize CircuitGenerator if not already done
        if not initialize_circuit_generator():
            return None
            
        with st.spinner("Generating circuit..."):
            if circuit_type == "voltage_divider":
                from generate_circuit import create_voltage_divider
                schematic_file = create_voltage_divider(5.0, 3.3)
            elif circuit_type == "rc_filter":
                from generate_circuit import create_rc_low_pass_filter
                schematic_file = create_rc_low_pass_filter(1000)
            elif circuit_type == "led_circuit":
                from generate_circuit import create_led_circuit
                schematic_file = create_led_circuit(5.0, 2.0, 0.020)
            else:
                st.error(f"Unknown circuit type: {circuit_type}")
                return None
            
            # Check for generated files - look for both .net and .kicad_sch
            generated_files = []
            circuit_dir = ""
            circuit_name = ""
            
            if schematic_file:
                circuit_dir = os.path.dirname(schematic_file)
                circuit_name = os.path.basename(schematic_file).replace('.kicad_sch', '')
                
                # Check for netlist file (this should always exist)
                netlist_file = os.path.join(circuit_dir, f"{circuit_name}.net")
                if os.path.exists(netlist_file):
                    generated_files.append(netlist_file)
                
                # Check for project file (should exist now)
                project_file = os.path.join(circuit_dir, f"{circuit_name}.kicad_pro")
                if os.path.exists(project_file):
                    generated_files.append(project_file)
                
                # Check for schematic file (may not exist with KiCad 8)
                if os.path.exists(schematic_file):
                    generated_files.append(schematic_file)
            
            if generated_files:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Create response
                response = f"✅ {circuit_type.replace('_', ' ').title()} generated successfully!\n\n"
                response += f"**Circuit Type:** {circuit_type.replace('_', ' ').title()}\n"
                response += f"**Circuit Name:** {circuit_name}\n"
                response += f"**Generated:** {timestamp}\n"
                response += f"**Files Created:** {len(generated_files)} files\n"
                
                for file_path in generated_files:
                    response += f"**File:** {os.path.basename(file_path)}\n"
                
                # Add to circuit history
                circuit_info = {
                    'name': circuit_name,
                    'type': circuit_type,
                    'description': f"Generated {circuit_type}",
                    'timestamp': timestamp,
                    'circuit_dir': circuit_dir,
                    'generated_files': generated_files,
                    'response': response
                }
                st.session_state.circuit_history.append(circuit_info)
                
                return circuit_info
            else:
                st.error("Failed to generate circuit files")
                st.error(f"Expected files in: {circuit_dir}")
                st.error(f"Circuit name: {circuit_name}")
                return None
            
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
        
        # Separate files by type
        netlist_files = [f for f in generated_files if f.endswith('.net')]
        schematic_files = [f for f in generated_files if f.endswith('.kicad_sch')]
        project_files = [f for f in generated_files if f.endswith('.kicad_pro')]
        
        # Display netlist files
        if netlist_files:
            st.markdown("### 🔌 Netlist Files (.net)")
            st.info("**Netlist files** contain component connections and can be imported into KiCad projects. They are NOT schematic files.")
            
            for file_path in netlist_files:
                if os.path.exists(file_path):
                    file_name = os.path.basename(file_path)
                    
                    # Read file content
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        
                        # Create download button
                        st.download_button(
                            label=f"📥 Download {file_name} (Netlist)",
                            data=file_content,
                            file_name=file_name,
                            mime="text/plain",
                            key=f"download_{file_name}_{circuit_info['timestamp']}"
                        )
                        
                        # Show file info
                        st.write(f"**{file_name}** - {os.path.getsize(file_path)} bytes")
                        
                        # Show import instructions - only if not inside an expander
                        if not inside_expander:
                            with st.expander(f"📋 How to import {file_name} into KiCad"):
                                st.markdown("""
                                **To import this netlist into KiCad:**
                                
                                1. **Create a new KiCad project:**
                                   - Open KiCad
                                   - File → New Project → New Project
                                   - Choose a location and name
                                
                                2. **Import the netlist:**
                                   - Open the Schematic Editor
                                   - Tools → Update PCB from Schematic
                                   - Or: Tools → Import Netlist
                                   - Select this `.net` file
                                
                                3. **Alternative method:**
                                   - Open PCB Editor
                                   - File → Import → Netlist
                                   - Select this `.net` file
                                
                                **Note:** The netlist contains component connections but you'll need to create the schematic manually or use the PCB editor directly.
                                """)
                        else:
                            # Show instructions inline when inside expander
                            st.markdown("**Import instructions:** Create new KiCad project → Schematic Editor → Tools → Import Netlist → Select this file")
                        
                    except Exception as e:
                        st.error(f"Error reading file {file_name}: {str(e)}")
                else:
                    st.warning(f"File not found: {file_path}")
        
        # Display schematic files
        if schematic_files:
            st.markdown("### 🎨 Schematic Files (.kicad_sch)")
            st.success("**Schematic files** can be opened directly in KiCad Schematic Editor.")
            
            for file_path in schematic_files:
                if os.path.exists(file_path):
                    file_name = os.path.basename(file_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        
                        st.download_button(
                            label=f"📥 Download {file_name} (Schematic)",
                            data=file_content,
                            file_name=file_name,
                            mime="application/octet-stream",
                            key=f"download_{file_name}_{circuit_info['timestamp']}"
                        )
                        
                        st.write(f"**{file_name}** - {os.path.getsize(file_path)} bytes")
                        
                    except Exception as e:
                        st.error(f"Error reading file {file_name}: {str(e)}")
                else:
                    st.warning(f"File not found: {file_path}")
        
        # Display project files
        if project_files:
            st.markdown("### 📁 Project Files (.kicad_pro)")
            st.success("**Project files** can be opened directly in KiCad.")
            
            for file_path in project_files:
                if os.path.exists(file_path):
                    file_name = os.path.basename(file_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        
                        st.download_button(
                            label=f"📥 Download {file_name} (Project)",
                            data=file_content,
                            file_name=file_name,
                            mime="application/json",
                            key=f"download_{file_name}_{circuit_info['timestamp']}"
                        )
                        
                        st.write(f"**{file_name}** - {os.path.getsize(file_path)} bytes")
                        
                    except Exception as e:
                        st.error(f"Error reading file {file_name}: {str(e)}")
                else:
                    st.warning(f"File not found: {file_path}")
        
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
        
        # Add KiCad import instructions - only if not inside expander
        if netlist_files and not inside_expander:
            st.subheader("📋 KiCad Import Instructions")
            st.markdown("""
            **To use these files in KiCad:**
            
            **Option 1: Import Netlist (Recommended)**
            1. Create a new KiCad project
            2. Open Schematic Editor
            3. Tools → Import Netlist → Select the `.net` file
            4. Components will be placed on the schematic
            
            **Option 2: Direct PCB Import**
            1. Create a new KiCad project
            2. Open PCB Editor
            3. File → Import → Netlist → Select the `.net` file
            4. Components will be placed on the PCB
            
            **Note:** Netlist files contain component connections but not visual layout. You may need to arrange components manually.
            """)

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