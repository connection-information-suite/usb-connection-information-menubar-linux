# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-06

### Added
- Initial release of USB Device Monitor
- System tray application for monitoring USB devices
- Real-time device detection and information display
- Support for both AyatanaAppIndicator3 and AppIndicator3
- Cross-platform compatibility for Linux systems
- GUI wrapper for the `usb-devices` command
- Detailed device information including manufacturer, product name, serial number, USB version, speed, and power consumption
- Debian package support
- Comprehensive documentation and installation instructions

### Technical Details
- Built with Python 3.8+ and GTK3
- Uses PyGObject for GTK bindings
- AppIndicator3/AyatanaAppIndicator3 for system tray integration
- `usbutils` package integration for device information parsing
