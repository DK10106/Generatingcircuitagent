# KiCad AI Circuit Generator

An AI-powered interface for generating KiCad circuit files through natural language descriptions or simple button clicks.

## Features

- **Two Interface Options:**
  - **Chat Interface**: Natural language circuit description input
  - **Simple Interface**: Button-based circuit generation
- **Easy Launcher**: Choose your interface with a simple menu
- **Real Circuit Generation**: Creates actual KiCad schematic files
- **Multiple Circuit Types:**
  - Voltage Divider (5V to 3.3V conversion)
  - RC Low-Pass Filter (configurable cutoff frequency)
  - LED Circuit (with current limiting resistor)
- **Automatic Downloads**: Direct download of generated schematic files
- **KiCad Integration**: Generates proper `.kicad_sch` files
- **Smart Parsing**: Understands natural language circuit descriptions

## Prerequisites

- Python 3.8 or higher
- KiCad 6.0 or higher (optional, for viewing generated files)
- Git (for downloading symbol libraries)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DK10106/Generatingcircuitagent.git
cd Generatingcircuitagent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Option 1: Use the Launcher (Recommended)

1. Run the launcher script:
```bash
python launch.py
```

2. Choose your preferred interface:
   - **1**: Simple Interface (Beginner-Friendly)
   - **2**: Chat Interface (Advanced)
   - **3**: Test Circuit Generation
   - **4**: Exit

### Option 2: Direct Launch

#### Simple Interface (Beginner-Friendly)
```bash
streamlit run app.py
```

#### Chat Interface (Advanced)
```bash
streamlit run interface/chat_ui.py
```

## Usage

### Simple Interface
1. Click the buttons to generate circuits:
   - **Generate Voltage Divider**: Creates a 5V to 3.3V voltage divider
   - **Generate RC Filter**: Creates a 1kHz RC low-pass filter
   - **Generate LED Circuit**: Creates a simple LED circuit with current limiting
2. Download the generated schematic files using the download buttons

### Chat Interface
Type your circuit description in natural language, for example:
- "Create a voltage divider that converts 5V to 3.3V"
- "Generate an RC low-pass filter with 1kHz cutoff frequency"
- "Design a simple LED circuit with current limiting resistor"

## Generated Files

The generated KiCad files will be saved in the `kicad_output` directory:

```
kicad_output/
├── voltage_divider/
│   └── voltage_divider_5v_33v.kicad_sch
├── rc_low_pass_filter/
│   └── rc_low_pass_1000hz.kicad_sch
└── led_circuit/
    └── simple_led_circuit.kicad_sch
```

## Project Structure

```
Generatingcircuitagent/
├── interface/
│   └── chat_ui.py          # Chat-based interface
├── app.py                  # Simple button-based interface
├── launch.py               # Launcher script
├── generate_circuit.py     # Core circuit generation functions
├── test_circuit_generation.py  # Test script
├── requirements.txt
└── README.md
```

## Circuit Types

### 1. Voltage Divider
- **Purpose**: Converts higher voltage to lower voltage
- **Components**: 2 Resistors
- **Default**: 5V to 3.3V conversion
- **Use Case**: Logic level conversion, sensor interfacing

### 2. RC Low-Pass Filter
- **Purpose**: Filters high-frequency signals
- **Components**: 1 Resistor, 1 Capacitor
- **Default**: 1kHz cutoff frequency
- **Use Case**: Signal conditioning, noise reduction

### 3. LED Circuit
- **Purpose**: Powers LED with current limiting
- **Components**: 1 Resistor, 1 LED
- **Default**: 5V supply, 20mA current
- **Use Case**: Status indicators, lighting

## Testing

Run the test script to verify all circuit generation functions:

```bash
python test_circuit_generation.py
```

Or use the launcher and select option 3.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License. 