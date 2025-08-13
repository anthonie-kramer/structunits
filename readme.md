# structunits

A Python unit conversion framework with operator overloading for easy manipulation of physical quantities.

## Overview

structunits provides a clean, intuitive interface for working with physical quantities that have units. Key features include:

- Full operator overloading for arithmetic operations (+, -, *, /, ^)
- Automatic unit tracking and conversion
- Support for common mathematical functions (sqrt, abs, min/max, etc.)
- LaTeX string output for documentation
- Easy extensibility for new unit types

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/structunits.git
cd structunits

# Install the package
pip install -e .
```

## Usage Example

```python
from structunits.specific_units.length import Length
from structunits.specific_units.length_unit import LengthUnit

# Create length values
inch_length = Length(10, LengthUnit.INCH)
foot_length = Length(1, LengthUnit.FOOT)
meter_length = Length(1, LengthUnit.METER)

# Convert between units
print(f"10 inches = {inch_length.convert_to(LengthUnit.FOOT)} feet")  # 0.8333 feet
print(f"1 foot = {foot_length.convert_to(LengthUnit.METER)} meters")  # 0.3048 meters

# Perform operations with automatic unit tracking
sum_length = inch_length + foot_length  # Addition
diff_length = meter_length - foot_length  # Subtraction
doubled_length = inch_length * 2  # Multiplication
halved_length = inch_length / 2  # Division
area = inch_length * inch_length  # Creates an area (L²)

# Compare values (automatically handles unit conversion)
if meter_length > foot_length:
    print("1 meter is greater than 1 foot")
```

## Extending the Framework

To add a new unit type:

1. Create a new unit class (e.g., `ForceUnit`) in `structunits/specific_units/force_unit.py`
2. Create a new result class (e.g., `Force`) in `structunits/specific_units/force.py`
3. Add the new classes to `structunits/specific_units/__init__.py`
4. Update the `_build_typed_result` method in `result.py` to handle the new unit type

## Current Unit Types

Currently implemented unit types:
- Length (inch, foot, meter, etc.)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
