# HomeAssistant - Avatto

Custom component - Avatto - to add Avatto devices into Home Assistant

This integration allows full local control of your Avatto devices along with Avatto specific features not available in the official [Tuya](https://www.home-assistant.io/integrations/tuya/) or [local tuya](https://github.com/rospogrigio/localtuya) integrations.

It also allows you to use the application along with the Home Assistant running, or even multiple Home Assistant instances communicating with the same device. While you are using the application, the control via Home Assistant is not available.

## Installation

Copy contents of custom_components/avatto/ to custom_components/avatto/ in your Home Assistant config folder.

## Installation using HACS

**Coming soon**

HACS is a community store for Home Assistant. You can install [HACS](https://github.com/custom-components/hacs) and then install Avatto from the HACS store.

## Requirements

### Network

Broadcast UDP ports 6666 and 6667 **must be open** in firewall for the discovery process.

### Tuya device's Key

There are several ways to obtain the localKey depending on your environment and the devices you own. A good place to start getting info is https://github.com/codetheweb/tuyapi/blob/master/docs/SETUP.md .

### If you block cloud access

You must block DNS requests too (to the local DNS server eg 192.168.1.1). If you only block outbound internet then the device will sit in zombie state, it will refuse / not respond to any connections with the localkey. Connect the devices first with an active internet connection, grab each device localkey and then implement the block.

## Usage

Add devices via Integrations (search for Avatto) in Home Assistant UI.

To add multiple devices, add integration multiple times.

## Have a comment or a suggestion?

Please [open a new issue](https://github.com/JurajNyiri/HomeAssistant-Avatto/issues/new).

## Thank you

- [local tuya](https://github.com/rospogrigio/localtuya) by which this integration has been inspired and uses some parts of it

<a href="https://www.buymeacoffee.com/jurajnyiri" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee"  width="150px" ></a>

# Disclaimer

Author is in no way affiliated with Avatto or Tuya.

Author does not guarantee functionality of this integration and is not responsible for any damage.

All product names, trademarks and registered trademarks in this repository, are property of their respective owners.
