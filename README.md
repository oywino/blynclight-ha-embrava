## How to Install

### Part 1: Windows Client Setup
[Unchanged from previous steps]

### Part 2: Install the Integration via HACS
1. **Add Repository to HACS**:
   - HACS > Integrations > “+ Explore & Add Repositories” > Add `https://github.com/oywino/blynclight-ha-embrava` > Click on Download.
2. **Configure in HA**:
   - Devices & Services > “+ Add Integration” > Search “Blynclight Embrava” > Enter host (e.g., `http://192.168.1.x:5000`) where x is the adresseof your client PC where Blynclight is connected.
3. **Restart HA**:
   - Restart Home Assistant if prompted.
4. ## Usage
- Entity: `select.blynclight`
- Add to UI using an "Entities" card to see a dropdown with "red", "green", "blue", "off".
- Select an option to change the Blynclight Plus state.
