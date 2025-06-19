#!/usr/bin/env python3
import sys
import argparse
from core.kicad_generator import KiCadSchematicGenerator

def main():
    parser = argparse.ArgumentParser(description='Generate KiCad schematics from text descriptions')
    parser.add_argument('prompt', type=str, help='Natural language description of the circuit')
    args = parser.parse_args()
    
    try:
        generator = KiCadSchematicGenerator()
        output_file = generator.parse_prompt(args.prompt)
        print(f"Successfully generated schematic: {output_file}")
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 