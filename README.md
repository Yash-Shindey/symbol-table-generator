# Symbol Table Manager

This application provides a graphical user interface for managing a symbol table, which is often used in the context of compiler development. Below are the core functionalities of the Symbol Table Manager:

## Features

- **Insert Symbol**: Add a new symbol to the current scope.
- **Delete Symbol**: Remove an existing symbol from the symbol table.
- **Enter Scope**: Create a new nested scope within the symbol table.
- **Exit Scope**: Move back to the parent scope.
- **Lookup**: Search for a symbol in the current and parent scopes.
- **Serialize**: Save the current state of the symbol table to a file.
- **Deserialize**: Load the symbol table state from a file.

## Usage

To use the application, simply run the `main.py` script in a Python environment where PyQt5 is installed. Through the GUI, you can perform all the above operations by interacting with the buttons and input fields.

## Installation

1. Ensure you have Python installed on your system.
2. Install PyQt5 using `pip install PyQt5`
3. Run the application: `python3 main.py` in the same directory where the other files are kept.
