from skidl import *
import os
import urllib.request

# Create libraries directory if it doesn't exist
os.makedirs('libraries', exist_ok=True)

# Download the Device.kicad_sym file if it doesn't exist
device_lib_path = os.path.join('libraries', 'Device.kicad_sym')
if not os.path.exists(device_lib_path):
    url = "https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/Device.kicad_sym"
    urllib.request.urlretrieve(url, device_lib_path)

# Set the library search path to our local libraries directory
lib_search_paths_kicad = lib_search_paths_skidl = [os.path.abspath('libraries')]

# Set default tool to KiCad
set_default_tool(KICAD)

# Circuit description
circuit_name = 'RC_Filter'
circuit_description = 'Simple RC low-pass filter circuit'
default_circuit.name = circuit_name
default_circuit.description = circuit_description

# Power and ground
vcc = Net("VCC")
gnd = Net("GND")
out = Net("OUT")

# Components with footprints
r1 = Part("Device", "R", value="10k", footprint="Resistor_SMD:R_0805_2012Metric")
c1 = Part("Device", "C", value="0.1uF", footprint="Capacitor_SMD:C_0805_2012Metric")

# Connections
vcc += r1[1]
r1[2] += out
out += c1[1]
c1[2] += gnd

# Generate netlist with specific filename
generate_netlist(file_=f'{circuit_name}.net')

