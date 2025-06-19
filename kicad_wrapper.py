from typing import Dict, List, Optional, Tuple
from skidl import *
import os
import shutil
import urllib.request
from datetime import datetime

class KiCadWrapper:
    """
    Wrapper for KiCad operations using skidl and Python
    Handles circuit creation, netlist generation, and schematic/PCB operations
    """
    def __init__(self):
        self.current_circuit = None
        self.lib_search_paths = []
        self.output_dir = os.path.join(os.getcwd(), 'kicad_output')
        os.makedirs(self.output_dir, exist_ok=True)
        self.setup_environment()
        
    def log(self, msg: str):
        """Log messages with timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
        
    def setup_environment(self):
        """Setup KiCad environment and library paths"""
        self.log("Setting up KiCad environment...")
        
        # Create necessary directories
        libraries_dir = os.path.join(os.getcwd(), 'libraries')
        os.makedirs(libraries_dir, exist_ok=True)
        
        # Download required KiCad libraries if they don't exist
        required_libs = {
            'Device.kicad_sym': 'https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/Device.kicad_sym',
            'power.kicad_sym': 'https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/power.kicad_sym'
        }
        
        for lib_name, lib_url in required_libs.items():
            lib_path = os.path.join(libraries_dir, lib_name)
            if not os.path.exists(lib_path):
                self.log(f"Downloading {lib_name}...")
                try:
                    urllib.request.urlretrieve(lib_url, lib_path)
                    self.log(f"✓ Downloaded {lib_name}")
                except Exception as e:
                    self.log(f"✗ Error downloading {lib_name}: {str(e)}")
                    raise
        
        # Set up library search paths
        self.lib_search_paths = [os.path.abspath(libraries_dir)]
        lib_search_paths_kicad = lib_search_paths_skidl = self.lib_search_paths
        
        # Set environment variables
        os.environ['KICAD_SYMBOL_DIR'] = os.path.abspath(libraries_dir)
        os.environ['KICAD6_SYMBOL_DIR'] = os.path.abspath(libraries_dir)
        os.environ['KICAD7_SYMBOL_DIR'] = os.path.abspath(libraries_dir)
        os.environ['KICAD8_SYMBOL_DIR'] = os.path.abspath(libraries_dir)
        
        # Set default tool
        set_default_tool(KICAD)
        self.log("✓ KiCad environment setup complete")
    
    def create_circuit(self, name: str, description: str = "") -> None:
        """Create a new circuit with the given name and description"""
        self.log(f"Creating circuit: {name}")
        self.current_circuit = Circuit()
        self.current_circuit.name = name
        self.current_circuit.description = description
        default_circuit.name = name
        default_circuit.description = description
    
    def add_component(self, lib: str, part: str, value: str = "", footprint: str = "", **kwargs) -> Part:
        """Add a component to the circuit"""
        self.log(f"Adding component: {part} ({value})")
        return Part(lib, part, value=value, footprint=footprint, **kwargs)
    
    def create_net(self, name: str) -> Net:
        """Create a named net"""
        self.log(f"Creating net: {name}")
        return Net(name)
    
    def generate_outputs(self, circuit_name: str) -> Tuple[str, str]:
        """Generate KiCad output files (netlist and project files)"""
        self.log("Generating KiCad output files...")
        
        # Create output directory for this circuit
        circuit_dir = os.path.join(self.output_dir, circuit_name)
        os.makedirs(circuit_dir, exist_ok=True)
        
        # Generate netlist
        netlist_file = os.path.join(circuit_dir, f"{circuit_name}.net")
        self.log(f"Generating netlist: {netlist_file}")
        generate_netlist(file_=netlist_file)
        
        # Create KiCad project file
        project_file = os.path.join(circuit_dir, f"{circuit_name}.kicad_pro")
        with open(project_file, 'w') as f:
            f.write('''{
  "board": {
    "design_settings": {
      "defaults": {
        "board_outline_line_width": 0.09999999999999999,
        "copper_line_width": 0.19999999999999998,
        "copper_text_italic": false,
        "copper_text_size_h": 1.5,
        "copper_text_size_v": 1.5,
        "copper_text_thickness": 0.3,
        "copper_text_upright": false,
        "courtyard_line_width": 0.049999999999999996,
        "dimension_precision": 4,
        "dimension_units": 3,
        "dimensions": {
          "arrow_length": 1270000,
          "extension_offset": 500000,
          "keep_text_aligned": true,
          "suppress_zeroes": false,
          "text_position": 0,
          "units_format": 1
        }
      }
    }
  },
  "meta": {
    "filename": "circuit.kicad_pro",
    "version": 1
  },
  "net_settings": {
    "classes": [
      {
        "bus_width": 12.0,
        "clearance": 0.2,
        "diff_pair_gap": 0.25,
        "diff_pair_via_gap": 0.25,
        "diff_pair_width": 0.2,
        "line_style": 0,
        "microvia_diameter": 0.3,
        "microvia_drill": 0.1,
        "name": "Default",
        "pcb_color": "rgba(0, 0, 0, 0.000)",
        "schematic_color": "rgba(0, 0, 0, 0.000)",
        "track_width": 0.25,
        "via_diameter": 0.8,
        "via_drill": 0.4,
        "wire_width": 6.0
      }
    ],
    "meta": {
      "version": 2
    }
  },
  "schematic": {
    "drawing": {
      "default_line_thickness": 6.0,
      "default_text_size": 50.0,
      "field_names": [],
      "intersheets_ref_own_page": false,
      "intersheets_ref_prefix": "",
      "intersheets_ref_short": false,
      "intersheets_ref_show": false,
      "intersheets_ref_suffix": "",
      "junction_size_choice": 3,
      "label_size_ratio": 0.25,
      "pin_symbol_size": 0.0,
      "text_offset_ratio": 0.08
    }
  }
}''')
        
        # Create schematic file
        schematic_file = os.path.join(circuit_dir, f"{circuit_name}.kicad_sch")
        with open(schematic_file, 'w') as f:
            f.write(f'''(kicad_sch (version 20211123) (generator skidl)
  (paper "A4")
  (title_block
    (title "{circuit_name}")
    (date "{datetime.now().strftime('%Y-%m-%d')}")
    (rev "v1.0")
    (company "Generated by KiCad AI Assistant")
  )
)''')
        
        self.log(f"✓ Generated KiCad files in: {circuit_dir}")
        return netlist_file, project_file
    
    def create_voltage_divider(self, name: str, vin: float, vout: float) -> Tuple[str, str]:
        """Create a voltage divider circuit with the specified input and output voltages"""
        self.log(f"Creating voltage divider: Vin={vin}V, Vout={vout}V")
        
        # Calculate resistor values (using 10k for R1)
        r1_value = 10000  # 10k
        r2_value = int(r1_value * (vout / (vin - vout)))
        
        # Create circuit
        self.create_circuit(name, f"Voltage divider {vin}V to {vout}V")
        
        # Create nets
        vcc = self.create_net('VCC')
        gnd = self.create_net('GND')
        out = self.create_net('OUT')
        
        # Create components
        r1 = self.add_component("Device", "R", value=f"{r1_value}", footprint="Resistor_SMD:R_0805_2012Metric")
        r2 = self.add_component("Device", "R", value=f"{r2_value}", footprint="Resistor_SMD:R_0805_2012Metric")
        
        # Make connections
        vcc += r1[1]
        r1[2] += out
        out += r2[1]
        r2[2] += gnd
        
        # Generate output files
        return self.generate_outputs(name)
    
    def create_rc_filter(self, name: str, cutoff_freq: float) -> Tuple[str, str]:
        """Create an RC low-pass filter with the specified cutoff frequency"""
        self.log(f"Creating RC filter: fc={cutoff_freq}Hz")
        
        # Calculate component values (using 10k for R)
        r_value = 10000  # 10k
        c_value = 1 / (2 * 3.14159 * cutoff_freq * r_value)
        c_value_uf = c_value * 1e6  # Convert to µF
        
        # Create circuit
        self.create_circuit(name, f"RC low-pass filter fc={cutoff_freq}Hz")
        
        # Create nets
        vcc = self.create_net('VCC')
        gnd = self.create_net('GND')
        out = self.create_net('OUT')
        
        # Create components
        r1 = self.add_component("Device", "R", value=f"{r_value}", footprint="Resistor_SMD:R_0805_2012Metric")
        c1 = self.add_component("Device", "C", value=f"{c_value_uf:.2f}uF", footprint="Capacitor_SMD:C_0805_2012Metric")
        
        # Make connections
        vcc += r1[1]
        r1[2] += out
        out += c1[1]
        c1[2] += gnd
        
        # Generate output files
        return self.generate_outputs(name)

    def get_circuit_info(self) -> Dict:
        """
        Get information about the current circuit
        Returns:
            Dictionary containing circuit information
        """
        if not self.current_circuit:
            return {}
        
        return {
            "name": self.current_circuit.name,
            "description": self.current_circuit.description,
            "components": [str(c) for c in self.current_circuit.parts],
            "nets": [str(n) for n in self.current_circuit.nets]
        } 