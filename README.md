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
Welcome to the ADA project - an exciting venture into the world of hardware-software integration.  At its core, ADA is an exploration of how we can make physical spaces more intelligent and accessible using the power of programming and a sprinkle of electronic ingenutiy.  In this project, we dive into using RFID technology, magnetic read switches, and other components to create a system that's more than just a lock and key.


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

## Hardware Setup
TODO - Detailed setup instructions.

## Development Guide
### Architecture
TODO - Describe the ADA architecture.

### Code Structure
TODO - Explain how the codebase is organized.

### Build Instructions
TODO - Instructions on how to build ADA from source or config.

## Contributing
TODO - Contirubtion guildelines for ADA.

## Testing
### Testing Frameworks and Tools
TODO - Information about ADA testing tools.

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
