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

## Runtime options (for Windows testing)

List input devices:

```powershell
python speaktype_windows.py --list-devices
```

Use a specific microphone:

```powershell
python speaktype_windows.py --input-device 2
```

Toggle mode instead of hold-to-talk:

```powershell
python speaktype_windows.py --mode toggle
```

Language and model overrides:

```powershell
python speaktype_windows.py --language en --model-size base --compute-type int8
```

Enable auto language detection:

```powershell
python speaktype_windows.py --language auto
```

Clipboard-only fallback (no synthetic paste):

```powershell
python speaktype_windows.py --paste-mode clipboard
```

## Suggested Windows validation checklist

- Verify `--list-devices` shows expected microphone devices.
- Verify default **hold** mode (F8 down/up) records and pastes into Notepad.
- Verify **toggle** mode starts/stops reliably and transcribes once per stop action.
- Verify `--input-device` uses the selected microphone.
- Verify `--paste-mode clipboard` copies transcript even when paste injection is blocked.
- Verify `--language auto` and fixed language mode both produce expected transcripts.

## Notes and limitations

- Default language remains `en`; can now be overridden at runtime.
- Default microphone device is used unless `--input-device` is provided.
- No tray UI or settings UI yet.
- Model defaults to `base` with `int8` compute for broad CPU compatibility.
- Some target apps may block synthetic paste depending on security context.

## Next hardening steps

- Add tray icon + settings panel.
- Add fallback insertion path when synthetic paste is blocked.
