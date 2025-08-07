#!/usr/bin/env python3

import gi
import os
import threading
import subprocess
import re
import sys
import time
import uuid
import signal

# Import GTK library (this one is usually stable)
gi.require_version('Gtk', '3.0')

# --- AppIndicator Handling ---
# Try to import AyatanaAppIndicator3 first, as it's the modern standard on many systems
try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator3
    print("Using AyatanaAppIndicator3")
except ValueError:
    # If AyatanaAppIndicator3 is not available, try the older AppIndicator3
    try:
        gi.require_version('AppIndicator3', '0.1')
        from gi.repository import AppIndicator3
        print("Using AppIndicator3 (legacy)") # For debugging
    except ValueError:
        print("Error: Neither AppIndicator3 nor AyatanaAppIndicator3 namespace available.")
        print("Please ensure you have the correct system packages installed:")
        print("  For Debian/Ubuntu: sudo apt install gir1.2-ayatanaappindicator3-0.1")
        print("  For Arch Linux: sudo pacman -S libayatana-appindicator")
        print("  For Fedora: sudo dnf install libappindicator-gtk3")
        sys.exit(1) # Exit if neither is found

from gi.repository import Gtk, GLib


# --- Your Existing Code (with minor adjustments) ---

class UsbFallbackParser:
    def parse_usb_devices_fallback(self):
        try:
            output = subprocess.check_output(['usb-devices'], text=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Failed to run 'usb-devices': {e}", file=sys.stderr)
            return {}

        devices = {}
        blocks = output.strip().split('\n\n')

        if len(blocks) <= 1: # Fallback for different usb-devices formats
            lines = output.strip().split('\n')
            blocks = []
            current_block = []
            for line in lines:
                if line.startswith('T:') and current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = [line]
                else:
                    current_block.append(line)
            if current_block:
                blocks.append('\n'.join(current_block))

        for block in blocks:
            lines = block.strip().split('\n')
            entry = self.parse_usb_block(lines)
            if entry:
                unique_key = str(uuid.uuid4())
                devices[unique_key] = entry
        return devices

    def parse_usb_block(self, lines):
        entry = {}
        for line in lines:
            if line.startswith('T:'):
                if m := re.search(r'Spd=\s*(\S+)', line): entry['speed'] = m.group(1)
                if m := re.search(r'Bus=(\d+)', line): entry['bus_info'] = f"Bus {m.group(1)}"
            elif line.startswith('D:'):
                if m := re.search(r'Ver=\s*(\d+\.\d+)', line): entry['version'] = m.group(1)
            elif line.startswith('P:'):
                if m := re.search(r'Vendor=(\S+)\s+ProdID=(\S+)', line):
                    entry['vidpid'] = f"{m.group(1).upper()}:{m.group(2).upper()}"
            elif line.startswith('S:'):
                if 'Manufacturer=' in line: entry['manufacturer'] = line.split('Manufacturer=')[1].strip()
                elif 'Product=' in line: entry['product'] = line.split('Product=')[1].strip()
                elif 'SerialNumber=' in line: entry['serial'] = line.split('SerialNumber=')[1].strip()
            elif line.startswith('C:'):
                if m := re.search(r'MxPwr=\s*(\d+)mA', line):
                    try:
                        watts = (int(m.group(1)) / 1000.0) * 5.0
                        entry['max_power'] = f"{watts:.2f}"
                    except ValueError: pass
        return entry if (entry.get('vidpid') or entry.get('product') or entry.get('manufacturer')) else None

class UsbMonitor(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.daemon = True # Allows main thread to exit even if this thread is running
        self.running = True
        self.callback = callback
        self.last_device_list = set()

    def get_current_devices(self):
        try:
            usb_path = "/sys/bus/usb/devices/"
            if os.path.exists(usb_path):
                return {item for item in os.listdir(usb_path) if ':' not in item}
        except Exception as e:
            print(f"Error getting USB devices: {e}", file=sys.stderr)
        return set()

    def run(self):
        while self.running:
            current_devices = self.get_current_devices()
            if current_devices != self.last_device_list:
                self.last_device_list = current_devices
                # Schedule the callback to run on the main GTK thread
                GLib.idle_add(self.callback)
            time.sleep(2) # Check every 2 seconds

    def stop(self):
        self.running = False

# --- New GUI Application Class ---

class UsbMenuApp:
    def __init__(self):
        # Unique ID for the app indicator
        self.app_id = 'usb-connection-information'
        # Use a standard system icon for USB
        self.icon = 'drive-removable-media-usb'
        
        self.parser = UsbFallbackParser()
        
        self.indicator = AppIndicator3.Indicator.new(
            self.app_id, self.icon,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        
        self.menu = Gtk.Menu()
        self.indicator.set_menu(self.menu)
        
        # Start monitoring and build the initial menu
        self.rebuild_menu()
        self.monitor = UsbMonitor(self.rebuild_menu)
        self.monitor.start()

    def rebuild_menu(self):
        # Clear existing menu items
        for i in self.menu.get_children():
            self.menu.remove(i)
            
        # Get current device list
        devices = self.parser.parse_usb_devices_fallback()
        
        if not devices:
            item = Gtk.MenuItem(label="No USB devices found")
            item.set_sensitive(False)
            self.menu.append(item)
        else:
            for device_key, info in devices.items():
                product = info.get('product', 'Unknown Device')
                vidpid = info.get('vidpid', '')
                
                # Main menu item for the device
                main_item_label = f"{product} ({vidpid})" if vidpid else product
                main_item = Gtk.MenuItem(label=main_item_label)
                
                # Create a submenu for device details
                submenu = Gtk.Menu()
                main_item.set_submenu(submenu)
                
                # Populate submenu with details
                details = []
                if info.get('manufacturer') not in (None, '', 'N/A'):
                    details.append(f"Manufacturer: {info.get('manufacturer')}")
                if vidpid:
                    details.append(f"VID:PID: {vidpid}")
                if info.get('serial') not in (None, '', 'N/A'):
                    details.append(f"Serial: {info.get('serial')}")
                if info.get('version') not in (None, '', 'N/A'):
                    details.append(f"USB Version: {info.get('version')}")
                if info.get('speed') not in (None, '', 'N/A'):
                    details.append(f"Speed: {info.get('speed')} Mbps")
                if info.get('max_power') not in (None, '', '0.00', 'N/A'):
                    details.append(f"Power: {info.get('max_power')} W")
                
                for detail_text in filter(None, details):
                    sub_item = Gtk.MenuItem(label=detail_text)
                    sub_item.set_sensitive(False) # Make details non-clickable
                    submenu.append(sub_item)
                
                self.menu.append(main_item)
        
        # Add Separator and Quit Button
        self.menu.append(Gtk.SeparatorMenuItem())
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit)
        self.menu.append(quit_item)
        
        self.menu.show_all()

    def quit(self, _):
        self.monitor.stop()
        Gtk.main_quit()

def main():
    # Allow Ctrl+C to work in the terminal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    print("USB Device Monitor started. Check the system tray for the icon.")
    UsbMenuApp()
    Gtk.main()

if __name__ == "__main__":
    sys.exit(main())