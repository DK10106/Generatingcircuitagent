from skidl import *
import os
import urllib.request
from datetime import datetime
import json

def log(msg):
    """Log messages with timestamp"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def setup_kicad_env():
    """Setup KiCad environment and download required libraries"""
    log("Setting up KiCad environment...")
    
    # Create libraries directory
    libraries_dir = os.path.join(os.getcwd(), 'libraries')
    os.makedirs(libraries_dir, exist_ok=True)
    
    # Download required KiCad libraries
    required_libs = {
        'Device.kicad_sym': 'https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/Device.kicad_sym',
        'power.kicad_sym': 'https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/power.kicad_sym',
        'LED.kicad_sym': 'https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/LED.kicad_sym'
    }
    
    for lib_name, lib_url in required_libs.items():
        lib_path = os.path.join(libraries_dir, lib_name)
        if not os.path.exists(lib_path):
            log(f"Downloading {lib_name}...")
            urllib.request.urlretrieve(lib_url, lib_path)
            log(f"✓ Downloaded {lib_name}")
    
    # Set up library search paths
    lib_search_paths_kicad = lib_search_paths_skidl = [os.path.abspath(libraries_dir)]
    
    # Set environment variables
    os.environ['KICAD_SYMBOL_DIR'] = os.path.abspath(libraries_dir)
    os.environ['KICAD6_SYMBOL_DIR'] = os.path.abspath(libraries_dir)
    os.environ['KICAD7_SYMBOL_DIR'] = os.path.abspath(libraries_dir)
    os.environ['KICAD8_SYMBOL_DIR'] = os.path.abspath(libraries_dir)
    
    # Set default tool
    set_default_tool(KICAD)
    log("✓ KiCad environment setup complete")

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

def create_voltage_divider(vin=5.0, vout=3.3):
    """Create a voltage divider circuit with proper horizontal layout and return the schematic file path."""
    # Calculate resistor values for voltage divider
    # Using R1 = 10k, calculate R2 for desired output voltage
    r1_value = 10000  # 10k resistor
    r2_value = int(r1_value * (vout / (vin - vout)))
    
    # Create output directory
    output_dir = os.path.join(os.getcwd(), 'kicad_output', 'voltage_divider')
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up circuit with descriptive name
    circuit_name = f'voltage_divider_{int(vin)}v_{int(vout*10)}v'
    default_circuit.name = circuit_name
    default_circuit.description = f"Voltage divider converting {vin}V to {vout}V using {r1_value/1000}k and {r2_value/1000}k resistors"
    
    # Define nets with clear naming
    vcc = Net('VCC')      # Input voltage (5V)
    gnd = Net('GND')      # Ground (0V)
    out = Net('OUT')      # Output voltage (3.3V)
    
    # Create components with proper footprints
    r1 = Part("Device", "R", value=f"{r1_value}", footprint="Resistor_SMD:R_0805_2012Metric")
    r2 = Part("Device", "R", value=f"{r2_value}", footprint="Resistor_SMD:R_0805_2012Metric")
    
    # Set component properties for better identification
    r1.ref = "R1"
    r2.ref = "R2"
    r1.value = f"{r1_value}"
    r2.value = f"{r2_value}"
    
    # Connect components in proper voltage divider layout: VCC → R1 → OUT → R2 → GND
    # This creates a horizontal layout that's easy to read
    vcc += r1[1]          # VCC connects to R1 pin 1
    r1[2] += out          # R1 pin 2 connects to output
    out += r2[1]          # Output connects to R2 pin 1
    r2[2] += gnd          # R2 pin 2 connects to ground
    
    # Generate KiCad files
    netlist_file = os.path.join(output_dir, f"{circuit_name}.net")
    log(f"Generating netlist: {netlist_file}")
    generate_netlist(file_=netlist_file)
    
    # Create KiCad project file
    project_file = create_kicad_project(circuit_name, output_dir)
    
    # Create schematic file 
    schematic_file = os.path.join(output_dir, f"{circuit_name}.kicad_sch")
    generate_schematic(file_=schematic_file)
    
    log(f"✓ Generated KiCad files in: {output_dir}")
    log(f"✓ Voltage divider: {vin}V → {vout}V using R1={r1_value}Ω, R2={r2_value}Ω")
    return schematic_file

def create_rc_low_pass_filter(cutoff_freq=1000):
    """Create an RC low-pass filter with proper horizontal layout and return the schematic file path."""
    # Calculate component values for RC low-pass filter
    # Cutoff frequency: f = 1/(2πRC)
    # Using C = 0.1µF, calculate R for desired cutoff frequency
    c_value = 0.1e-6  # 0.1µF capacitor
    r_value = int(1 / (2 * 3.14159 * cutoff_freq * c_value))

    output_dir = os.path.join(os.getcwd(), 'kicad_output', 'rc_low_pass_filter')
    os.makedirs(output_dir, exist_ok=True)
    
    circuit_name = f'rc_low_pass_{cutoff_freq}hz'
    default_circuit.name = circuit_name
    default_circuit.description = f"RC Low-Pass Filter with {cutoff_freq}Hz cutoff using {r_value}Ω and {c_value*1e6}µF"
    
    # Define nets with clear naming
    vin = Net('VIN')      # Input signal
    vout = Net('VOUT')    # Output signal (filtered)
    gnd = Net('GND')      # Ground reference
    
    # Create components with proper footprints
    r = Part('Device', 'R', value=f'{r_value} Ohms', footprint='Resistor_SMD:R_0805_2012Metric')
    c = Part('Device', 'C', value=f'{c_value*1e6}µF', footprint='Capacitor_SMD:C_0805_2012Metric')
    
    # Set component properties for better identification
    r.ref = "R1"
    c.ref = "C1"
    r.value = f"{r_value}Ω"
    c.value = f"{c_value*1e6}µF"
    
    # Connect components in proper RC filter layout: VIN → R → VOUT → C → GND
    # This creates a horizontal layout: Input → Resistor → Output → Capacitor → Ground
    vin += r[1]           # Input connects to resistor pin 1
    r[2] += vout          # Resistor pin 2 connects to output
    vout += c[1]          # Output connects to capacitor pin 1
    gnd += c[2]           # Ground connects to capacitor pin 2

    # Generate KiCad files
    netlist_file = os.path.join(output_dir, f"{circuit_name}.net")
    log(f"Generating netlist: {netlist_file}")
    generate_netlist(file_=netlist_file)
    
    # Create KiCad project file
    project_file = create_kicad_project(circuit_name, output_dir)
    
    # Create schematic file 
    schematic_file = os.path.join(output_dir, f"{circuit_name}.kicad_sch")
    generate_schematic(file_=schematic_file)
    
    log(f"✓ Generated KiCad files in: {output_dir}")
    log(f"✓ RC filter: {cutoff_freq}Hz cutoff using R={r_value}Ω, C={c_value*1e6}µF")
    return schematic_file

def create_led_circuit(v_source=5.0, v_led=2.0, i_led=0.020):
    """Create a simple LED circuit with current limiting resistor and proper horizontal layout."""
    # Calculate the current-limiting resistor value
    # R = (V_source - V_LED) / I_LED
    r_value = int((v_source - v_led) / i_led)
    
    output_dir = os.path.join(os.getcwd(), 'kicad_output', 'led_circuit')
    os.makedirs(output_dir, exist_ok=True)

    circuit_name = 'simple_led_circuit'
    default_circuit.name = circuit_name
    default_circuit.description = f"LED circuit with current limiting: {v_source}V → {v_led}V LED at {i_led*1000}mA using {r_value}Ω resistor"
    
    # Define nets with clear naming
    vcc = Net('VCC')      # Power supply (5V)
    gnd = Net('GND')      # Ground (0V)
    
    # Create components with proper footprints
    r = Part('Device', 'R', value=f'{r_value} Ohms', footprint='Resistor_SMD:R_0805_2012Metric')
    d = Part('Device', 'LED', footprint='LED_SMD:LED_0805_2012Metric')
    
    # Set component properties for better identification
    r.ref = "R1"
    d.ref = "D1"
    r.value = f"{r_value}Ω"
    d.value = "LED"
    
    # Connect components in proper LED circuit layout: VCC → R → LED → GND
    # This creates a horizontal layout: Power → Resistor → LED → Ground
    vcc += r[1]           # VCC connects to resistor pin 1
    r[2] += d[1]          # Resistor pin 2 connects to LED anode
    d[2] += gnd           # LED cathode connects to ground

    # Generate KiCad files
    netlist_file = os.path.join(output_dir, f"{circuit_name}.net")
    log(f"Generating netlist: {netlist_file}")
    generate_netlist(file_=netlist_file)
    
    # Create KiCad project file
    project_file = create_kicad_project(circuit_name, output_dir)
    
    # Create schematic file 
    schematic_file = os.path.join(output_dir, f"{circuit_name}.kicad_sch")
    generate_schematic(file_=schematic_file)
    
    log(f"✓ Generated KiCad files in: {output_dir}")
    log(f"✓ LED circuit: {v_source}V → {v_led}V LED at {i_led*1000}mA using R={r_value}Ω")
    return schematic_file

if __name__ == "__main__":
    # Set up KiCad environment
    setup_kicad_env()
    
    # Create a voltage divider (5V to 3.3V)
    netlist, project, schematic = create_voltage_divider(5.0, 3.3)
    
    log("\nTo use these files in KiCad:")
    log("1. Open KiCad")
    log("2. Click 'File' -> 'Open Project'")
    log(f"3. Navigate to: {os.path.dirname(project)}")
    log(f"4. Open {os.path.basename(project)}")
    log("5. The schematic and netlist will be loaded automatically") 