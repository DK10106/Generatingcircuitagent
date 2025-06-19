import os
import json
import urllib.request
import subprocess
import shutil
import tempfile
import zipfile
from datetime import datetime
from skidl import *
from skidl.pyspice import *

def find_closest_e12_value(target_value):
    """Find the closest E12 resistor value"""
    e12_values = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
    
    # Handle different magnitudes
    magnitude = 1
    while target_value > 100:
        target_value /= 10
        magnitude *= 10
    while target_value < 10:
        target_value *= 10
        magnitude /= 10
    
    # Find closest E12 value
    closest = min(e12_values, key=lambda x: abs(x - target_value))
    return int(closest * magnitude)

def find_closest_capacitor_value(target_value):
    """Find the closest standard capacitor value"""
    standard_values = [0.1e-6, 1e-6, 10e-6, 100e-6, 1e-3]  # 0.1µF, 1µF, 10µF, 100µF, 1mF
    
    # Find closest standard value
    closest = min(standard_values, key=lambda x: abs(x - target_value))
    
    # Format for display
    if closest >= 1e-3:
        return f"{closest*1e3}mF"
    elif closest >= 1e-6:
        return f"{closest*1e6}µF"
    else:
        return f"{closest*1e9}nF"

def log(msg):
    """Log messages with timestamp"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def setup_kicad_env():
    """Setup KiCad environment and download required libraries"""
    print("[{}] Setting up KiCad environment...".format(datetime.now().strftime("%H:%M:%S")))
    
    try:
        # Add KiCad 9 bin directory to PATH if not already there
        kicad_bin_path = r"C:\Program Files\KiCad\9.0\bin"
        if os.path.exists(kicad_bin_path) and kicad_bin_path not in os.environ.get('PATH', ''):
            os.environ['PATH'] = kicad_bin_path + os.pathsep + os.environ.get('PATH', '')
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Added KiCad 9 bin to PATH")
        
        # Create libraries directory
        libraries_dir = os.path.join(os.getcwd(), 'libraries')
        os.makedirs(libraries_dir, exist_ok=True)
        
        # Required libraries with their URLs
        required_libs = {
            'Device.kicad_sym': 'https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/Device.kicad_sym',
            'power.kicad_sym': 'https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/power.kicad_sym',
            'LED.kicad_sym': 'https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/LED.kicad_sym'
        }
        
        # Download missing libraries
        for lib_name, lib_url in required_libs.items():
            lib_path = os.path.join(libraries_dir, lib_name)
            if not os.path.exists(lib_path):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Downloading {lib_name}...")
                try:
                    urllib.request.urlretrieve(lib_url, lib_path)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Downloaded {lib_name}")
                except Exception as e:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Failed to download {lib_name}: {e}")
                    return False
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ {lib_name} already exists")
        
        # Add the local libraries directory to skidl's search path
        from skidl import lib_search_paths
        if isinstance(lib_search_paths, list):
            lib_search_paths.append(os.path.abspath(libraries_dir))
        else:
            # If it's a dict, convert to list and add
            lib_search_paths = [os.path.abspath(libraries_dir)]
        
        # Set default tool to KiCad
        set_default_tool(KICAD)
        
        # Test library loading
        try:
            # Test if we can load a basic component
            test_resistor = Part("Device", "R")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ KiCad environment setup complete")
            return True
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Library test failed: {e}")
            return False
            
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ KiCad environment setup failed: {e}")
        return False

def create_kicad_project(circuit_name: str, output_dir: str) -> str:
    """Create a KiCad project file (.kicad_pro) that can be opened directly in KiCad"""
    project_file = os.path.join(output_dir, f"{circuit_name}.kicad_pro")
    
    # Create a basic KiCad project structure
    project_data = {
        "board": {
            "design_settings": {
                "defaults": {
                    "board_outline_line_width": 0.1,
                    "copper_line_width": 0.2,
                    "copper_text_italic": False,
                    "copper_text_size_h": 1.5,
                    "copper_text_size_v": 1.5,
                    "copper_text_thickness": 0.3,
                    "courtyard_line_width": 0.05,
                    "dimension_units": 3,
                    "dimensions": {
                        "suppress_zeroes": False,
                        "units_format": 1
                    },
                    "drill": {
                        "oval": False,
                        "shape": 0
                    },
                    "drill_shape": 0,
                    "drill_size": 0.6,
                    "edge_cut_line_width": 0.1,
                    "fab_line_width": 0.1,
                    "fab_text_italic": False,
                    "fab_text_size_h": 1.0,
                    "fab_text_size_v": 1.0,
                    "fab_text_thickness": 0.15,
                    "footprint_text_italic": False,
                    "footprint_text_size_h": 1.0,
                    "footprint_text_size_v": 1.0,
                    "footprint_text_thickness": 0.15,
                    "graphics_text_italic": False,
                    "graphics_text_size_h": 1.5,
                    "graphics_text_size_v": 1.5,
                    "graphics_text_thickness": 0.2,
                    "grid": {
                        "origin": {
                            "x": 0.0,
                            "y": 0.0
                        },
                        "size": {
                            "x": 1.0,
                            "y": 1.0
                        },
                        "style": 0,
                        "user_grid_x": 0.0,
                        "user_grid_y": 0.0
                    },
                    "pad_to_mask_clearance": 0.0,
                    "pad_to_paste_clearance": 0.0,
                    "pad_to_paste_clearance_ratio": 0.0,
                    "pcbplotparams": {
                        "aperture_lt": False,
                        "auto_scale": False,
                        "autoscale_plot": False,
                        "blackandwhite": False,
                        "check_zone_fills": False,
                        "create_reference_images": False,
                        "disableapertmacros": False,
                        "drillshape": 1,
                        "duplicate_layers": False,
                        "exclude_edge_layer": True,
                        "fine_plot": False,
                        "format": 1,
                        "gerber_job_file": "",
                        "gerber_plot_format": 0,
                        "gerber_precision": 4,
                        "hpgl_pen_number": 1,
                        "hpgl_pen_speed": 20,
                        "hpgl_plot_format": 0,
                        "layerselection": "0x00010fc_ffffffff",
                        "line_width": 0.0,
                        "mirror_plot": False,
                        "negative_plot": False,
                        "output_directory": "",
                        "plot_footprint_refs": True,
                        "plot_footprint_values": True,
                        "plot_invisible_text": False,
                        "plot_on_all_layers_selection": "0x00000000_ffffffff",
                        "plot_pad_numbers": False,
                        "plot_reference": True,
                        "plot_sheet_reference": False,
                        "plot_value": True,
                        "ps_color": False,
                        "ps_fine_plot": False,
                        "ps_negative_plot": False,
                        "scale_adjust_x": 1.0,
                        "scale_adjust_y": 1.0,
                        "sketch_plot": False,
                        "sketch_plot_inverted": False,
                        "subtract_mask_from_silk": False,
                        "svg_precision": 4,
                        "text_default_italic": False,
                        "text_default_size": 1.5,
                        "text_default_thickness": 0.3,
                        "text_default_upright": False,
                        "use_aux_axis_as_origin": False,
                        "use_gerber_attributes": False,
                        "use_gerber_extensions": False,
                        "use_gerber_netlist": False,
                        "use_gerber_x2format": True,
                        "use_project_dir": False,
                        "via_on_silk": False,
                        "width_adjust": 0.0
                    },
                    "silk_line_width": 0.2,
                    "silk_text_italic": False,
                    "silk_text_size_h": 1.0,
                    "silk_text_size_v": 1.0,
                    "silk_text_thickness": 0.15,
                    "solder_mask_clearance": 0.0,
                    "solder_mask_min_width": 0.0,
                    "text_italic": False,
                    "text_size_h": 1.5,
                    "text_size_v": 1.5,
                    "text_thickness": 0.2,
                    "text_upright": False,
                    "zone_45_only": False,
                    "zone_hatch_style": 0,
                    "zone_keep_fill": False,
                    "zone_outline_hatch_style": 0
                },
                "rules": {
                    "constraint": [],
                    "rule": []
                }
            },
            "layers": {
                "copper": {
                    "0": {
                        "name": "F.Cu",
                        "type": 0
                    },
                    "31": {
                        "name": "B.Cu",
                        "type": 0
                    }
                },
                "technical": {
                    "10": {
                        "name": "F.SilkS",
                        "type": 1
                    },
                    "11": {
                        "name": "B.SilkS",
                        "type": 1
                    },
                    "12": {
                        "name": "F.Paste",
                        "type": 2
                    },
                    "13": {
                        "name": "B.Paste",
                        "type": 2
                    },
                    "14": {
                        "name": "F.Mask",
                        "type": 3
                    },
                    "15": {
                        "name": "B.Mask",
                        "type": 3
                    },
                    "16": {
                        "name": "Dwgs.User",
                        "type": 4
                    },
                    "17": {
                        "name": "Cmts.User",
                        "type": 4
                    },
                    "18": {
                        "name": "Eco1.User",
                        "type": 4
                    },
                    "19": {
                        "name": "Eco2.User",
                        "type": 4
                    },
                    "20": {
                        "name": "Edge.Cuts",
                        "type": 5
                    },
                    "21": {
                        "name": "Margin",
                        "type": 6
                    },
                    "22": {
                        "name": "F.CrtYd",
                        "type": 7
                    },
                    "23": {
                        "name": "B.CrtYd",
                        "type": 7
                    },
                    "24": {
                        "name": "F.Fab",
                        "type": 8
                    },
                    "25": {
                        "name": "B.Fab",
                        "type": 8
                    }
                }
            },
            "setup": {
                "stackup": {
                    "dielectric": [
                        {
                            "color": "0.8 0.8 0.8 1.0",
                            "epsilon_r": 4.5,
                            "loss_tangent": 0.02,
                            "material": "FR4",
                            "thickness": 0.2
                        }
                    ],
                    "layer": [
                        {
                            "color": "0.7 0.7 0.7 1.0",
                            "name": "F.SilkS",
                            "number": 10,
                            "type": "signal"
                        },
                        {
                            "color": "0.9 0.9 0.9 1.0",
                            "name": "F.Paste",
                            "number": 12,
                            "type": "signal"
                        },
                        {
                            "color": "0.9 0.9 0.9 1.0",
                            "name": "F.Mask",
                            "number": 14,
                            "type": "signal"
                        },
                        {
                            "color": "0.8 0.8 0.8 1.0",
                            "name": "F.Cu",
                            "number": 0,
                            "type": "signal"
                        },
                        {
                            "color": "0.8 0.8 0.8 1.0",
                            "name": "B.Cu",
                            "number": 31,
                            "type": "signal"
                        },
                        {
                            "color": "0.9 0.9 0.9 1.0",
                            "name": "B.Mask",
                            "number": 15,
                            "type": "signal"
                        },
                        {
                            "color": "0.9 0.9 0.9 1.0",
                            "name": "B.Paste",
                            "number": 13,
                            "type": "signal"
                        },
                        {
                            "color": "0.7 0.7 0.7 1.0",
                            "name": "B.SilkS",
                            "number": 11,
                            "type": "signal"
                        }
                    ]
                }
            }
        },
        "sheets": [],
        "text_variables": {}
    }
    
    # Write the project file
    with open(project_file, 'w', encoding='utf-8') as f:
        json.dump(project_data, f, indent=2)
    
    log(f"✓ Created KiCad project file: {project_file}")
    return project_file

def create_voltage_divider(input_voltage: float = 5.0, output_voltage: float = 3.3, current: float = 0.001) -> dict:
    """Create a voltage divider circuit"""
    try:
        # Setup KiCad environment
        if not setup_kicad_env():
            return {"error": "Failed to setup KiCad environment"}
        
        # Calculate resistor values
        r2_value = output_voltage / current
        r1_value = (input_voltage - output_voltage) / current
        
        # Use standard E12 resistor values
        r1_standard = find_closest_e12_value(r1_value)
        r2_standard = find_closest_e12_value(r2_value)
        
        # Create circuit name
        circuit_name = f"voltage_divider_{input_voltage}v_{output_voltage}v"
        output_dir = os.path.join("kicad_output", "voltage_divider")
        os.makedirs(output_dir, exist_ok=True)
        
        # Create KiCad project file
        project_file = create_kicad_project(circuit_name, output_dir)
        
        # Create circuit using SKiDL
        # from skidl import *  # Already imported at top
        
        # Set up circuit
        default_circuit.name = circuit_name
        default_circuit.description = f"Voltage divider converting {input_voltage}V to {output_voltage}V"
        
        # Define nets with clear naming
        vcc = Net('VCC')      # Input voltage
        gnd = Net('GND')      # Ground
        out = Net('OUT')      # Output voltage
        
        # Create components
        r1 = Part("Device", "R", value=f"{r1_standard}Ω")
        r2 = Part("Device", "R", value=f"{r2_standard}Ω")
        
        # Set component properties
        r1.ref = "R1"
        r2.ref = "R2"
        
        # Connect in proper layout: VCC → R1 → OUT → R2 → GND
        vcc += r1[1]          # VCC connects to R1 pin 1
        r1[2] += out          # R1 pin 2 connects to output
        out += r2[1]          # Output connects to R2 pin 1
        r2[2] += gnd          # R2 pin 2 connects to ground
        
        # Generate netlist
        netlist_file = os.path.join(output_dir, f"{circuit_name}.net")
        log(f"Generating netlist: {netlist_file}")
        generate_netlist(file_=netlist_file)
        
        # NEW: convert netlist to KiCad project and create ZIP
        try:
            zip_path = net_to_project(netlist_file, output_dir)
            # Clean up the netlist file (optional - keep workspace clean)
            os.remove(netlist_file)
            
            generated_files = [zip_path]
            log(f"✓ Generated KiCad project ZIP: {zip_path}")
            log(f"✓ Voltage divider: {input_voltage}V → {output_voltage}V using R1={r1_standard}Ω, R2={r2_standard}Ω")
            
            return {
                "type": "voltage_divider",
                "name": circuit_name,
                "circuit_dir": output_dir,
                "generated_files": generated_files,
                "download_label": os.path.basename(zip_path),
                "download_path": zip_path,
                "response": f"✅ Circuit generated successfully! Voltage divider converting {input_voltage}V to {output_voltage}V using R1={r1_standard}Ω and R2={r2_standard}Ω",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            log(f"Error creating KiCad project: {e}")
            # Fallback to netlist if KiCad CLI fails
            generated_files = [netlist_file]
            return {
                "type": "voltage_divider",
                "name": circuit_name,
                "circuit_dir": output_dir,
                "generated_files": generated_files,
                "download_label": os.path.basename(netlist_file),
                "download_path": netlist_file,
                "response": f"✅ Circuit generated successfully! Voltage divider converting {input_voltage}V to {output_voltage}V using R1={r1_standard}Ω and R2={r2_standard}Ω (Netlist only - KiCad CLI not available)",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
    except Exception as e:
        log(f"Error creating voltage divider: {e}")
        return {"error": f"Failed to create voltage divider: {str(e)}"}

def create_rc_low_pass_filter(cutoff_freq: float = 1000.0) -> dict:
    """Create an RC low-pass filter circuit"""
    try:
        # Setup KiCad environment
        if not setup_kicad_env():
            return {"error": "Failed to setup KiCad environment"}
        
        # Calculate component values (assuming R = 10kΩ)
        r_value = 10000  # 10kΩ
        c_value = 1 / (2 * 3.14159 * cutoff_freq * r_value)  # C = 1/(2πfR)
        
        # Use standard capacitor value
        c_standard = find_closest_capacitor_value(c_value)
        
        # Create circuit name
        circuit_name = f"rc_low_pass_{cutoff_freq}hz"
        output_dir = os.path.join("kicad_output", "rc_low_pass_filter")
        os.makedirs(output_dir, exist_ok=True)
        
        # Create KiCad project file
        project_file = create_kicad_project(circuit_name, output_dir)
        
        # Create circuit using SKiDL
        # from skidl import *  # Already imported at top
        
        # Set up circuit
        default_circuit.name = circuit_name
        default_circuit.description = f"RC low-pass filter with {cutoff_freq}Hz cutoff frequency"
        
        # Define nets with clear naming
        vin = Net('VIN')      # Input signal
        vout = Net('VOUT')    # Output signal
        gnd = Net('GND')      # Ground
        
        # Create components
        r1 = Part("Device", "R", value=f"{r_value}Ω")
        c1 = Part("Device", "C", value=f"{c_standard}F")
        
        # Set component properties
        r1.ref = "R1"
        c1.ref = "C1"
        
        # Connect in proper layout: VIN → R → VOUT → C → GND
        vin += r1[1]          # Input connects to R pin 1
        r1[2] += vout         # R pin 2 connects to output
        vout += c1[1]         # Output connects to C pin 1
        c1[2] += gnd          # C pin 2 connects to ground
        
        # Generate netlist
        netlist_file = os.path.join(output_dir, f"{circuit_name}.net")
        log(f"Generating netlist: {netlist_file}")
        generate_netlist(file_=netlist_file)
        
        # NEW: convert netlist to KiCad project and create ZIP
        try:
            zip_path = net_to_project(netlist_file, output_dir)
            # Clean up the netlist file (optional - keep workspace clean)
            os.remove(netlist_file)
            
            generated_files = [zip_path]
            log(f"✓ Generated KiCad project ZIP: {zip_path}")
            log(f"✓ RC filter: {cutoff_freq}Hz cutoff using R={r_value}Ω, C={c_standard}F")
            
            return {
                "type": "rc_filter",
                "name": circuit_name,
                "circuit_dir": output_dir,
                "generated_files": generated_files,
                "download_label": os.path.basename(zip_path),
                "download_path": zip_path,
                "response": f"✅ Circuit generated successfully! RC low-pass filter with {cutoff_freq}Hz cutoff frequency using R={r_value}Ω and C={c_standard}F",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            log(f"Error creating KiCad project: {e}")
            # Fallback to netlist if KiCad CLI fails
            generated_files = [netlist_file]
            return {
                "type": "rc_filter",
                "name": circuit_name,
                "circuit_dir": output_dir,
                "generated_files": generated_files,
                "download_label": os.path.basename(netlist_file),
                "download_path": netlist_file,
                "response": f"✅ Circuit generated successfully! RC low-pass filter with {cutoff_freq}Hz cutoff frequency using R={r_value}Ω and C={c_standard}F (Netlist only - KiCad CLI not available)",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
    except Exception as e:
        log(f"Error creating RC filter: {e}")
        return {"error": f"Failed to create RC filter: {str(e)}"}

def create_led_circuit(voltage: float = 5.0, led_voltage: float = 2.0, led_current: float = 0.02) -> dict:
    """Create an LED circuit with current limiting resistor"""
    try:
        # Setup KiCad environment
        if not setup_kicad_env():
            return {"error": "Failed to setup KiCad environment"}
        
        # Calculate resistor value
        r_value = (voltage - led_voltage) / led_current
        
        # Use standard E12 resistor value
        r_standard = find_closest_e12_value(r_value)
        
        # Create circuit name
        circuit_name = f"led_circuit_{voltage}v"
        output_dir = os.path.join("kicad_output", "led_circuit")
        os.makedirs(output_dir, exist_ok=True)
        
        # Create KiCad project file
        project_file = create_kicad_project(circuit_name, output_dir)
        
        # Create circuit using SKiDL
        # from skidl import *  # Already imported at top
        
        # Set up circuit
        default_circuit.name = circuit_name
        default_circuit.description = f"LED circuit with {voltage}V supply"
        
        # Define nets with clear naming
        vcc = Net('VCC')      # Supply voltage
        gnd = Net('GND')      # Ground
        
        # Create components
        r1 = Part("Device", "R", value=f"{r_standard}Ω")
        led1 = Part("Device", "LED", value="LED")
        
        # Set component properties
        r1.ref = "R1"
        led1.ref = "D1"
        
        # Connect in proper layout: VCC → R → LED → GND
        vcc += r1[1]          # VCC connects to R pin 1
        r1[2] += led1[1]      # R pin 2 connects to LED anode
        led1[2] += gnd        # LED cathode connects to ground
        
        # Generate netlist
        netlist_file = os.path.join(output_dir, f"{circuit_name}.net")
        log(f"Generating netlist: {netlist_file}")
        generate_netlist(file_=netlist_file)
        
        # NEW: convert netlist to KiCad project and create ZIP
        try:
            zip_path = net_to_project(netlist_file, output_dir)
            # Clean up the netlist file (optional - keep workspace clean)
            os.remove(netlist_file)
            
            generated_files = [zip_path]
            log(f"✓ Generated KiCad project ZIP: {zip_path}")
            log(f"✓ LED circuit: {voltage}V supply with R={r_standard}Ω current limiting")
            
            return {
                "type": "led_circuit",
                "name": circuit_name,
                "circuit_dir": output_dir,
                "generated_files": generated_files,
                "download_label": os.path.basename(zip_path),
                "download_path": zip_path,
                "response": f"✅ Circuit generated successfully! LED circuit with {voltage}V supply using R={r_standard}Ω current limiting resistor",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            log(f"Error creating KiCad project: {e}")
            # Fallback to netlist if KiCad CLI fails
            generated_files = [netlist_file]
            return {
                "type": "led_circuit",
                "name": circuit_name,
                "circuit_dir": output_dir,
                "generated_files": generated_files,
                "download_label": os.path.basename(netlist_file),
                "download_path": netlist_file,
                "response": f"✅ Circuit generated successfully! LED circuit with {voltage}V supply using R={r_standard}Ω current limiting resistor (Netlist only - KiCad CLI not available)",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
    except Exception as e:
        log(f"Error creating LED circuit: {e}")
        return {"error": f"Failed to create LED circuit: {str(e)}"}

def net_to_project(net_path: str, export_dir: str) -> str:
    """
    Convert SKiDL netlist to a minimal KiCad project ( .kicad_pro + .kicad_sch )
    Since KiCad 9 CLI doesn't support import-netlist, we create a basic project structure.
    Return path to a zipped project for download.
    """
    try:
        # Ensure KiCad CLI is in PATH
        kicad_bin_path = r"C:\Program Files\KiCad\9.0\bin"
        if os.path.exists(kicad_bin_path) and kicad_bin_path not in os.environ.get('PATH', ''):
            os.environ['PATH'] = kicad_bin_path + os.pathsep + os.environ.get('PATH', '')
        
        base = os.path.splitext(os.path.basename(net_path))[0]
        proj_dir = os.path.join(export_dir, base)
        os.makedirs(proj_dir, exist_ok=True)

        # Create project file
        project_file = os.path.join(proj_dir, f"{base}.kicad_pro")
        create_kicad_project(base, proj_dir)
        
        # Copy the netlist to the project directory
        netlist_dest = os.path.join(proj_dir, f"{base}.net")
        shutil.copy2(net_path, netlist_dest)
        
        # Create a basic schematic file (empty for now, user can import netlist manually)
        schematic_file = os.path.join(proj_dir, f"{base}.kicad_sch")
        with open(schematic_file, 'w') as f:
            f.write('(kicad_sch (version 20221018) (generator eeschema)\n')
            f.write('  (paper "A4")\n')
            f.write('  (lib_symbols)\n')
            f.write('  (sheet_instances)\n')
            f.write('  (symbol (lib_id "power:GND") (at 0 0 0) (property "Reference" "GND" (at 0 -2.54 0) (effects (font (size 1.27 1.27)))))\n')
            f.write(')\n')

        # 3) Zip project for download
        zip_path = os.path.join(export_dir, f"{base}.kicad_project.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(proj_dir):
                for f in files:
                    fp = os.path.join(root, f)
                    zf.write(fp, arcname=os.path.relpath(fp, proj_dir))
        
        log(f"✓ Created KiCad project ZIP: {zip_path}")
        return zip_path
        
    except FileNotFoundError:
        raise Exception("❌ KiCad CLI not found – install KiCad 7+ or make it reachable in PATH.")
    except subprocess.CalledProcessError as e:
        raise Exception(f"❌ KiCad CLI error: {str(e)}")
    except Exception as e:
        raise Exception(f"❌ Error creating project: {str(e)}")

class CircuitGenerator:
    def __init__(self):
        self.setup_kicad_environment()
    
    def setup_kicad_environment(self):
        """Setup KiCad environment"""
        return setup_kicad_env()
    
    def generate_voltage_divider(self, input_voltage=5.0, output_voltage=3.3):
        """Generate voltage divider circuit"""
        return create_voltage_divider(input_voltage, output_voltage)
    
    def generate_rc_filter(self, cutoff_freq=1000.0):
        """Generate RC low-pass filter circuit"""
        return create_rc_low_pass_filter(cutoff_freq)
    
    def generate_led_circuit(self, voltage=5.0):
        """Generate LED circuit"""
        return create_led_circuit(voltage)
    
    def generate_custom_circuit(self, user_request: str):
        """Generate custom circuit using LLM"""
        try:
            # Import LLM engine
            from llm_engine import LLMEngine
            
            # Initialize LLM engine
            llm_engine = LLMEngine()
            
            # If voltage divider requested
            if 'voltage_divider' in user_request:
                return create_voltage_divider(input_voltage=5.0, output_voltage=3.3)
            
            # Generate circuit using LLM
            result = llm_engine.generate_and_execute_circuit(user_request)
            
            if result and 'error' not in result:
                return result
            else:
                return {"error": result.get('error', 'Failed to generate custom circuit')}
                
        except Exception as e:
            return {"error": f"Error generating custom circuit: {str(e)}"}

if __name__ == "__main__":
    # Set up KiCad environment
    setup_kicad_env()
    
    # Create a voltage divider (5V to 3.3V)
    netlist, project, schematic = create_voltage_divider(input_voltage=5.0, output_voltage=3.3)
    
    log("\nTo use these files in KiCad:")
    log("1. Open KiCad")
    log("2. Click 'File' -> 'Open Project'")
    log(f"3. Navigate to: {os.path.dirname(project)}")
    log(f"4. Open {os.path.basename(project)}")
    log("5. The schematic and netlist will be loaded automatically") 