# Blynclight Embrava
[![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/github/v/release/oywino/blynclight-ha-embrava)
[![Community Forum][forum-shield]][forum]

Controls a Blynclight Plus device in Home Assistant via Embrava Connect hotkeys and a PowerShell HTTP server. Uses a `select` entity to switch between red, green, blue, or off states.

## Features
- Integrates with Embrava Connect’s global hotkeys.
- Simple dropdown control in Lovelace (`select.blynclight`).
- Local communication via PowerShell HTTP server.
- No external dependencies beyond `aiohttp`.

## Prerequisites
- **Windows PC**: Running Embrava Connect with a Blynclight Plus connected via USB.
- **Home Assistant**: With HACS installed for custom integrations.

## Installation

### Part 1: Windows Client Setup
1. **Configure Embrava Connect**:
   - Install Embrava Connect and ensure it runs as a service.
   - Set hotkeys: `Ctrl+Alt+R` (Red), `Ctrl+Alt+G` (Green), `Ctrl+Alt+B` (Blue), `Ctrl+Alt+O` (Off).
   - Test hotkeys manually to confirm color changes.
2. **Set Up PowerShell HTTP Server**:
   - Requires a script running on `http://localhost:5000` to map actions (`"red"`, `"green"`, `"blue"`, `"off"`) to hotkeys. See detailed setup in the [full guide](https://github.com/oywino/blynclight-ha-embrava/wiki).
   - Test with: `curl -X POST http://localhost:5000 -H "Content-Type: application/json" -d "{\"action\":\"red\"}"`.

### Part 2: Install via HACS
1. **Add Repository**:
   - In HACS: Integrations > “+ Explore & Add Repositories” > Enter `https://github.com/oywino/blynclight-ha-embrava` > “Add”.
   - Click “Blynclight Embrava” > “DOWNLOAD” > Restart Home Assistant.
2. **Configure**:
   - In HA: Devices & Services > “+ Add Integration” > Search “Blynclight Embrava” > Set Host to `http://<your-windows-ip>:5000` (e.g., `http://192.168.1.x:5000`) > Submit.

## Usage
- **Entity**: `select.blynclight`
- **Lovelace**: Add an “Entities” card with `select.blynclight` to see a dropdown: “red”, “green”, “blue”, “off”.
- **Action**: Select an option to change the Blynclight state.

## License
MIT License - see [LICENSE](LICENSE) file for details.

## Support
Post questions or issues on the [HA Community Forum](https://community.home-assistant.io/) or [GitHub Issues](https://github.com/oywino/blynclight-ha-embrava/issues).

[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=popout
[forum]: https://community.home-assistant.io/