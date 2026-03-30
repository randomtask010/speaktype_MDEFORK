# SpeakType

<div align="center">

![SpeakType Icon](speaktype/Assets.xcassets/AppIcon.appiconset/icon_256x256.png)

**Fast, Offline Voice-to-Text — macOS App + Windows Porting Fork**

![SpeakType app screenshot](image.png)
[![Download](https://img.shields.io/badge/Download-SpeakType.dmg-blueviolet?logo=apple&logoColor=white)](https://github.com/karansinghgit/speaktype/releases/latest)
[![Swift](https://img.shields.io/badge/Swift-5.9-orange?logo=swift)](https://swift.org)
[![Platform](https://img.shields.io/badge/Platform-macOS%20stable%20%7C%20Windows%20adaptation-blue)](docs/windows-adaptation/README.md)
[![License](https://img.shields.io/badge/License-MIT-red)](LICENSE)

*Press a hotkey, speak, and instantly paste text anywhere — with an active Windows transition plan in this fork.*

</div>

---

## What is SpeakType?

SpeakType is a **privacy-first, offline voice dictation tool**. The upstream app is macOS-first, and this fork is focused on porting the core dictation workflow to Windows while keeping local, offline transcription as the baseline requirement.

- **Privacy First** - Zero data leaves your Mac
- **Lightning Fast** - Optimized for Apple Silicon
- **Works Everywhere** - Any app, any text field
- **Open Source** - Audit every line of code yourself

### Fork status: Windows adaptation

- macOS app remains the primary production implementation.
- The canonical Windows transition plan lives in [`docs/windows-adaptation/README.md`](docs/windows-adaptation/README.md).
- The end-state Windows target is a native C# desktop shell with a shared cross-platform core.
- The runnable Windows Python MVP in [`windows-prototype/`](windows-prototype/README.md) is temporary tester tooling, not the long-term Windows product shell.
- Repo-level contributor and agent guidance for Windows-port work lives in [`AGENTS.md`](AGENTS.md).

---

## Installation

### Requirements (macOS app)

- macOS 13.0+ (Ventura or newer)
- Apple Silicon (M1+) recommended
- 2GB available storage (for AI models)

### Download (macOS app)

**[Download Latest Release](https://github.com/karansinghgit/speaktype/releases/latest)**

1. Download `SpeakType.dmg`
2. Drag **SpeakType** to **Applications**
3. Grant Microphone + Accessibility + Documents Folder permissions
4. Download an AI model from Settings → AI Models

Press `fn` to start dictating.

### Windows adaptation (this fork)

For Windows architecture, migration phases, portability decisions, and release direction:

- [`docs/windows-adaptation/README.md`](docs/windows-adaptation/README.md)

For transitional Windows tester setup, runtime options, troubleshooting, and user-testing checklist:

- [`windows-prototype/README.md`](windows-prototype/README.md)

### Build from Source (macOS app)

```bash
git clone https://github.com/karansinghgit/speaktype.git
cd speaktype
make build && make run
```

---

## Usage

1. Press hotkey (`fn` by default)
2. Speak your text
3. Release hotkey
4. Text appears!

**Tips:**
- Speak naturally - Whisper handles accents well
- Say punctuation: "comma", "period", "question mark"
- Best results with 3-10 second clips

---

## Development

```bash
make build          # Build debug
make run            # Run app
make clean          # Clean build
make test           # Run tests
make dmg            # Create DMG installer
```

### Current Issues

⚠️ When loading a model for the first time / switching to another model, there is a startup delay of 30-60 seconds. 

So the first transcription will appear ultra slow, but it will go back to instantaneous dictation right after it's warmed up. 

### Windows adaptation development notes

- The Makefile targets in this repository are macOS/Xcode-oriented.
- Windows porting strategy and sequencing are defined in `docs/windows-adaptation/README.md`.
- Windows testing currently progresses through the Python MVP in `windows-prototype/` until the native Windows shell is ready.

### Project Structure

```
speaktype/
├── App/           # Entry point
├── Views/         # SwiftUI interface
├── Models/        # Data models
├── Services/      # Core functionality
├── Controllers/   # Window management
└── Resources/     # Assets & config
```

### Tech Stack

- **Swift 5.9+** / SwiftUI + AppKit
- **[WhisperKit](https://github.com/argmaxinc/WhisperKit)** - Local Whisper inference
- **[KeyboardShortcuts](https://github.com/sindresorhus/KeyboardShortcuts)** - Global hotkeys
- **AVFoundation** - Audio capture

---

## Contributing

1. Fork & clone
2. Create a branch: `git checkout -b feature/my-feature`
3. Make changes and run `make lint`
4. Submit a PR

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Credits

- [WhisperKit](https://github.com/argmaxinc/WhisperKit) by Argmax
- [OpenAI Whisper](https://github.com/openai/whisper)

---

<div align="center">

**Made with ❤️ for developers**

*Privacy-first • Open Source *

</div>
