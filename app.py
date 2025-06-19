import streamlit as st
from generate_circuit import (
    setup_kicad_env,
    create_voltage_divider,
    create_rc_low_pass_filter,
    create_led_circuit
)
import os

st.title("KiCad AI Circuit Generator")
st.write("Click a button below to generate a circuit design and download the KiCad schematic file.")

# Setup the environment once
setup_kicad_env()

# --- Circuit 1: Voltage Divider ---
st.header("1. Voltage Divider (5V to 3.3V)")
if st.button("Generate Voltage Divider"):
    st.info("Generating your voltage divider... please wait.")
    schematic_file = create_voltage_divider(vin=5.0, vout=3.3)
    st.session_state['voltage_divider_file'] = schematic_file

if 'voltage_divider_file' in st.session_state:
    file_path = st.session_state['voltage_divider_file']
    if os.path.exists(file_path):
        st.success("Voltage divider generated!")
        with open(file_path, "rb") as file:
            st.download_button(
                label="Download Schematic",
                data=file,
                file_name=os.path.basename(file_path),
                mime="application/octet-stream"
            )

# --- Circuit 2: RC Low-Pass Filter ---
st.header("2. RC Low-Pass Filter (1kHz Cutoff)")
if st.button("Generate RC Filter"):
    st.info("Generating your RC low-pass filter... please wait.")
    schematic_file = create_rc_low_pass_filter(cutoff_freq=1000)
    st.session_state['rc_filter_file'] = schematic_file

if 'rc_filter_file' in st.session_state:
    file_path = st.session_state['rc_filter_file']
    if os.path.exists(file_path):
        st.success("RC filter generated!")
        with open(file_path, "rb") as file:
            st.download_button(
                label="Download Schematic",
                data=file,
                file_name=os.path.basename(file_path),
                mime="application/octet-stream"
            )

# --- Circuit 3: Simple LED Circuit ---
st.header("3. Simple LED Circuit")
if st.button("Generate LED Circuit"):
    st.info("Generating your LED circuit... please wait.")
    schematic_file = create_led_circuit()
    st.session_state['led_circuit_file'] = schematic_file

if 'led_circuit_file' in st.session_state:
    file_path = st.session_state['led_circuit_file']
    if os.path.exists(file_path):
        st.success("LED circuit generated!")
        with open(file_path, "rb") as file:
            st.download_button(
                label="Download Schematic",
                data=file,
                file_name=os.path.basename(file_path),
                mime="application/octet-stream"
            ) 