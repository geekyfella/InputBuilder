# Computational Chemistry Input Builder

## Overview

The Computational Chemistry Input Builder is a Python-based graphical user interface (GUI) application designed to simplify the process of creating input files for computational chemistry software. By providing an intuitive interface, this tool helps users configure various parameters and generate input files with ease, reducing the potential for errors and improving efficiency.

## Features

- **User-Friendly Interface**: Easy-to-use interface built with Tkinter.
- **Dynamic Parameter Selection**: Drop-down menus for selecting and configuring parameters such as SCFMETH, LVL, CHARGE, SPIN, MEMORY, MEMDDI, and BASIS.
- **Geometry File Import**: Capability to import geometry files in XYZ format.
- **Input File Generation**: Generates and displays the input file content based on selected parameters.
- **Save Functionality**: Save the generated input file to a specified location.
- **Submit Placeholder**: Placeholder for future submission functionality.

## Getting Started

### Prerequisites

- Python 3.0 or Higher
- Tkinter (usually included with Python)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/computational-chemistry-input-builder.git
    cd computational-chemistry-input-builder
    ```

2. Run the application:

    ```bash
    python input_builder.py
    ```

## Usage

1. **Run the Application**: Launch the application by running the `input_builder.py` script.

2. **Select Parameters**: Use the drop-down menus to select and configure the desired parameters for your computational chemistry input file.

3. **Import Geometry File**: Click on the "Import Geometry File" button to select a geometry file in XYZ format.

4. **Generate Output**: Click the "Generate Output" button to generate and display the input file content based on the selected parameters and imported geometry file.

5. **Save Input File**: Click the "Save Input File" button to save the generated input file to a specified location.

6. **Submit Input**: (Optional) The "Submit" button is a placeholder for future functionality related to submitting the input file directly to computational chemistry software.

## Code Structure

- **`input_builder.py`**: Main application script containing the `ComputationalChemistryInputBuilder` class and the Tkinter GUI setup.

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Project by Ojasvi, Hemali, Aditya, Dev, Om
- Built with Python and Tkinter
