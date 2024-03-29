# ADA
## Project Folder Structure
```
ADA/
│
├── src/
│	├── __init__.py
│	├── database/
│	│	├── __init__.py
│	│	├── implementations/
│	│	│	├── __init__.py
│	│	│	└── json_database.py
│	│	│
│	│	└── interfaces/
│	│		├── __init__.py
│	│		└── database_interface.py
│	│	
│	├── hardware/
│	│	├── __init__.py
│	│	├── implementations/
│	│	│	├── __init__.py
│	│	│	├── continuous_mfrc522_scanner.py
│	│	│	├── continuous_switch_monitor.py
│	│	│	├── mrfc522_reader.py
│	│	│	├── pi_gpio_switch_operator.py
│	│	│	└── pi_gpio_switch_reader.py
│	│	│
│	│	└── interfaces/
│	│		├── __init__.py
│	│		├── continuous_monitor_interface.py
│	│		├── hardware_interface.py
│	│		├── rfid_reader_interface.py
│	│		├── toggle_interface.py
│	│		└── toggle_monitoring_interface.py
│	│
│	├── schemas/
│	│   ├── __init__.py
│	│	└── member_schema.py
│	│
│	└── utils/
│		├── __init__.py
│		├── logging_utils.py
│		└── threading_shared_variable.py
│
├── tests/
│	├── __init__.py
│	├── database/
│	│	├── implementations/
│	│	│	└── test_json_database_interface.py
│	│   │
│	│	└── interfaces/
│	│		└── test_database_interface.py
│	│
│	└── hardware/
│		├── implementations/
│		│	├── test_pi_gpio_switch_operator.py
│		│	└── test_pi_gpio_switch_reader.py
│		│
│		└── interfaces/
│			└── test_toggle_interface.py
│
├── logs/
│	└── ada.log
│
├── ada.py
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements-dev.txt
├── requirements.txt
└── setup.py
```

# ADA (Advanced Doorway Access)
Welcome to the ADA project - a venture into the world of hardware-software integration.  At its core, ADA is an exploration of how we can make physical spaces more intelligent and accessible using the power of programming and a sprinkle of electronic ingenutiy.  In this project, we're using RFID technology, magnetic read switches, and other components to create a system that's more than just a lock and key.


## Table of Contents
- [Technology Used](#technology-used)
- [Features](#features)
- [Getting Started](#getting-started)
- [Detailed Usage Guide](#detailed-usage-guide)
- [Hardware Setup](#hardware-setup)
- [Development Guide](#development-guide)
- [Contributing](#contributing)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact Information](#contact-information)
- [Changelog](#changelog)

## Technology Used
| Type | Technology | Project Use |
|------|------------|-----|
| Software | [Python 3.11.7](https://www.python.org/) | Programming and scripting |
| Libraries/Frameworks | [RPi.GIO](https://pypi.org/project/RPi.GPIO/) | Interfacing with Raspberry Pi GPIO pins |
| Libraries/Frameworks | [spidev](https://pypi.org/project/spidev/) | SPI (Serial Peripheral Interface) communication, used with RFID |
| Libraries/Frameworks | [mfrc522](https://pypi.org/project/mfrc522/) | Interfacing with RFID module |
| Libraries/Frameworks | [python-dotenv](https://pypi.org/project/python-dotenv/) | Managing environment variables |
| Libraries/Frameworks | [PyTest](https://docs.pytest.org/en/7.4.x/) | Unit testing |
| Libraries/Frameworks | [python-dateutil](https://pypi.org/project/python-dateutil/) | Parsing date/time strings and computing recurrences |
| Libraries/Frameworks | [zoneinfo](https://docs.python.org/3/library/zoneinfo.html) | IANA Time Zone calculations |
Libraries/Frameworks | [tzdata](https://pypi.org/project/tzdata/) | Data for `zoneinfo` to compute Time Zones |
| Libraries/Frameworks | [isodate](https://pypi.org/project/isodate/) | Parsing ISO 8601 durations
| Hardware | [Raspberry Pi 4B 8GB](https://www.adafruit.com/product/4564) | Hardware platform for interfacing with components |
| Hardware | [12V Strike Lock](https://www.amazon.com/dp/B0B6HS7JGD) | Electric door latch for automatically locking/unlocking |
| Hardware | [MFRC522](https://www.amazon.com/dp/B0CC4JGN3P) | RFID Reader |
| Hardware | [Reed Switch](https://www.amazon.com/dp/B093FFTQYK/) | Interfacing with door open/close status |

## Features
TODO - Describe the main features and functionality of ADA.

***Draft:***

The ADA (Automated Door Access) project is a comprehensive solution designed to enhance security and access management for various premises. Leveraging the power of Raspberry Pi and RFID technology, ADA offers a seamless and flexible approach to control and monitor door access. Here are some of the standout features of the ADA project:

* **RFID-Based Authentication:** Utilizes RFID technology for fast and secure identification of individuals, providing a keyless entry system that enhances both security and convenience.

* **Modular Business Logic:** Designed with modularity in mind, allowing for easy customization and expansion of business logic to meet specific security requirements and scenarios.

* **Real-Time Access Control:** Offers immediate validation against a centralized database, ensuring only authorized individuals can access the premises. This includes support for different member levels and access privileges.

* **Temporary Access Management:** Supports the creation and validation of temporary access intervals using the ISO 8601 standard, allowing for flexible access control for guests or temporary workers.

* **Responsive Design:** Implements a non-blocking main loop with threading to ensure high responsiveness and minimal CPU usage, allowing ADA to quickly respond to access requests and hardware events without lag.

* **Hardware Integration:** Provides detailed instructions and support for integrating with various hardware components, including RFID scanners, switches, and GPIO-based door latches, making it adaptable to a wide range of physical security setups.

* **Environment Variable Configuration:** Facilitates easy configuration through environment variables, enabling quick setup and adjustments without altering the core code.

* **Extensive Logging:** Features comprehensive logging for monitoring access events, troubleshooting, and ensuring accountability and traceability of access attempts.

* **Security Best Practices:** Adheres to security best practices, including data validation and secure handling of member information, to protect against unauthorized access and data breaches.

* **Open Source and Community-Driven:** As an open-source project, ADA encourages community contributions, offering a platform for developers to share improvements, new features, and hardware compatibility extensions.

ADA is ideal for small to medium-sized organizations, makerspaces, and community centers looking for a DIY solution to door access control. Its flexibility and open design also make it an excellent educational tool for those interested in learning about RFID technology, security principles, and hardware integration.

## Getting Started
### Prerequisites
TODO - List the prerequisites for installing ADA.

### Installation
TODO - Step-by-step installation instructions.

### Basic Usage
TODO - Quick-start guide and basic usage instructions.

## Detailed Usage Guide
### Configuration
TODO - Details on how to configure ADA.

### Operating Instructions
TODO - Instructions for using all the features of ADA.

### API Documentation
TODO - Include API documentation or link to source.

***Draft***:

Below is an overview of the primary interfaces and methods available to developers:
Member Management API:

**Member Management API**
* add_member(member_info)
    * Description: Adds a new member to the database.
    * Parameters:
        * member_info (dict): A dictionary containing member information following the member_schema.
    * Returns: The added member information or None if the operation fails.
* get_member(member_query)
    * Description: Retrieves member information based on the provided query.
    * Parameters:
        * member_query (dict): A dictionary with query parameters (e.g., {"obf_rfid": "<RFID_VALUE>"}).
    * Returns: A dictionary containing the member's information if found, None otherwise.
* update_member(member_info)
    * Description: Updates the information of an existing member.
    * Parameters:
        * member_info (dict): A dictionary containing the updated member information.
    * Returns: The updated member information or None if the operation fails.

* delete_member(member_query)
    * Description: (Optional, if implemented) Removes a member from the database.
    * Parameters:
        * member_query (dict): A dictionary with query parameters to identify the member to delete.
    * Returns: Boolean indicating the success or failure of the operation.

**Hardware Interaction API**
* unlock_door(duration)
    * Description: Unlocks the door for a specified duration.
    * Parameters:
        * duration (int): Time in seconds for which the door should remain unlocked.
    * Returns: None.
* read_rfid()
    * Description: Initiates an RFID read operation.
    * Returns: The RFID code read or None if no tag is detected.
* set_mode(mode)
    * Description: Sets the operating mode of the system.
    * Parameters:
        * mode (str): The desired mode of operation (e.g., "active", "inactive").
    * Returns: None.

**Utility Functions**
* get_temp_access_interval()
    * Description: Generates a temporary access interval string based on current settings.
    * Returns: A string representing the temporary access interval in ISO 8601 format.
* is_within_access_interval(interval_str)
    * Description: Checks if the current time is within the specified access interval.
    * Parameters:
        * interval_str (str): The access interval in ISO 8601 format.
    * Returns: Boolean indicating if the current time falls within the access interval.

**Extensibility**

The ADA project's API is designed to be extensible, allowing for future enhancements such as additional hardware support, new member management functionalities, or integration with external systems without breaking existing functionality.

Example Usage:

```python
# Example: Adding a new member
member_info = {
    "obf_rfid": "some_unique_rfid_code",
    "member_level": "member",
    "membership_status": "active",
    ...
}
added_member = add_member(member_info)
print(added_member)

```

## Hardware Setup
TODO - Detailed setup instructions.

## Development Guide
### Architecture
TODO - Describe the ADA architecture.

### Code Structure
TODO - Explain how the codebase is organized.

***Draft:***

The ADA project is structured to promote modularity, readability, and ease of extension. At its core, ADA blends hardware interactions with business logic to create a seamless access control system. Below is a breakdown of the project's directory structure and descriptions of key components:

* src/: This directory contains the source code for ADA, organized into subdirectories by functionality.
    * database/: Implements the database interface and provides concrete implementations, such as JsonDatabase, for storing and retrieving member data.
    * hardware/: Contains classes for interfacing with the hardware components like RFID readers, switches, and actuators. This includes reader and monitor implementations for continuous polling and state management.
    * utils/: Offers utility functions and classes that support logging, threading, and environment variable management.
    * schemas/: Defines the data schemas used within the project, such as member_schema, ensuring consistent data handling and validation.

* ada.py: The main entry point for the ADA application. It orchestrates the initialization of hardware components, database connections, and the main event loop responsible for handling access control logic based on the current mode and sensor inputs.

* .env: Environment variables file that stores configuration settings, such as database connection details and GPIO pin assignments, allowing for easy adjustments to different hardware setups or preferences.

* Dockerfile and docker-compose.yml (if applicable): For projects aimed at containerization, these files define how to build and deploy ADA in a Docker environment, emphasizing portability and ease of deployment.

Extending ADA

Developers looking to extend ADA with new features or hardware integrations should focus on the following areas:

* Adding New Hardware Components: Implement additional classes in src/hardware/ following the interfaces established by existing components. Ensure that new hardware integrations are encapsulated within their modules to maintain separation of concerns.

* Business Logic Enhancements: To introduce new access control logic or modify existing behaviors, ada.py is the starting point. This may involve adding new methods or altering the main loop's conditionals to accommodate additional modes or functionalities.

* Database Adaptations: For projects requiring different database backends, implement new classes within src/database/ adhering to the DatabaseInterface interface. This allows switching between database implementations without altering the business logic.

8 Utilizing Environment Variables: When adding new features or hardware, expose configuration options as environment variables in the .env file, ensuring that ADA remains flexible and configurable without code changes.

This structured approach ensures that ADA remains adaptable to various access control scenarios, hardware configurations, and future enhancements.

### Build Instructions
TODO - Instructions on how to build ADA from source or config.

## Contributing
TODO - Contirubtion guildelines for ADA.

## Testing
### Testing Frameworks and Tools
Draft

The ADA project uses a combination of testing frameworks and tools to ensure the quality and reliability of the software. Below are the key frameworks and tools utilized in our testing environment:

**Pytest**

* **Description**: Pytest is a powerful testing framework that simplifies the creation, organization, and execution of tests in Python. It is used for writing unit tests as well as functional and integration tests for the ADA project.
* **Installation**: Pytest can be installed using pip. If not already installed, you can install it by running:
```python
pip install pytest
```
* **Running Tests**: To run the tests with Pytest, navigate to the project root directory and execute:
```python
pytest
```
**Pytets-mock**

* **Description**: Pytest-mock is a plugin for Pytest that provides a convenient interface for mocking in tests. It is used extensively in the ADA project for mocking external dependencies and hardware interfaces.
* **Installation**: It comes installed with Pytest if you followed the Pytest installation instructions. If needed separately, you can install it using pip:
```python
pip install pytest-mock
```
* **Usage**: Pytest-mock is automatically recognized by Pytest. Mock objects can be created using the 'mocker' fixture in your test functions.

### Running Tests
TODO - Instructions on how to run tests.

## Deployment
TODO - Instructions and guidelines for deploying ADA.

## Troubleshooting
TODO - List common issues and their solutions (FAQ?).

## License
TODO - License.

## Acknowledgments
TODO

## Contact Information
TODO

## Changelog
TODO - (maybe)
