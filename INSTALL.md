# Installation Guide

## Step 1: Install Python

Since Python is not currently installed on your system, you need to install it first:

### Option A: Download from python.org (Recommended)

1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.12 (latest stable version)
3. **IMPORTANT**: During installation, check the box that says **"Add Python to PATH"**
4. Click "Install Now" or "Customize installation" (both work)
5. Wait for installation to complete

### Option B: Install from Microsoft Store

1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Install"
4. This automatically adds Python to PATH

## Step 2: Verify Installation

Open a new PowerShell or Command Prompt window and run:

```powershell
python --version
```

You should see something like: `Python 3.11.x` or `Python 3.12.x`

## Step 3: Install Dependencies

Once Python is installed, navigate to this folder in PowerShell/Command Prompt and run:

```powershell
cd C:\Sources\quarm-quick-character-copy
python -m pip install -r requirements.txt
```

This will install:
- `customtkinter` - Modern GUI library
- `pillow` - Image processing (required by customtkinter)

## Step 4: Run the Application

```powershell
python character_manager.py
```

## Troubleshooting

### "python is not recognized"
- Make sure you checked "Add Python to PATH" during installation
- Try restarting your terminal/PowerShell window
- Try using `py` instead of `python`: `py -m pip install -r requirements.txt`

### "pip is not recognized"
- Try: `python -m pip install -r requirements.txt`
- Or: `py -m pip install -r requirements.txt`

### Still having issues?
- Reinstall Python and make sure to check "Add Python to PATH"
- Or manually add Python to your system PATH environment variable

