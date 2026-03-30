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

## Windows user-testing runbook (post-PR)

Use this flow when validating or reporting issues during Windows testing:

1. Confirm environment:
   - Windows version (10/11)
   - Python version (`python --version`)
   - Whether terminal is elevated (Administrator)
2. Validate setup on a clean virtual environment:
   - `pip install -r requirements.txt`
   - `python speaktype_windows.py --list-devices`
3. Validate core flow in at least two target apps:
   - Notepad
   - Browser text area (for example, web form/chat input)
4. Validate both recording modes:
   - hold mode (default)
   - `--mode toggle`
5. Validate fallback behavior:
   - run once with default `--paste-mode ctrlv`
   - run once with `--paste-mode clipboard`
6. Record all failures with the bug report fields below.

### Bug report fields required from testers

- Windows version and hardware (CPU/RAM)
- Command used to run prototype
- Input device index/name
- Target app where paste was attempted
- Expected behavior vs actual behavior
- Terminal output (copy/paste)
- Repro steps and frequency (always/intermittent)

## Notes and limitations

- Default language remains `en`; can now be overridden at runtime.
- Default microphone device is used unless `--input-device` is provided.
- No tray UI or settings UI yet.
- Model defaults to `base` with `int8` compute for broad CPU compatibility.
- Some target apps may block synthetic paste depending on security context.

## Troubleshooting

### Hotkey does not trigger
- Try running terminal as Administrator.
- Ensure another app is not already consuming the same global hotkey.
- Try a different key using `--hotkey` (for example `--hotkey f9`).

### No audio captured / empty transcript
- Run `--list-devices` and select a specific mic via `--input-device`.
- Check Windows microphone privacy settings.
- Speak for longer than minimum duration (`--min-duration` defaults to 0.2s).

### Transcript copied but not pasted
- Some applications block synthetic key injection.
- Re-run with `--paste-mode clipboard` and paste manually as fallback.
- Capture app name and behavior in bug report.

### Slow first transcription
- First run may be slower due to model initialization.
- Re-test a second utterance before reporting latency issues.

## Next hardening steps

- Add tray icon + settings panel.
- Add richer insertion fallback path (for example UI Automation send-text) beyond clipboard-only mode.
