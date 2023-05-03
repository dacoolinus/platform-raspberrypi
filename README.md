# Platform.Pico: development platform for [PlatformIO](https://platformio.org) and the Raspeberry Pi Pico

# Why Platform.Pico

Per the Platformio documentation, there are three core functions that a Development platform, or platform, are supposed to perform:

1.  The PlatformIO Build System Scripts for the supported frameworks and SDKs
2. Pre-Configured presets for embedded circuit boards
3. Pre-compiled toolchains and related tools for the architecture(s)

The Official Platformio platform for the RP2040 exclusively supports arduino as a framework and does not support the [C/C++ SDK](https://github.com/raspberrypi/pico-sdk) provided by Raspeberry Pi or other frameworks that could be ported to the platform without relying on arduino(FreeRTOS, Zephyr, etc).

Furthermore, the lack of native support for using picoprobe as a default debyggung tool causes a lot of friction for development. 

Platform.Pico sets out to solve the lack of flexibility provided by the original Platform-RaspberryPi. 

# Why Plaform-RaspberryPi

[![Build Status](https://github.com/platformio/platform-raspberrypi/workflows/Examples/badge.svg)](https://github.com/dacoolinus/platform.pico/actions)

RP2040 is a low-cost, high-performance microcontroller device with a large on-chip memory, symmetric dual-core processor complex, deterministic bus fabric, and rich peripheral set augmented with a unique Programmable I/O (PIO) subsystem, it provides professional users with unrivalled power and flexibility.

* [Home](https://registry.platformio.org/platforms/platformio/raspberrypi) (home page in the PlatformIO Registry)
* [Documentation](https://docs.platformio.org/page/platforms/raspberrypi.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](https://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](https://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = raspberrypi
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/platformio/platform-raspberrypi.git
board = ...
...
```

# Configuration

Please navigate to [documentation](https://docs.platformio.org/page/platforms/raspberrypi.html).
