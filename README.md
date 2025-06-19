# KiCad AI Circuit Generator

An AI-powered circuit generator that creates KiCad schematic files using natural language descriptions. The system uses SKiDL (SKiDL Is a Description Language) to generate circuits and outputs complete KiCad projects ready for use.

## Features

- **AI-Powered Circuit Generation**: Describe any circuit in natural language
- **Pre-built Circuit Templates**: Quick generation of common circuits (voltage dividers, filters, LED circuits)
- **Complete KiCad Projects**: Output is a zipped KiCad project containing `.kicad_sch` and `.kicad_pro` files
- **User-Friendly Interface**: Streamlit web interface with chat and button-based generation
- **Download-Ready Files**: Single ZIP download with complete KiCad project

## Quick Start

### Prerequisites

- Python 3.8+
- KiCad 7+ (for CLI functionality)
- Ollama (for AI circuit generation)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Generatingcircuitagent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install KiCad CLI** (optional but recommended):
   - Download and install KiCad 7+ from [kicad.org](https://kicad.org)
   - Ensure `kicad-cli` is available in your PATH

4. **Install Ollama** (for AI features):
   - Download from [ollama.com](https://ollama.com)
   - Install and start the Ollama service

### Usage

1. **Start the application**:
   ```bash
   streamlit run interface/chat_ui.py
   ```

2. **Open your browser** to the provided URL (usually http://localhost:8501)

3. **Generate circuits**:
   - Use the sidebar buttons for quick generation of common circuits
   - Use the chat interface to describe custom circuits in natural language

4. **Download and use**:
   - Download the generated `.kicad_project.zip` file
   - Extract the ZIP file
   - Open the `.kicad_pro` file in KiCad
   - View and edit the schematic

## Circuit Types

### Pre-built Circuits
- **Voltage Divider**: Converts higher voltage to lower voltage (e.g., 5V to 3.3V)
- **RC Low-Pass Filter**: Filters high-frequency signals with configurable cutoff frequency
- **LED Circuit**: Simple LED with current-limiting resistor

### AI-Generated Circuits
- **Custom Circuits**: Describe any circuit in natural language
- **Complex Designs**: Multi-component circuits with specific requirements
- **Specialized Applications**: Sensor interfaces, power supplies, amplifiers, etc.

## Output Format

The system generates **complete KiCad projects** in the following format:

```
circuit_name.kicad_project.zip
├── circuit_name.kicad_pro    # KiCad project file
└── circuit_name.kicad_sch    # Schematic file
```

### Usage Instructions

1. **Download** the `.kicad_project.zip` file
2. **Extract** the ZIP file to a folder
3. **Open KiCad** (version 7 or later)
4. **File → Open Project** → Select the `.kicad_pro` file
5. **Double-click** the `.kicad_pro` file to open directly
6. **View the schematic** in the Schematic Editor
7. **Create PCB** from the schematic if needed

## File Structure

```
Generatingcircuitagent/
├── interface/
│   └── chat_ui.py           # Streamlit web interface
├── generate_circuit.py      # Core circuit generation logic
├── llm_engine.py           # AI/LLM integration
├── kicad_wrapper.py        # KiCad file handling
├── libraries/              # KiCad symbol libraries
├── kicad_output/           # Generated circuit files
└── requirements.txt        # Python dependencies
```

## Technical Details

### Dependencies
- **SKiDL**: Circuit description language
- **Streamlit**: Web interface framework
- **Ollama**: Local LLM for AI circuit generation
- **KiCad CLI**: Command-line tools for project creation

### Circuit Generation Process
1. **User Input**: Natural language description or circuit type selection
2. **AI Processing**: LLM generates SKiDL code (for custom circuits)
3. **Netlist Generation**: SKiDL creates component netlist
4. **Project Creation**: KiCad CLI converts netlist to schematic
5. **ZIP Packaging**: Complete project packaged for download
6. **Cleanup**: Temporary files removed

### Fallback Mode
If KiCad CLI is not available, the system falls back to generating netlist files (`.net`) that can be imported into KiCad manually.

## Troubleshooting

### Common Issues

1. **KiCad CLI not found**:
   - Install KiCad 7+ and ensure it's in your PATH
   - The system will fall back to netlist-only output

2. **Ollama not running**:
   - Start Ollama service: `ollama serve`
   - Install required models: `ollama pull llama2`

3. **Library errors**:
   - The system automatically downloads required KiCad libraries
   - Check internet connection for library downloads

### Error Messages

- **"KiCad CLI not found"**: Install KiCad 7+ or use netlist fallback
- **"Ollama service not running"**: Start Ollama with `ollama serve`
- **"Library download failed"**: Check internet connection and try again

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **SKiDL**: Circuit description language
- **KiCad**: Open-source PCB design software
- **Ollama**: Local LLM framework
- **Streamlit**: Web application framework 