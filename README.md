# USB Connection Information

A lightweight system tray application that provides a GUI wrapper around the `usb-devices` command, making it easy to monitor USB devices in real-time.

Built to bring the [USB Connection Information](https://apps.apple.com/app/id6747853674) Mac App to Linux

## Features

- **GUI wrapper for usb-devices**: Provides a user-friendly interface to the powerful `usb-devices` command
- **Real-time monitoring**: Automatically detects when USB devices are connected or disconnected
- **System tray integration**: Runs unobtrusively in the system tray
- **Detailed device information**: Shows manufacturer, product name, serial number, USB version, speed, and power consumption
- **Cross-platform compatibility**: Works on Linux systems with GTK3 and AppIndicator support
- **Lightweight**: Minimal resource usage while providing comprehensive device monitoring

The application appears as a USB icon in your system tray. Clicking on it reveals a menu with all connected USB devices and their details - essentially a GUI version of running `usb-devices` in the terminal.

## Installation

### From Debian Package (.deb)

**Free Download:**
1. Download the latest `.deb` package from the [releases page](https://github.com/connection-information-suite/usb-connection-information-menubar-linux/releases)
2. Install using your package manager:
   ```bash
   sudo dpkg -i usb-connection-information_*.deb
   sudo apt-get install -f  # Install any missing dependencies
   ```

### From Source

#### Prerequisites

Install the required system dependencies:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1 libgirepository-2.0-dev usbutils
```

**Arch Linux:**
```bash
sudo pacman -S python python-gobject gtk3 libayatana-appindicator usbutils
```

**Fedora:**
```bash
sudo dnf install python3 python3-gobject gtk3 libappindicator-gtk3 usbutils
```

#### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/connection-information-suite/usb-connection-information-menubar-linux.git
   cd usb-connection-information-menubar-linux
   ```

2. Install `uv` (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env  # or restart your shell
   ```

3. Create a virtual environment and install the package:
   ```bash
   uv venv --system-site-packages
   source .venv/bin/activate
   uv pip install -e .
   ```
   > `--system-site-packages` lets the venv use your system-installed PyGObject/Cairo
   > instead of trying to compile them from source, which avoids build errors on most distros.

4. Run the application:
   ```bash
   usb-connection-information
   ```

## Usage

### Starting the Application

Ensure your virtual environment is activated, then run:
```bash
usb-connection-information
```

Or launch it from your applications menu by searching for "USB Connection Information" (if installed system-wide or desktop file is configured).

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

### Application Launcher

The application includes a desktop launcher that will appear in your "Show Applications" menu. After installation, you can:

1. **Launch from Applications Menu**: Click on "Show Applications" (usually the 9-dot grid icon) and search for "USB Connection Information"
2. **Add to Favorites**: Right-click on the launcher and select "Add to Favorites" for quick access
3. **Pin to Dock**: Drag the launcher to your dock/panel for easy access

### Auto-start on Boot

To automatically start the application when you log in:

**GNOME:**
1. Open "Settings" → "Applications" → "Startup Applications"
2. Click "Add" and enter:
   - Name: USB Connection Information
   - Command: `usb-connection-information`

**KDE:**
1. Open "System Settings" → "Startup and Shutdown" → "Autostart"
2. Click "Add Program" and select `usb-connection-information`

**Other Desktop Environments:**
Add `usb-connection-information` to your desktop environment's startup applications list.

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
python3 -u usb_connection_information/main.py
```

## Development

We use `uv` for dependency management and `pre-commit` for code quality.

### Setup Development Environment

1. Clone the repository and install `uv`:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Create a virtual environment with system site packages (for PyGObject):
   ```bash
   uv venv --system-site-packages
   source .venv/bin/activate
   ```
3. Install development dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```
4. Install and run pre-commit hooks:
   ```bash
   uvx pre-commit install
   uvx pre-commit run --all-files
   ```
5. Run tests:
   ```bash
   uv run pytest
   ```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Ensure tests pass and pre-commit hooks succeed
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Report bugs and feature requests on [GitHub Issues](https://github.com/connection-information-suite/usb-connection-information-menubar-linux/issues)
- **Discussions**: Join discussions on [GitHub Discussions](https://github.com/connection-information-suite/usb-connection-information-menubar-linux/discussions)
- **Email**: Contact the maintainer at support@usbconnectioninformation.com

## Acknowledgments

- Built with Python and GTK3
- Uses PyGObject for GTK bindings
- AppIndicator3/AyatanaAppIndicator3 for system tray integration
- `usbutils` package for the `usb-devices` command that provides all the device information
