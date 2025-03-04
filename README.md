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

#### Step 1: Configure Embrava Connect
- Install Embrava Connect and ensure it runs as a service.
- Set hotkeys: `Ctrl+Alt+R` (Red), `Ctrl+Alt+G` (Green), `Ctrl+Alt+B` (Blue), `Ctrl+Alt+O` (Off).
- Test hotkeys manually to confirm color changes.

#### Step 2: Set Up PowerShell HTTP Server
- Open Notepad, paste the following script, and save as `C:\Users\Public\Blynclight\blynclight_control.ps1`:
```powershell
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Keyboard {
    [DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    public const byte VK_CONTROL = 0x11;
    public const byte VK_MENU = 0x12;
    public const byte VK_R = 0x52;
    public const byte VK_G = 0x47;
    public const byte VK_B = 0x42;
    public const byte VK_O = 0x4F;
    public const uint KEYEVENTF_KEYUP = 0x0002;
    public static void SendHotkey(char key) {
        byte vk;
        switch (key) {
            case 'R': vk = VK_R; break;
            case 'G': vk = VK_G; break;
            case 'B': vk = VK_B; break;
            case 'O': vk = VK_O; break;
            default: return;
        }
        keybd_event(VK_CONTROL, 0, 0, UIntPtr.Zero);
        keybd_event(VK_MENU, 0, 0, UIntPtr.Zero);
        keybd_event(vk, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(100);
        keybd_event(vk, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }
}
"@

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://+:5000/")
$listener.Start()

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        $response.Headers.Add("Content-Type", "application/json")

        if ($request.HttpMethod -eq "POST") {
            $reader = New-Object System.IO.StreamReader($request.InputStream)
            $body = $reader.ReadToEnd() | ConvertFrom-Json
            $action = $body.action

            $hotkeys = @{
                "red" = "R"
                "green" = "G"
                "blue" = "B"
                "off" = "O"
            }

            if ($hotkeys.ContainsKey($action)) {
                [Keyboard]::SendHotkey($hotkeys[$action])
                $response.StatusCode = 200
                $responseBody = @{ "status" = "success"; "action" = $action } | ConvertTo-Json -Compress
            } else {
                $response.StatusCode = 400
                $responseBody = @{ "error" = "Invalid action" } | ConvertTo-Json -Compress
            }
        } else {
            $response.StatusCode = 405
            $responseBody = @{ "error" = "Method Not Allowed" } | ConvertTo-Json -Compress
        }

        $buffer = [System.Text.Encoding]::UTF8.GetBytes($responseBody)
        $response.ContentLength64 = $buffer.Length
        $response.OutputStream.Write($buffer, 0, $buffer.Length)
        $response.Close()
    }
} finally {
    $listener.Stop()
}
```
- Notes: This script runs an HTTP server on port 5000, mapping `"red"`, `"green"`, `"blue"`, `"off"` to the hotkeys set in Embrava Connect.

#### Step 3: Enable Script Execution
- Open PowerShell as Administrator and run:
```powershell
Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy RemoteSigned -Force
```

#### Step 4: Configure Task Scheduler
- Open Task Scheduler > “Create Task”:
  - **General**: Name: `BlynclightControl`, check “Run with highest privileges” and “Run only when user is logged on”.
  - **Trigger**: “At startup”, delay by 1 minute.
  - **Action**: Program: `powershell.exe`, Arguments: `-WindowStyle Hidden -ExecutionPolicy Bypass -File C:\Users\Public\Blynclight\blynclight_control.ps1`.
  - **Conditions**: Uncheck “Start only if on AC power”.
  - **Settings**: Uncheck “Stop if runs longer than”.
- Save with admin credentials.

#### Step 5: Allow Firewall Access
- In PowerShell (Admin):
```powershell
New-NetFirewallRule -DisplayName "Blynclight Control" -Direction Inbound -Protocol TCP -LocalPort 5000 -```

#### Step 6: Test Server
- Reboot PC, wait 1-2 minutes, test:
```cmd
curl -X POST http://localhost:5000 -H "Content-Type: application/json" -d "{\"action\":\"red\"}"
```
- Verify all actions: `"red"`, `"green"`, `"blue"`, `"off"`.

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
