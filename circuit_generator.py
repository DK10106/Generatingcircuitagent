from typing import Dict, List, Optional, Tuple
import os
import json
from datetime import datetime
from generate_circuit import create_voltage_divider, setup_kicad_env

class CircuitGenerator:
    """
    Handles conversion of LLM responses to actual KiCad circuit files
    """
    def __init__(self):
        """Initialize the circuit generator"""
        self.output_dir = os.path.join(os.getcwd(), 'kicad_output')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_llm_response(self, llm_response: dict) -> tuple[str, list]:
        """Process the LLM response and generate circuit files
        
        Args:
            llm_response (dict): Structured circuit description from LLM
            
        Returns:
            tuple[str, list]: (circuit_directory, list_of_generated_files)
        """
        try:
            # Extract circuit type and parameters
            circuit_type = llm_response.get('circuit_type', '').lower()
            params = llm_response.get('parameters', {})
            
            # Generate circuit based on type
            if circuit_type == 'voltage_divider':
                vin = float(params.get('input_voltage', 5.0))
                vout = float(params.get('output_voltage', 3.3))
                
                netlist, project, schematic = create_voltage_divider(vin, vout)
                circuit_dir = os.path.dirname(project)
                generated_files = [netlist, project, schematic]
                
                return circuit_dir, generated_files
            
            # Add more circuit types here as needed
            else:
                raise ValueError(f"Unsupported circuit type: {circuit_type}")
                
        except Exception as e:
            print(f"Error generating circuit: {str(e)}")
            return None, None

    def log(self, msg: str):
        """Log messages with timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    def parse_circuit_description(self, llm_response: str) -> Dict:
        """
        Parse LLM response to extract circuit details
        Expected format:
        {
            "circuit_type": "voltage_divider|rc_filter|etc",
            "parameters": {
                "name": "circuit_name",
                "values": {
                    "param1": value1,
                    "param2": value2,
                    ...
                }
            },
            "components": [
                {
                    "type": "resistor|capacitor|etc",
                    "value": "value",
                    "connections": ["net1", "net2"]
                },
                ...
            ]
        }
        """
        try:
            # Try to find JSON block in response
            start = llm_response.find('{')
            end = llm_response.rfind('}') + 1
            if start >= 0 and end > start:
                circuit_json = llm_response[start:end]
                return json.loads(circuit_json)
            else:
                self.log("No JSON circuit description found in response")
                return None
        except json.JSONDecodeError as e:
            self.log(f"Error parsing circuit description: {str(e)}")
            return None

    def generate_circuit_files(self, circuit_desc: Dict) -> Tuple[str, List[str]]:
        """
        Generate actual KiCad circuit files from the description
        Returns:
            Tuple of (circuit_dir, list of generated files)
        """
        if not circuit_desc:
            return None, []

        circuit_type = circuit_desc.get('circuit_type', '').lower()
        params = circuit_desc.get('parameters', {})
        
        # Generate circuit based on type
        if circuit_type == 'voltage_divider':
            name = params.get('name', 'voltage_divider')
            vin = float(params.get('values', {}).get('vin', 5.0))
            vout = float(params.get('values', {}).get('vout', 3.3))
            netlist_file, project_file = self.kicad.create_voltage_divider(name, vin, vout)
            
        elif circuit_type == 'rc_filter':
            name = params.get('name', 'rc_filter')
            cutoff_freq = float(params.get('values', {}).get('cutoff_freq', 1000))
            netlist_file, project_file = self.kicad.create_rc_filter(name, cutoff_freq)
            
        elif circuit_type == 'custom':
            # Handle custom circuit with explicit component definitions
            name = params.get('name', 'custom_circuit')
            self.kicad.create_circuit(name)
            
            # Create nets
            nets = {}
            for component in circuit_desc.get('components', []):
                for net_name in component.get('connections', []):
                    if net_name not in nets:
                        nets[net_name] = self.kicad.create_net(net_name)
            
            # Create and connect components
            for component in circuit_desc.get('components', []):
                comp_type = component.get('type', '').lower()
                value = component.get('value', '')
                
                if comp_type == 'resistor':
                    part = self.kicad.add_component("Device", "R", value=value)
                elif comp_type == 'capacitor':
                    part = self.kicad.add_component("Device", "C", value=value)
                # Add more component types as needed
                
                # Connect component pins to nets
                for i, net_name in enumerate(component.get('connections', [])):
                    if net_name in nets:
                        nets[net_name] += part[i+1]
            
            netlist_file, project_file = self.kicad.generate_outputs(name)
        
        else:
            self.log(f"Unsupported circuit type: {circuit_type}")
            return None, []
        
        # Get all generated files
        circuit_dir = os.path.dirname(netlist_file)
        generated_files = [
            netlist_file,
            project_file,
            os.path.join(circuit_dir, f"{params.get('name')}.kicad_sch")
        ]
        
        self.log(f"Generated circuit files in: {circuit_dir}")
        for f in generated_files:
            if os.path.exists(f):
                self.log(f"✓ Created: {os.path.basename(f)}")
        
        return circuit_dir, generated_files 