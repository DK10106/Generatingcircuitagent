# KiCad AI Circuit Generator

An AI-powered chat interface for generating KiCad circuit files through natural language descriptions.

## Features

- Natural language circuit description input
- Generates complete KiCad projects with:
  - Schematics (.kicad_sch)
  - Netlists (.net)
  - PCB files (.kicad_pcb)
  - Project files (.kicad_pro)
- Real-time chat interface
- Example circuit templates
- Automatic KiCad environment setup

## Prerequisites

- Python 3.8 or higher
- KiCad 6.0 or higher
- Git (for downloading symbol libraries)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kicad-ai-generator.git
cd kicad-ai-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the chat interface:
```bash
streamlit run interface/chat_ui.py
```

2. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Type your circuit description in natural language, for example:
   - "Create a voltage divider that converts 5V to 3.3V"
   - "Generate an RC low-pass filter with 1kHz cutoff frequency"
   - "Design a simple LED circuit with current limiting resistor"

4. The generated KiCad files will be saved in the `kicad_output` directory

## Project Structure

```
kicad-ai-generator/
├── core/
│   ├── circuit_generator.py
│   └── llm_engine.py
├── interface/
│   └── chat_ui.py
├── utils/
│   └── kicad_setup.py
├── generate_circuit.py
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 