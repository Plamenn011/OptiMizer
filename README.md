# OptiMizer - Advanced Performance & Registry Engine

OptiMizer is an industrial-grade system optimization tool designed to reduce input lag, clean OS bloating, and unlock maximum hardware stability for gaming. Built with Python and CustomTkinter, it features a glassmorphic cyber-telemetry interface utilizing native Windows API injections.

## Operational Profiles

- **Efficient:** Triggers a real-time deep purge of Windows `%TEMP%` cache and locks background process leaks. Features a precise telemetry counter showing data cleared in Megabytes (MB).
- **Normal:** Applies baseline OS visual tweaks, disabling desktop transparency effects, taskbar widgets, and telemetry micro-tasks to free up core memory.
- **Maximum (Admin Required):** Modifies deep Windows Registry keys. Disables Core Isolation (VBS), CPU mitigations, and blocks background services like `GameBarPresenceWriter.exe` to dramatically cut latency.
- **ULTRA (Hardware Boost):** Injects native console protocols to force hidden Windows power management configurations (**Ultimate Performance GUID**), overrides CPU thermal throttling limits, and locks system timer resolution to an ultra-stable **0.5ms**.

## Core Architecture

- **Python 3.14+** - Logic and multi-threaded script sequencing.
- **CustomTkinter** - Cyberpunk-themed text fields and reactive progress gauges.
- **Windows Win32 API (`ctypes` / `winreg`)** - Low-level kernel and registry data manipulation.
- **Pillow (PIL)** - High-fidelity borderless full-screen background scaling.

## Deployment & Compilation

To build the project into a single compiled binary deployment (`.exe`) file, locate your repository folder and run:

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "fondo_insti.png;." --icon="logo.ico" "OptiMizer.py"
```

## Disclaimer

This utility modifies critical system registry cells and kernel parameters. Usage is strictly **at your own risk**. The developer takes no responsibility for hardware instability, data loss, or system faults.

## License

Licensed under the **MIT License**. Created by Plamen T. (Plamenn011).
