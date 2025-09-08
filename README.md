# Professional Keylogger with GUI

A professional-grade keylogger application with a graphical user interface, built with Python. This application is designed for legitimate use cases such as typing pattern analysis and productivity tracking, with built-in user consent mechanisms.

## Features

- 🔐 User Consent System
- 👨‍💻 Graphical User Interface with Multiple Tabs
- 📊 Real-time Statistics
- 📝 Detailed Logging
- 🔄 Reset Functionality
- 📈 Key Press Analytics
- 💾 Local Data Storage

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DenCT101/KeyLogger-with-Consent.git
cd keylogger
```

2. Create a virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/MacOS
python3 -m venv .venv
source .venv/bin/activate
```

3. Install required packages:
```bash
pip install pynput
pip install tk
```

## Usage

1. Run the application:
```bash
python KeyLogger.py
```

2. When the application starts:
   - You'll be presented with a consent form
   - Fill in your name and purpose of usage
   - Accept the terms to proceed

3. Main Interface:
   - **Dashboard Tab**: Contains controls and real-time statistics
   - **Statistics Tab**: Shows detailed typing analytics
   - **Log Viewer Tab**: Displays the detailed keystroke log

4. Controls:
   - Start Logging: Begins capturing keystrokes
   - Stop Logging: Pauses the capture
   - Reset All Data: Clears all stored data

## Privacy and Consent

This application is built with privacy in mind:
- Requires explicit user consent before operation
- All data is stored locally on the user's computer
- No data is transmitted over the network
- Users can reset/delete all stored data at any time
- Clear documentation of data collection

## Technical Details

### Components Used

1. **Python Libraries**:
   - `pynput`: For keyboard monitoring
   - `tkinter`: For the GUI
   - `datetime`: For timestamp logging
   - `json`: For data storage
   - `threading`: For background processes

2. **Classes**:
   - `KeyLogger`: Core logging functionality
   - `ConsentDialog`: User consent management
   - `KeyLoggerGUI`: Main application interface

### Data Storage

The application stores data in two files:
- `keylog.txt`: Raw keystroke logs with timestamps
- `keystats.json`: Statistical data about typing patterns

## Development Process

1. Initial Setup:
   - Basic keylogging functionality
   - Core data collection methods

2. GUI Development:
   - Tab-based interface design
   - Real-time statistics display
   - Log viewer implementation

3. Privacy Features:
   - Consent dialog implementation
   - Local data storage
   - Data reset functionality

4. Enhancement:
   - Real-time updates
   - Improved statistics
   - Better user interface

## Guidelines for Ethical Use

This keylogger should only be used for legitimate purposes such as:
- Personal typing pattern analysis
- Productivity tracking
- Educational purposes
- Personal development

⚠️ **Important**: Always ensure you have proper authorization and consent before using this tool. Using keyloggers without consent may be illegal in your jurisdiction.

## Troubleshooting

1. If the application doesn't start:
   - Ensure all dependencies are installed
   - Check Python version compatibility
   - Verify tkinter is properly installed

2. If no keys are being logged:
   - Confirm you clicked "Start Logging"
   - Check if consent was properly given
   - Verify application has necessary permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Choose an appropriate license and include it here]

## Disclaimer

This tool is for educational and legitimate use only. Users are responsible for ensuring compliance with local laws and regulations regarding keystroke logging.
