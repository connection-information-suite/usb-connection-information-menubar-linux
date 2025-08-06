# Contributing to USB Device Monitor

Thank you for your interest in contributing to USB Device Monitor! This document provides guidelines and information for contributors.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit your changes with a descriptive commit message
7. Push to your fork and submit a pull request

## Development Setup

### Prerequisites

Install the required system dependencies:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1 usbutils
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip python-gobject gtk3 libayatana-appindicator usbutils
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip python3-gobject gtk3 libappindicator-gtk3 usbutils
```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/connection-information-suite/usb-connection-information-menubar-linux.git
   cd usb-connection-information-menubar-linux
   ```

2. Install in development mode:
   ```bash
   pip3 install -e .
   ```

3. Run the application:
   ```bash
   usb-device-monitor
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and concise
- Use type hints where appropriate

## Testing

Before submitting a pull request, please:

1. Test the application on different Linux distributions if possible
2. Verify that USB device detection works correctly
3. Test the system tray integration
4. Ensure the application starts and stops cleanly
5. Check that error handling works as expected

## Commit Messages

Use clear, descriptive commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

Example:
```
Add support for USB 3.2 devices

- Update device parsing to handle new USB 3.2 speed indicators
- Add fallback parsing for devices without speed information
- Fix issue with power consumption calculation

Closes #123
```

## Pull Request Guidelines

1. **Title**: Use a clear, descriptive title
2. **Description**: Explain what the PR does and why
3. **Testing**: Describe how you tested the changes
4. **Screenshots**: Include screenshots for UI changes
5. **Related Issues**: Link to any related issues

## Reporting Issues

When reporting issues, please include:

1. **Operating System**: Distribution and version
2. **Python Version**: `python3 --version`
3. **GTK Version**: `gtk3-demo --version` (if available)
4. **Steps to Reproduce**: Clear, step-by-step instructions
5. **Expected Behavior**: What you expected to happen
6. **Actual Behavior**: What actually happened
7. **Error Messages**: Any error messages or logs
8. **Screenshots**: If applicable

## Feature Requests

When requesting features, please:

1. Describe the feature in detail
2. Explain why it would be useful
3. Provide examples of how it would work
4. Consider implementation complexity

## Code of Conduct

This project is committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and considerate in all interactions.

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing, please:

1. Check the existing issues and discussions
2. Create a new discussion for general questions
3. Open an issue for specific problems
4. Contact the maintainer at dan@usbconnectioninformation.com

Thank you for contributing to USB Device Monitor!
