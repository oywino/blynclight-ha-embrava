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
- **GitHub Account**: To host the repository (e.g., `oywino/blynclight-ha-embrava`).
- **GitHub Desktop**: For managing the repository on Windows.

## Installation

### Part 1: Windows Client Setup
1. **Configure Embrava Connect**:
   - Install Embrava Connect and ensure it runs as a service.
   - Set hotkeys: `Ctrl+Alt+R` (Red), `Ctrl+Alt+G` (Green), `Ctrl+Alt+B` (Blue), `Ctrl+Alt+O` (Off).
   - Test hotkeys manually.
2. **Create PowerShell HTTP Server**:
   - Script saved as `C:\Users\Public\Blynclight\blynclight_control.ps1` (see full guide for code).
   - Runs on `http://localhost:5000`, maps actions to hotkeys.
3. **Enable Script Execution**:
   - Run in PowerShell (Admin): `Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy RemoteSigned -Force`.
4. **Set Up Task Scheduler**:
   - Task: `BlynclightControl`, runs `powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File C:\Users\Public\Blynclight\blynclight_control.ps1` at startup with 1-minute delay.
5. **Allow Firewall Access**:
   - Run in PowerShell (Admin): `New-NetFirewallRule -DisplayName "Blynclight Control" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow`.
6. **Test**:
   - Reboot, test with `curl -X POST http://localhost:5000 -H "Content-Type: application/json" -d "{\"action\":\"red\"}"`.

### Part 2: Install via HACS
1. **Add Repository**:
   - HACS > Integrations > “+ Explore & Add Repositories” > `https://github.com/oywino/blynclight-ha-embrava` > “Add”.
   - Click “Blynclight Embrava” > “DOWNLOAD” > Restart HA.
2. **Configure**:
   - Devices & Services > “+ Add Integration” > “Blynclight Embrava” > Host: `http://192.168.1.x:5000` > Submit.

## Usage
- **Entity**: `select.blynclight`
- **Lovelace**: Add an “Entities” card with `select.blynclight` to see a dropdown: “red”, “green”, “blue”, “off”.
- **Action**: Select an option to change the Blynclight state.

## License
MIT License - see [LICENSE](LICENSE) file for details. (Add a `LICENSE` file if sharing publicly.)

## Support
Post questions or issues on the [HA Community Forum](https://community.home-assistant.io/) or [GitHub Issues](https://github.com/oywino/blynclight-ha-embrava/issues).

[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=popout
[forum]: https://community.home-assistant.io/