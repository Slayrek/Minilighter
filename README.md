# Minilighter

Minilighter is a lightweight screen highlighting utility designed for presentations or screen sharing. It works similarly to the Windows Snipping Tool, but instead of taking a screenshot, it creates a dashed border around the selected area while dimming the rest of the screen.

## Features

- **Global Shortcut:** Quickly trigger the highlight overlay from anywhere (default `Alt+Shift+H`).
- **Two Behavior Modes:**
  - *Fade out:* The highlighted area disappears automatically after a specified time.
  - *Persist:* The highlighted area stays on the screen (allowing mouse clicks to pass through) until you press `Esc`.
- **Settings:** An easy-to-use settings dialog accessible via the system tray.
- **Startup Integration:** Includes simple scripts to add or remove the application from Windows startup.

## Installation (For Users)

1. Download `Minilighter.exe` (from releases or build it yourself).
2. Run `Minilighter.exe`. The application icon will appear in your system tray.
3. To add the application to Windows startup, run `add_to_startup.bat`.
4. To remove it from startup, run `remove_from_startup.bat`.

## Building from Source

You will need Python 3 and the following dependencies:

```bash
pip install PyQt5 keyboard pyinstaller
```

To build the standalone `.exe` file:

```bash
pyinstaller --noconsole --onefile --name Minilighter main.py
```

The executable will be located in the `dist/` folder.

## Usage

1. Run the application.
2. Press the global shortcut (default `Alt+Shift+H`).
3. Click and drag your left mouse button to highlight an area on the screen.
4. Release the mouse button. The area will stay highlighted based on your behavior settings.
5. To close the highlight manually at any time, press the `Esc` key.
6. To configure the shortcut, timeout, or behavior, right-click the yellow icon in the system tray and select **Settings**.
