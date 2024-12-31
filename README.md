# Group Member Finder

Group Member Finder is a Python-based automation tool that uses Selenium to interact with a web-based student group management system. The tool allows users to search for specific individuals across a range of groups and saves the results in a file for further review.

## Features

- **Automated Login**: Automatically logs into the system using your credentials.
- **Group Member Retrieval**: Extracts a list of members from specified groups.
- **Name Matching**: Searches for target individuals within each group's member list.
- **Results Export**: Saves detailed search results to a text file.
- **Retry Mechanism**: Attempts multiple logins in case of failure.

## Prerequisites

To use this tool, ensure you have the following installed:

- Python 3.8+
- Google Chrome Browser
- ChromeDriver (compatible with your Chrome version)
- Required Python libraries:
  - `selenium`

## Setup

1. Clone the repository or download the script file.
2. Install the required dependencies:

   ```bash
   pip install selenium
   ```
3. Download and set up ChromeDriver:
   - [Download ChromeDriver](https://sites.google.com/chromium.org/driver/)
   - Add the `chromedriver` executable to your system's PATH or place it in the same directory as the script.

4. Update the configuration:
   - Replace `YOUR_LOGIN_HERE` and `YOUR_PASSWORD_HERE` in the script with your actual login credentials.
   - Modify `START_GROUP_ID` and `END_GROUP_ID` to define the range of group IDs you want to scan.
   - Populate `TARGET_NAMES` with the names of individuals you are searching for in the format:
     ```python
     TARGET_NAMES = [
         {"First Name": "John", "Last Name": "Doe", "Found": False},
         {"First Name": "Jane", "Last Name": "Smith", "Found": False}
     ]
     ```

## Usage

Run the script using Python:

```bash
python group_member_finder.py
```

### Workflow

1. **Login**: The script navigates to the login page and submits your credentials.
2. **Group Scanning**: For each group in the specified range, it retrieves the member list.
3. **Name Search**: Checks if any of the target names are in the member list.
4. **Results Saving**: Saves the findings to `results.txt` in the current directory.

### Example Output

The `results.txt` file will contain lines like:

```
Results:
==============================
Found: John Doe in group ID 13001
Not found: Jane Smith
==============================
```

## Notes

- Make sure you have access to the student group management system and valid credentials.
- The script assumes consistent HTML structure on the target website. Changes in the website's layout may require updates to the script.
- Adjust `MAX_RETRIES` and `WebDriverWait` times as needed to handle varying network speeds or website load times.

## Disclaimer

This script is for educational purposes only. Ensure you have permission to access and interact with the target system before use.

## License

This project is open-source and available under the MIT License. See the LICENSE file for more information.
