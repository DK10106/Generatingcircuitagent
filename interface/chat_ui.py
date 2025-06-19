import streamlit as st
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'circuit_history' not in st.session_state:
        st.session_state.circuit_history = []

def generate_simple_circuit(description: str):
    """Generate a simple circuit response for demonstration"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    circuit_name = f"circuit_{timestamp}"
    
    # Create a simple response
    response = f"✅ Circuit generated successfully!\n\n"
    response += f"**Circuit Name:** {circuit_name}\n"
    response += f"**Description:** {description}\n"
    response += f"**Generated:** {timestamp}\n\n"
    response += "The circuit files have been saved to the `kicad_output` directory."
    
    return {
        'name': circuit_name,
        'description': description,
        'timestamp': timestamp,
        'response': response
    }

def main():
    st.set_page_config(
        page_title="KiCad AI Circuit Generator",
        page_icon="⚡",
        layout="wide"
    )
    
    st.title("⚡ KiCad AI Circuit Generator")
    st.markdown("Generate KiCad circuit files using natural language descriptions")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar for settings and history
    with st.sidebar:
        st.header("Settings")
        st.info("AI features coming soon!")
        
        # Circuit history
        st.header("Circuit History")
        if st.session_state.circuit_history:
            for i, circuit in enumerate(st.session_state.circuit_history):
                if st.button(f"{circuit['name']}", key=f"history_{i}"):
                    st.session_state.messages.append({
                        "role": "user",
                        "content": f"Show me the circuit: {circuit['description']}"
                    })
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": circuit['response']
                    })
        else:
            st.write("No circuits generated yet")
    
    # Main chat interface
    st.header("Chat Interface")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Describe the circuit you want to create..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Generating circuit..."):
                # Generate simple circuit response
                circuit_info = generate_simple_circuit(prompt)
                
                st.write(circuit_info['response'])
                
                # Add to circuit history
                st.session_state.circuit_history.append(circuit_info)
                
                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": circuit_info['response']
                })
    
    # Example prompts
    st.header("Example Prompts")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Voltage Divider"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Create a voltage divider that converts 5V to 3.3V"
            })
            st.rerun()
    
    with col2:
        if st.button("RC Filter"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Generate an RC low-pass filter with 1kHz cutoff frequency"
            })
            st.rerun()
    
    with col3:
        if st.button("LED Circuit"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Design a simple LED circuit with current limiting resistor"
            })
            st.rerun()

if __name__ == "__main__":
    main() 