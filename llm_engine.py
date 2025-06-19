from typing import Dict, List, Optional, Tuple
import os
import ollama
import json
import subprocess
import sys
import time
from datetime import datetime
import urllib.request
import re
import tempfile
import traceback
import openai

class LLMEngine:
    """
    Core LLM integration engine for KiCad AI Assistant using Ollama with Llama 2
    """
    def __init__(self, model_name: str = "llama2"):
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Initializing KiCad AI Assistant...")
        self.model_name = model_name
        self.context_history = []
        self.check_ollama_installation()
        self.initialize_model()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Initialization complete!")
    
    def check_ollama_installation(self):
        """Check if Ollama is installed and accessible"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking Ollama installation...")
        try:
            # First check if Ollama service is running
            try:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking if Ollama service is running...")
                ollama.list()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Ollama service is running")
                return
            except Exception:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Ollama service not running, attempting to start...")
                # Try to start the Ollama service
                subprocess.Popen(
                    ['ollama', 'serve'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                # Wait for service to start
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting for Ollama service to start (5s)...")
                time.sleep(5)  # Give the service time to start
                
                # Verify service is now running
                try:
                    ollama.list()
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Ollama service started successfully")
                    return
                except Exception as e:
                    raise Exception(f"Failed to start Ollama service: {str(e)}")
                
        except FileNotFoundError:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ ERROR: Ollama is not installed or not in PATH")
            print("Please install Ollama from: https://ollama.com/download/windows")
            print("After installation, you may need to:")
            print("1. Restart your terminal")
            print("2. Add Ollama to your system PATH")
            sys.exit(1)
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Error checking Ollama installation: {str(e)}")
            sys.exit(1)
    
    def initialize_model(self):
        """Initialize the Llama 2 model with Ollama"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Initializing Llama 2 model...")
        try:
            # List available models
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking available models...")
            models_response = ollama.list()
            available_models = []
            
            # Safely extract model names
            if hasattr(models_response, 'models'):
                for model in models_response.models:
                    if hasattr(model, 'name'):
                        available_models.append(model.name)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Available models: {', '.join(available_models)}")
            
            # Download model if not available
            if self.model_name not in available_models:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Downloading {self.model_name} model (this may take a few minutes)...")
                start_time = time.time()
                ollama.pull(self.model_name)
                elapsed_time = time.time() - start_time
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Model {self.model_name} downloaded successfully in {elapsed_time:.1f}s")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Model {self.model_name} is already available")
            
            # Set model parameters optimized for technical/engineering tasks
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Configuring model parameters...")
            self.model_params = {
                "num_gpu": 1,  # Use GPU acceleration
                "temperature": 0.7,  # Balanced between creativity and precision
                "top_p": 0.9,  # High coherence for technical responses
                "num_ctx": 4096,  # Large context window for complex circuits
                "num_thread": 8  # Utilize multiple CPU threads
            }
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Model parameters configured")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Error initializing model: {str(e)}")
            print("Please ensure Ollama is installed and running")
            raise
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate a response using Llama 2
        Args:
            prompt: Input prompt for the model
        Returns:
            Generated response
        """
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating response...")
            start_time = time.time()
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options=self.model_params
            )
            elapsed_time = time.time() - start_time
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Response generated in {elapsed_time:.1f}s")
            return response['response']
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Error generating response: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def analyze_circuit(self, circuit_data: Dict) -> Dict:
        """
        Analyze circuit design and provide insights using Llama 3.2
        Args:
            circuit_data: Dictionary containing circuit information
        Returns:
            Dictionary containing analysis results
        """
        prompt = f"""
        As an expert electronics engineer, analyze this circuit and provide detailed insights:
        
        Circuit Name: {circuit_data.get('name', 'Unnamed')}
        Description: {circuit_data.get('description', 'No description')}
        Components: {', '.join(circuit_data.get('components', []))}
        Connections: {', '.join(circuit_data.get('nets', []))}
        
        Please provide a comprehensive analysis including:
        1. Detailed component analysis and their roles
        2. Circuit topology and design patterns
        3. Potential performance characteristics
        4. Possible issues or reliability concerns
        5. Specific suggestions for improvement
        """
        
        response = self.generate_response(prompt)
        
        # Parse the response into structured data
        try:
            # Extract sections from the response
            components = []
            suggestions = []
            potential_issues = []
            
            # Simple parsing (can be improved)
            current_section = None
            for line in response.split('\n'):
                if 'Component analysis' in line or 'Circuit topology' in line:
                    current_section = 'components'
                elif 'Potential issues' in line or 'reliability concerns' in line:
                    current_section = 'issues'
                elif 'Suggestions' in line or 'improvement' in line:
                    current_section = 'suggestions'
                elif line.strip() and current_section:
                    if current_section == 'components':
                        components.append(line.strip())
                    elif current_section == 'issues':
                        potential_issues.append(line.strip())
                    elif current_section == 'suggestions':
                        suggestions.append(line.strip())
            
            return {
                "components": components,
                "suggestions": suggestions,
                "potential_issues": potential_issues,
                "raw_response": response
            }
        except Exception as e:
            return {
                "components": [],
                "suggestions": [],
                "potential_issues": [f"Error parsing response: {str(e)}"],
                "raw_response": response
            }
    
    def suggest_improvements(self, circuit_data: Dict) -> List[Dict]:
        """
        Suggest possible improvements for the circuit using Llama 3.2's expertise
        Args:
            circuit_data: Dictionary containing circuit information
        Returns:
            List of suggested improvements
        """
        prompt = f"""
        As an expert electronics engineer, suggest detailed improvements for this circuit:
        
        Circuit Name: {circuit_data.get('name', 'Unnamed')}
        Description: {circuit_data.get('description', 'No description')}
        Components: {', '.join(circuit_data.get('components', []))}
        Connections: {', '.join(circuit_data.get('nets', []))}
        
        Please provide specific, actionable improvements for:
        1. Performance optimization
        2. Reliability enhancement
        3. Cost reduction opportunities
        4. Power efficiency improvements
        5. EMC/EMI considerations
        6. Thermal management
        7. Manufacturing optimization
        """
        
        response = self.generate_response(prompt)
        
        # Convert response to structured format
        improvements = []
        current_category = None
        
        for line in response.split('\n'):
            if any(category in line.lower() for category in 
                  ['performance', 'reliability', 'cost', 'power', 'emc', 'thermal', 'manufacturing']):
                current_category = line.strip()
            elif line.strip() and current_category:
                improvements.append({
                    "category": current_category,
                    "suggestion": line.strip()
                })
        
        return improvements
    
    def process_user_query(self, query: str, context: Optional[Dict] = None) -> str:
        """
        Process a natural language query using Llama 2's capabilities
        Args:
            query: User's question or request
            context: Additional context about the current circuit
        Returns:
            Response to the user's query
        """
        # Build prompt with context and engineering focus
        example_code = '''from skidl import *
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
circuit_name = 'voltage_divider'  # Replace with appropriate name
circuit_description = 'A voltage divider circuit'  # Replace with appropriate description
default_circuit.name = circuit_name
default_circuit.description = circuit_description

# Define nets
vcc = Net('VCC')  # Power
gnd = Net('GND')  # Ground
out = Net('OUT')  # Output

# Create components with footprints
r1 = Part("Device", "R", value="10k", footprint="Resistor_SMD:R_0805_2012Metric")
r2 = Part("Device", "R", value="4.7k", footprint="Resistor_SMD:R_0805_2012Metric")

# Make connections
vcc += r1[1]
r1[2] += out
out += r2[1]
r2[2] += gnd

# Generate netlist with circuit name
generate_netlist(file_=f'{circuit_name}.net')'''

        prompt = f"""
        You are a KiCad and electronics expert. Provide specific, actionable responses focused on code implementation.
        Always include Python code examples using skidl when relevant.
        Keep theoretical explanations brief and focus on practical implementation.

        When showing code examples:
        1. Use skidl for circuit creation
        2. Include necessary imports and setup
        3. Show component connections clearly
        4. Add comments explaining key steps
        5. Include netlist generation with specific filename based on circuit name
        6. Always follow this exact code structure, but replace the values and components as needed.

        Here's an example of properly structured code:

        {example_code}

        Format your response EXACTLY like this, with NO VARIATIONS:

        [EXPLANATION]
        Brief explanation of what the code will do
        [/EXPLANATION]

        [CODE]
        Your complete code here, following the structure above but with appropriate values
        [/CODE]

        [INSTRUCTIONS]
        Brief instructions for what will happen next
        [/INSTRUCTIONS]

        IMPORTANT FORMATTING RULES:
        - Use [CODE] tags exactly as shown above, not backticks
        - Include all three sections: EXPLANATION, CODE, and INSTRUCTIONS
        - Keep the tags on their own lines
        - Make sure there are no spaces in the tags
        - Use descriptive circuit names (no spaces, use underscores)
        - Include clear circuit descriptions
        - Add actual component values and connections based on the circuit requirements
        - Keep the basic structure including imports, environment setup, and netlist generation
        - Make sure to define circuit_name before using it in generate_netlist
        - IMPORTANT: Always include the library download code as shown in the example
        
        Current request: {query}
        
        Circuit Context:
        {json.dumps(context, indent=2) if context else 'No circuit loaded'}
        """
        
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating focused response...")
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options=self.model_params
            )
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Response generated successfully")
            return response['response']
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error generating response: {str(e)}")
            return f"Error generating response: {str(e)}"

    def get_response(self, user_input: str) -> dict:
        """Get structured response from LLM
        
        For now, this is a simple mock that returns a voltage divider description.
        In a real implementation, this would call an actual LLM API.
        
        Args:
            user_input (str): User's circuit request
            
        Returns:
            dict: Structured circuit description
        """
        # Mock response for voltage divider
        # In reality, this would parse the user input and generate appropriate parameters
        return {
            "circuit_type": "voltage_divider",
            "parameters": {
                "input_voltage": 5.0,
                "output_voltage": 3.3
            }
        }

    def extract_code_from_response(self, response: str) -> Optional[str]:
        """Extract Python code from LLM response"""
        try:
            # Look for code between [CODE] tags
            code_match = re.search(r'\[CODE\](.*?)\[/CODE\]', response, re.DOTALL)
            if code_match:
                return code_match.group(1).strip()
            
            # Fallback: look for code between triple backticks
            code_match = re.search(r'```python\s*(.*?)\s*```', response, re.DOTALL)
            if code_match:
                return code_match.group(1).strip()
            
            # Fallback: look for code between single backticks
            code_match = re.search(r'`(.*?)`', response, re.DOTALL)
            if code_match:
                return code_match.group(1).strip()
            
            return None
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error extracting code: {str(e)}")
            return None

    def execute_circuit_code(self, code: str, circuit_name: str = "generated_circuit") -> Tuple[bool, str, List[str]]:
        """
        Execute LLM-generated circuit code safely and generate output files
        
        Args:
            code: Python code generated by LLM
            circuit_name: Name for the circuit
            
        Returns:
            Tuple of (success, message, list_of_generated_files)
        """
        try:
            # Create a temporary directory for execution
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create the Python file
                code_file = os.path.join(temp_dir, f"{circuit_name}.py")
                
                # Add safety imports and setup
                safe_code = f"""import os
import sys
import traceback
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.getcwd())

# Set up output directory
output_dir = os.path.join(os.getcwd(), 'kicad_output', '{circuit_name}')
os.makedirs(output_dir, exist_ok=True)

# Change to temp directory for execution
os.chdir(temp_dir)

try:
{chr(10).join('    ' + line for line in code.split(chr(10)))}
    
    # Generate netlist file
    netlist_file = os.path.join(output_dir, '{circuit_name}.net')
    generate_netlist(file_=netlist_file)
    
    print(f"✓ Generated netlist: {{netlist_file}}")
    
    # Try to generate schematic (may not work with KiCad 8)
    try:
        schematic_file = os.path.join(output_dir, '{circuit_name}.kicad_sch')
        generate_schematic(file_=schematic_file)
        print(f"✓ Generated schematic: {{schematic_file}}")
    except Exception as e:
        print(f"⚠ Schematic generation failed: {{str(e)}}")
    
    print(f"✓ Circuit generation completed successfully")
    
except Exception as e:
    print(f"❌ Error executing circuit code: {{str(e)}}")
    traceback.print_exc()
    raise
"""
                
                with open(code_file, 'w') as f:
                    f.write(safe_code)
                
                # Execute the code
                result = subprocess.run(
                    [sys.executable, code_file],
                    capture_output=True,
                    text=True,
                    cwd=temp_dir,
                    timeout=60  # 60 second timeout
                )
                
                if result.returncode == 0:
                    # Success - collect generated files
                    generated_files = []
                    output_dir = os.path.join(os.getcwd(), 'kicad_output', circuit_name)
                    
                    # Check for netlist file
                    netlist_file = os.path.join(output_dir, f"{circuit_name}.net")
                    if os.path.exists(netlist_file):
                        generated_files.append(netlist_file)
                    
                    # Check for schematic file
                    schematic_file = os.path.join(output_dir, f"{circuit_name}.kicad_sch")
                    if os.path.exists(schematic_file):
                        generated_files.append(schematic_file)
                    
                    return True, result.stdout, generated_files
                else:
                    return False, f"Code execution failed: {result.stderr}", []
                    
        except subprocess.TimeoutExpired:
            return False, "Code execution timed out (60 seconds)", []
        except Exception as e:
            return False, f"Error executing code: {str(e)}", []

    def generate_and_execute_circuit(self, user_request: str) -> Dict:
        """
        Generate circuit code from user request and execute it
        
        Args:
            user_request: Natural language description of the circuit
            
        Returns:
            Dict with execution results
        """
        try:
            # Generate LLM response with circuit code
            prompt = f"""
You are a KiCad and electronics expert. Generate Python code using the SKiDL library to create the requested circuit.

**IMPORTANT CONTEXT:**
- You are using KiCad 8 with SKiDL version 2.0.1
- Schematic generation (.kicad_sch files) is NOT supported in KiCad 8 with SKiDL
- Only netlist generation (.net files) is supported
- You have the following libraries available to use:
  - **Device**: Contains common components like 'R' (resistors), 'C' (capacitors), 'D' (diodes)
  - **power**: Contains power symbols like 'VCC' and 'GND'
  - **LED**: Contains LED components like 'LED'

**REQUIREMENTS:**
1. Use ONLY components from the available libraries listed above
2. Do NOT use any .lib files (outdated format)
3. Do NOT attempt to generate schematic files
4. Focus on creating a proper netlist with correct component connections
5. Use clear, descriptive net names
6. Add inline comments explaining the circuit design
7. Use proper resistor values (standard E12 series: 10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82)
8. Use proper capacitor values (standard: 0.1µF, 1µF, 10µF, 100µF, etc.)

**CODE TEMPLATE:**
```python
from skidl import *
import os

# Set up KiCad environment
set_default_tool('kicad')

# Create circuit components
# Add your components here using Part("Library", "Component")

# Connect components
# Add your connections here

# Generate netlist
generate_netlist()
```

**USER REQUEST:** {user_request}

Generate the complete Python code that creates this circuit. Make sure to:
- Use only available libraries (Device, power, LED)
- Create a functional netlist
- Include proper component values
- Add helpful comments
- Handle any errors gracefully

Return ONLY the Python code, no explanations.
"""
            
            response = self.generate_response(prompt)
            code = self.extract_code_from_response(response)
            
            if not code:
                return {
                    "success": False,
                    "message": "Failed to extract code from LLM response",
                    "response": response,
                    "generated_files": []
                }
            
            # Execute the code
            circuit_name = f"circuit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            success, message, generated_files = self.execute_circuit_code(code, circuit_name)
            
            return {
                "success": success,
                "message": message,
                "response": response,
                "code": code,
                "generated_files": generated_files,
                "circuit_name": circuit_name
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error in circuit generation: {str(e)}",
                "response": "",
                "code": "",
                "generated_files": [],
                "circuit_name": ""
            } 