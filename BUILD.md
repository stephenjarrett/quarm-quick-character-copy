# Building the Executable

This document explains how to build a Windows executable from the source code.

## Automated Build (Recommended)

The easiest way to get a build is through GitHub Actions:

1. **Create a Release on GitHub:**
   - Go to your repository on GitHub
   - Click "Releases" → "Create a new release"
   - Tag a version (e.g., `v1.0.0`)
   - Add release notes
   - Click "Publish release"

2. **Download the Executable:**
   - GitHub Actions will automatically build the executable
   - Once complete, the `.exe` file will be attached to the release
   - Download `QuarmQuickCharacterCopy.exe` from the release page

## Manual Build (Local)

If you want to build locally on Windows:

### Prerequisites
- Python 3.11 or later
- pip

### Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Build the executable:**
   ```bash
   py -m PyInstaller build.spec --clean --noconfirm
   ```

3. **Find the executable:**
   - The executable will be in the `dist/` folder
   - File name: `QuarmQuickCharacterCopy.exe`

### Building Options

The build configuration is in `build.spec`. Key settings:

- **Single file executable:** All dependencies bundled into one `.exe`
- **No console window:** `console=False` (GUI app)
- **UPX compression:** Enabled to reduce file size

### Troubleshooting

- **Antivirus warnings:** Some antivirus software may flag PyInstaller executables. This is a false positive. You may need to add an exception or sign the executable.

- **Missing modules:** If the executable fails to run, you may need to add missing imports to `hiddenimports` in `build.spec`.

- **Large file size:** The executable includes Python and all dependencies, so it will be ~50-100MB. This is normal.

## Distribution

The executable is standalone - users don't need Python installed. Just distribute the `.exe` file.

