# File Revision Management System

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Watchdog Version](https://img.shields.io/badge/watchdog-2.1%2B-green)
![Status](https://img.shields.io/badge/Under%20Development-green)
![Status](https://img.shields.io/badge/GUI-purple)

A Python script for monitoring and managing file revisions based on file modifications. This script uses the Watchdog library to track changes in specified files and directories, creating new revisions with timestamps when changes occur.

## Features

- Continuous monitoring of specified files and directories.
- Automatic creation of new file revisions upon modification.
- Configuration management through a CSV file.
- Duplicate file prevention based on MD5 checksum.
- Flexible and customizable for different file revision needs.
- Intrutive Graphical User Interface.
- Notification via Email.
- **Upcoming** Automatically Cleanup of older revisions.
- **Upcoming** Dark Mode

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Watchdog library (version 2.1 or higher)

### Installation

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/nanaksingh13/FileRevisionManager.git
   ```

2. Install the required dependencies:

   ```shell
   pip install watchdog
   pip install hashlib
   pip install tkinter
   pip install pathlib
   ```

### Usage

1. Run the script:

   ```shell
   python gui.py
   ```

2. The script will continuously monitor the specified files and directories for changes and create revisions as needed.

### GUI

![Screenshot 2023-09-13 015910](https://github.com/nsdhanoa/FileRevisionManager/assets/66524832/d48e7a49-5629-4e26-9c81-76daa6c629ba)


### Upcoming Feature

- [x] **Batch Import/Export:** Allow users to import a batch of file configurations at once (from a CSV or JSON file) or export the current configurations.
- [x] **Drag and Drop:** Allow users to drag and drop files into the GUI for monitoring, rather than only using the file dialog.
- [x] **Search Bar:** Add a search bar at the top of the configuration table to allow users to easily find a particular file or revision directory.
- [ ] **Real-time Notification:** Implement desktop notifications to alert the user when a file has been modified.
- [ ] **Themes and Customization:** Allow users to switch between light and dark themes. Also, let users customize the look and feel, such as font types, sizes, and colors.
- [ ] **Help and Documentation:** Integrate a help section that provides a user guide, FAQ, and troubleshooting tips.
- [x] **UI/UX Improvements:** Better more intrutive, mordern interface.

## Author

- Nanak Singh
- GitHub: [nanaksingh13](https://github.com/nanaksingh13)
