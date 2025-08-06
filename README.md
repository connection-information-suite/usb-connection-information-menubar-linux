# USB Device Monitor

A lightweight system tray application that provides a GUI wrapper around the `usb-devices` command, making it easy to monitor USB devices in real-time.

## Features

- **GUI wrapper for usb-devices**: Provides a user-friendly interface to the powerful `usb-devices` command
- **Real-time monitoring**: Automatically detects when USB devices are connected or disconnected
- **System tray integration**: Runs unobtrusively in the system tray
- **Detailed device information**: Shows manufacturer, product name, serial number, USB version, speed, and power consumption
- **Cross-platform compatibility**: Works on Linux systems with GTK3 and AppIndicator support
- **Lightweight**: Minimal resource usage while providing comprehensive device monitoring

The application appears as a USB icon in your system tray. Clicking on it reveals a menu with all connected USB devices and their details - essentially a GUI version of running `usb-devices` in the terminal.

## Installation

### From Source

#### Prerequisites

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

#### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/usb-device-monitor.git
   cd usb-device-monitor
   ```

2. Install the Python package:
   ```bash
   pip3 install -e .
   ```

3. Run the application:
   ```bash
   usb-device-monitor
   ```

## Usage

### Starting the Application

Simply run:
```bash
usb-device-monitor
```

The application will start and appear in your system tray.

### Using the Interface

1. **System Tray Icon**: Look for the USB icon in your system tray
2. **Device List**: Click the icon to see all connected USB devices
3. **Device Details**: Click on any device to see detailed information including:
   - Manufacturer
   - Product name
   - Serial number
   - USB version
   - Speed
   - Power consumption
4. **Quit**: Use the "Quit" option in the menu to exit the application

### Auto-start on Boot

To automatically start the application when you log in:

**GNOME:**
1. Open "Settings" → "Applications" → "Startup Applications"
2. Click "Add" and enter:
   - Name: USB Device Monitor
   - Command: `usb-device-monitor`

**KDE:**
1. Open "System Settings" → "Startup and Shutdown" → "Autostart"
2. Click "Add Program" and select `usb-device-monitor`

**Other Desktop Environments:**
Add `usb-device-monitor` to your desktop environment's startup applications list.

### Common Issues

**"Neither AppIndicator3 nor AyatanaAppIndicator3 namespace available"**
- Install the required system packages:
  ```bash
  # Ubuntu/Debian
  sudo apt install gir1.2-ayatanaappindicator3-0.1
  
  # Arch Linux
  sudo pacman -S libayatana-appindicator
  
  # Fedora
  sudo dnf install libappindicator-gtk3
  ```

**"No USB devices found"**
- Ensure `usbutils` is installed (this provides the `usb-devices` command):
  ```bash
  sudo apt install usbutils  # Ubuntu/Debian
  sudo pacman -S usbutils    # Arch Linux
  sudo dnf install usbutils  # Fedora
  ```

**"usb-devices command not found"**
- This application requires the `usb-devices` command from the `usbutils` package:
  ```bash
  sudo apt install usbutils  # Ubuntu/Debian
  sudo pacman -S usbutils    # Arch Linux
  sudo dnf install usbutils  # Fedora
  ```

**Application doesn't appear in system tray**
- Check if your desktop environment supports system tray icons
- Ensure you have the correct AppIndicator packages installed
- Try running the application from terminal to see error messages

### Debug Mode

Run the application with debug output:
```bash
python3 -u usb_device_monitor/main.py
```

## Development

### Project Structure (Work in Progress)

```
usb-device-monitor/
├── usb_device_monitor/
│   ├── __init__.py
│   └── main.py
├── debian/
│   ├── control
│   ├── rules
│   ├── changelog
│   ├── compat
│   ├── usb-device-monitor.desktop
│   ├── usb-device-monitor.1
│   └── usb-device-monitor.svg
├── setup.py
├── requirements.txt
└── README.md
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Report bugs and feature requests on [GitHub Issues](https://github.com/yourusername/usb-device-monitor/issues)
- **Discussions**: Join discussions on [GitHub Discussions](https://github.com/yourusername/usb-device-monitor/discussions)
- **Email**: Contact the maintainer at your.email@example.com

## Changelog

### Version 1.0.0
- Initial release
- USB device monitoring with system tray integration
- Real-time device detection and information display
- Support for both AyatanaAppIndicator3 and AppIndicator3
- Cross-platform compatibility for Linux systems

## Acknowledgments

- Built with Python and GTK3
- Uses PyGObject for GTK bindings
- AppIndicator3/AyatanaAppIndicator3 for system tray integration
- `usbutils` package for the `usb-devices` command that provides all the device information 
