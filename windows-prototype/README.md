# SpeakType Windows Prototype

This folder contains a **workable Windows MVP prototype** for SpeakType:

- Hold **F8** to record
- Release **F8** to transcribe locally
- Transcript is copied to clipboard and pasted with **Ctrl+V**

## What this prototype includes

- Global hotkey capture (`keyboard`)
- Microphone capture (`sounddevice`)
- Local Whisper transcription (`faster-whisper`)
- Clipboard + paste (`pyperclip` + synthetic `Ctrl+V`)

## Requirements

- Windows 10/11
- Python 3.10+
- Microphone permission enabled
- Running terminal as Administrator may be required for global key hooks in some environments

## Setup

```powershell
cd windows-prototype
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```powershell
python speaktype_windows.py
```

Then:
1. Focus any text field (Notepad, browser text area, etc.)
2. Hold `F8` and speak
3. Release `F8`
4. Transcript is pasted automatically

## Notes and limitations

- Prototype currently forces `language="en"` for predictable MVP behavior.
- Uses default microphone device.
- No tray UI or settings UI yet.
- Model defaults to `base` with `int8` compute for broad CPU compatibility.
- Some target apps may block synthetic paste depending on security context.

## Next hardening steps

- Add device selection and language selection.
- Add push-to-talk/toggle modes.
- Add tray icon + settings panel.
- Add fallback insertion path when synthetic paste is blocked.
