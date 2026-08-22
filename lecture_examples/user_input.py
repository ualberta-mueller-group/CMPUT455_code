from typing import Any

def user_input(items: list[Any], text: str) -> Any:
    """
    Let user select one item from items.
    Returns item in the correct type - input returns a str
    """
    item_map = {str(i): i for i in items} # E.g. map from '0' to 0
    while True:
        input_str = input(f"Choose your {text} - {items}: ").strip()
        if input_str in item_map:
            return item_map[input_str]

def user_input_int(prompt: str) -> int:
    """Prompts the user for input until a valid integer is entered."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Enter a valid integer.")

def user_input_float(prompt: str) -> float:
    """Prompts the user for input until a valid float is entered."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Enter a valid float.")