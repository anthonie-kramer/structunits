#!/usr/bin/env python
"""
Example usage of the structunits package.
"""

from structunits.specific_units.length import Length
from structunits.specific_units.length_unit import LengthUnit
from structunits.result import Result


def main():
    # Create length values
    inch_length = Length(10, LengthUnit.INCH)
    foot_length = Length(1, LengthUnit.FOOT)
    meter_length = Length(1, LengthUnit.METER)

    print("==== Basic Conversions ====")
    print(f"10 inches = {inch_length.convert_to(LengthUnit.FOOT):.4f} feet")
    print(f"10 inches = {inch_length.convert_to(LengthUnit.METER):.4f} meters")

    print(f"1 foot = {foot_length.convert_to(LengthUnit.INCH):.4f} inches")
    print(f"1 foot = {foot_length.convert_to(LengthUnit.METER):.4f} meters")

    print(f"1 meter = {meter_length.convert_to(LengthUnit.INCH):.4f} inches")
    print(f"1 meter = {meter_length.convert_to(LengthUnit.FOOT):.4f} feet")

    print("\n==== Operations ====")
    # Addition
    sum_length = inch_length + foot_length
    print(f"10 inches + 1 foot = {sum_length.convert_to(LengthUnit.INCH):.4f} inches")
    print(f"10 inches + 1 foot = {sum_length.convert_to(LengthUnit.FOOT):.4f} feet")

    # Subtraction
    diff_length = meter_length - foot_length
    print(f"1 meter - 1 foot = {diff_length.convert_to(LengthUnit.METER):.4f} meters")
    print(f"1 meter - 1 foot = {diff_length.convert_to(LengthUnit.INCH):.4f} inches")

    # Multiplication
    doubled_length = inch_length * 2
    print(f"10 inches * 2 = {doubled_length.convert_to(LengthUnit.INCH):.4f} inches")

    # Division
    halved_length = inch_length / 2
    print(f"10 inches / 2 = {halved_length.convert_to(LengthUnit.INCH):.4f} inches")

    # Squaring (creates an area)
    area = inch_length * inch_length
    print(f"Area of 10-inch square = {area.value:.4f} square inches")

    print("\n==== Mathematical Functions ====")
    # Square root
    sqrt_length = Result.sqrt(inch_length)
    print(f"Square root of 10 inches = {sqrt_length.value:.4f} inches^0.5")

    # Absolute value
    neg_length = Length(-5, LengthUnit.INCH)
    abs_length = Result.abs(neg_length)
    print(f"Absolute value of -5 inches = {abs_length.convert_to(LengthUnit.INCH):.4f} inches")

    # Min/Max
    min_length = Result.min(inch_length, foot_length)
    max_length = Result.max(inch_length, foot_length)
    print(f"Minimum of 10 inches and 1 foot = {min_length.convert_to(LengthUnit.INCH):.4f} inches")
    print(f"Maximum of 10 inches and 1 foot = {max_length.convert_to(LengthUnit.INCH):.4f} inches")

    print("\n==== Comparisons ====")
    print(f"10 inches == 1 foot: {inch_length == foot_length}")
    print(f"10 inches < 1 foot: {inch_length < foot_length}")
    print(f"10 inches > 1 foot: {inch_length > foot_length}")
    print(f"1 meter >= 1 foot: {meter_length >= foot_length}")

    print("\n==== LaTeX Strings ====")
    print(f"LaTeX for 10 inches: {inch_length.to_latex_string()}")
    print(f"LaTeX for 1 meter: {meter_length.to_latex_string(LengthUnit.METER)}")


if __name__ == "__main__":
    main()
