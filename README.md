# Finance Tracker


[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Overview

The Finance Tracker is a Python application that allows users to manage and visualize their financial transactions. Users can add transactions, view a summary of their finances, and visualize their income and expenses over time.

## Requirements

1. **Python 3.x**: Ensure Python 3.x is installed on your system (tested on 3.10.2).
   
2. **Required Libraries**: You will need the following Python libraries:
   - `pandas`: For handling CSV files and data manipulation.
   - `tkcalendar`: For providing a date picker in the GUI.
   - `matplotlib`: For plotting financial data.
   
   

### Installation / How to Run

<ol>
<li>Create a virtual environment (optional but recommended):</li>

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```


<li> Use the package manager pip to install the libraries:</li>

```bash
pip install pandas tkcalendar matplotlib
```


<li> Clone the Repository:</li>

```bash
git clone https://github.com/AnnaMi0/Finance-Tracker.git
cd Finance-Tracker
```

<li> Run the program: </li>

```bash
python gui.py
```

</ol>