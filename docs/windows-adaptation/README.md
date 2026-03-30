# SpeakType Windows Transition Plan

This document is the canonical Windows strategy and execution guide for this fork.

- The production app in this repository is still the macOS SwiftUI/AppKit implementation.
- The Windows Python MVP in [`windows-prototype/`](../../windows-prototype/README.md) exists only as a transitional tester bootstrap.
- All Windows-port decisions, milestones, and documentation updates must align with this file.

## Objective and End-State

Port SpeakType from a macOS-first desktop app to a Windows-capable product without regressing the core dictation workflow:

- push-to-talk or toggle recording
- local, offline transcription
- insertion into the active app with documented fallbacks
- tray-driven access to controls and status
- local model download and management
- onboarding, history, settings, and update flow parity

The target Windows product is a native C# desktop app with a shared cross-platform core and platform adapters.

## Current-State Gap Analysis

The current app is tightly coupled to Apple frameworks and build tooling:

- Build and release are driven by Xcode, `xcodebuild`, DMG packaging, notarization, and macOS-only scripts.
- App lifecycle depends on SwiftUI scenes, `NSApplicationDelegateAdaptor`, `MenuBarExtra`, and AppKit window management.
- Hotkey handling relies on `NSEvent`, `CGEventTap`, and Fn-specific event suppression.
- Clipboard and insertion rely on `NSPasteboard`, `CGEvent`, and Accessibility trust.
- Audio capture and playback rely on AVFoundation.
- Transcription is implemented through WhisperKit with CoreML-oriented assumptions.

Windows support in-repo today is limited to the Python CLI prototype:

- global hotkey via `keyboard`
- microphone capture via `sounddevice`
- local transcription via `faster-whisper`
- clipboard copy and attempted `Ctrl+V`

That prototype is useful for user-testing continuity, but it is not the end-state architecture.

## Locked Architecture Decisions

The following choices are locked for Windows-port work in this fork:

- Windows shell: native C# desktop shell.
- Native host layer: WPF is the primary Windows UI host for the first production port because it is mature for tray, hotkey, window, and input-injection integration.
- Shared architecture: shared core plus platform adapters.
- Transitional Windows path: keep the Python MVP only until the native shell proves core-flow parity.
- Packaging progression: portable Windows build first for internal and tester validation; signed installer and optional MSIX follow after workflow stability.
- Hotkey strategy: Win32-native registration or hook path, not a web-shell abstraction.
- Text insertion strategy: clipboard-first with synthetic paste, plus documented fallback modes for blocked apps.
- Audio strategy: Windows-native capture abstraction, not direct reuse of AVFoundation assumptions.
- Windows transcription runtime: non-CoreML backend. The Python MVP may validate runtime choices, but it is not the long-term app shell.

## Shared-Core Extraction Map

The shared core should contain behavior that is product-specific but not OS-shell-specific:

- transcription orchestration and recording-state transitions
- model metadata, selection rules, checksum policy, and local storage conventions
- settings schema and persistence contracts
- history storage contracts and statistics derivation
- licensing and trial policy
- logging contracts and support diagnostics

The following existing app areas are expected to inform core extraction:

- models and settings
- history and statistics calculations
- model download workflow
- transcription normalization and orchestration

The following must remain behind platform adapters:

- hotkey monitoring
- permission prompting and trust checks
- clipboard access and insertion
- tray/menu shell
- overlay windows and focus behavior
- URL, file, and shell actions
- OS-specific storage roots and app lifecycle hooks

## Required Cross-Platform Contracts

These interfaces are required and must be explicitly introduced during the refactor.

| Contract | Responsibility | Current macOS source | Windows target |
|---|---|---|---|
| `TranscriptionEngine` | Load models, transcribe files/chunks, expose runtime capability/errors | WhisperKit-backed service | Windows runtime adapter backed by a non-CoreML engine |
| `HotkeyService` | Register global hotkeys, track press/release state, expose conflicts/errors | `NSEvent` and `CGEventTap` handling | Win32 registration/hook implementation |
| `AudioCaptureService` | Start/stop recording, enumerate devices, stream or persist audio | AVFoundation recording services | Windows-native audio capture abstraction |
| `ClipboardInsertionService` | Copy transcript, attempt insertion, expose fallback mode | `NSPasteboard` plus synthetic paste | Win32 clipboard plus `Ctrl+V` simulation and fallback handling |
| `PermissionService` | Report and request microphone/input-injection capability | AVFoundation and Accessibility trust checks | Windows microphone and input-simulation capability checks |
| `WindowOverlayService` | Show recorder overlay, status changes, and focus-safe dismissal | AppKit mini-recorder window controller | Native WPF overlay window management |
| `SystemIntegrationService` | Open files/URLs, launch on login, notifications, app activation | `NSWorkspace` and AppKit integration | Windows shell integration |
| `ModelRepository` | Resolve model catalog, install state, download state, storage roots | WhisperKit model download workflow | Shared catalog plus Windows-specific storage/download adapter |
| `SettingsStore` | Persist app settings and feature flags | `UserDefaults`-backed settings | Windows-backed settings persistence |
| `HistoryStore` | Persist transcripts, audio references, and derived stats | Current history persistence service | Shared history contract with Windows storage backend |

## Windows Shell Responsibilities

The native Windows shell owns all user-facing platform behavior:

- tray icon and quick actions
- onboarding flow and permissions guidance
- dashboard/settings/history UI
- hotkey configuration UI
- recorder overlay and status feedback
- active-app insertion behavior and fallback messaging
- update prompts and release-channel display

The Windows shell must not re-implement product rules already defined in the shared core.

## Migration Phases and Exit Criteria

### Phase 0: Canonical strategy and repo alignment

Deliverables:

- this document becomes the single source of truth
- root docs point here consistently
- the Python MVP is documented as transitional, not final

Exit criteria:

- no repo doc implies the Python CLI is the long-term Windows product
- no repo doc presents an alternative Windows architecture

### Phase 1: Adapter seams in the macOS app

Deliverables:

- isolate direct AppKit, Cocoa, ApplicationServices, and AVFoundation dependencies behind the required contracts
- keep macOS behavior unchanged

Exit criteria:

- feature modules no longer call platform APIs directly
- macOS build and tests continue to pass

### Phase 2: Shared-core extraction

Deliverables:

- define a platform-neutral core module for settings, history, transcription orchestration, model metadata, and state transitions
- move persistence and runtime contracts out of the shell layer

Exit criteria:

- macOS uses the shared core through macOS adapters
- core logic is testable without AppKit or AVFoundation

### Phase 3: Native Windows shell implementation

Deliverables:

- WPF shell for tray, settings, onboarding, history, and overlay
- Win32-backed hotkey, clipboard, insertion, permission, and system-integration adapters
- Windows-native audio capture adapter
- Windows transcription engine adapter

Exit criteria:

- Windows can complete record, transcribe, copy, and paste in common target apps
- toggle and hold modes behave consistently with macOS

### Phase 4: Parity hardening and tester migration

Deliverables:

- replace Python MVP as the primary validation path
- preserve the Python prototype only as a fallback tool during limited overlap
- document known app-specific insertion limitations and fallback behavior

Exit criteria:

- native Windows shell is the primary documented test target
- parity checklist passes for onboarding, recording, transcription, history, and settings

### Phase 5: Packaging, signing, CI, and release readiness

Deliverables:

- portable Windows build for internal and tester distribution
- signed installer flow after portable-build stabilization
- Windows CI build and smoke-test coverage
- support and release docs updated for Windows lifecycle

Exit criteria:

- Windows release artifacts can be produced repeatably
- CI validates key Windows flows
- docs clearly differentiate portable, installer, and future MSIX paths

## Parity Matrix

| Capability | macOS status | Windows target | Current Windows status |
|---|---|---|---|
| Global hotkey dictation | Shipping | Native Win32-backed hotkey service | Python MVP only |
| Hold and toggle recording | Shipping | Same behavior through shared state model | Python MVP supports both |
| Local transcription | Shipping via WhisperKit | Native Windows runtime through `TranscriptionEngine` | Python MVP supports local transcription |
| Clipboard copy and active-app insertion | Shipping | Clipboard-first insertion with fallback modes | Python MVP supports copy plus attempted paste |
| Tray-driven control flow | Shipping | Native WPF tray shell | Not implemented |
| Overlay/status window | Shipping | Native WPF overlay | Not implemented |
| Settings UI | Shipping | Native Windows settings UI backed by shared contracts | Not implemented |
| History and stats UI | Shipping | Native Windows history/stats UI backed by shared stores | Not implemented |
| Model management UI | Shipping | Native Windows model-management UI backed by shared repository | Not implemented |
| Update flow | Shipping for macOS DMG releases | Windows portable then installer update strategy | Not implemented |
| Release automation | Shipping for macOS | Windows CI plus packaging pipeline | Not implemented |

## Risks and Mitigations

- Input injection may be blocked by target app context or security boundary.
  - Mitigation: clipboard-first behavior, clear fallback mode, app-specific guidance, and documented repro capture.
- Global hotkey behavior may conflict with system or app shortcuts.
  - Mitigation: configurable hotkeys, conflict detection, and robust hook lifecycle management.
- Windows runtime performance may vary widely by CPU and RAM.
  - Mitigation: model-tier recommendations, benchmark gate, conservative defaults, and tester hardware capture.
- Shared-core extraction may destabilize the shipping macOS app.
  - Mitigation: phase the work behind adapters first and keep macOS behavior unchanged until contracts are proven.
- Windows packaging and signing may lag functional parity.
  - Mitigation: portable build first, then signed installer, then optional MSIX.

## Testing and Validation Strategy

### Core validation

- unit tests for shared orchestration, normalization, settings rules, history calculations, and model-state transitions
- adapter contract tests for macOS and Windows implementations

### Windows smoke validation

Run repeatable smoke tests for:

- hotkey registration and cancellation
- hold mode and toggle mode
- microphone selection
- transcription completion
- clipboard copy
- paste into Notepad
- paste into a browser text field
- fallback behavior when synthetic paste is blocked

### Acceptance criteria for Windows readiness

Windows is ready to replace the Python MVP as the primary test target when:

1. setup succeeds on a clean Windows 10 or 11 machine
2. record, transcribe, and copy work reliably
3. paste works in common apps with documented fallback behavior where blocked
4. settings and history persist correctly
5. crashes and support logs are collectable

## Packaging and Release Progression

Packaging order is fixed:

1. portable Windows build for internal validation and tester pilots
2. signed installer after the portable build is stable
3. optional MSIX only after installer and update workflow maturity

The current repository release automation remains macOS-only until Windows packaging work is explicitly added.

## Ownership and Update Rules

- This document is the source of truth for Windows architecture, sequencing, and status.
- [`README.md`](../../README.md) should summarize Windows status, not redefine strategy.
- [`windows-prototype/README.md`](../../windows-prototype/README.md) should describe only how to run and validate the transitional MVP.
- Any change to Windows architecture, packaging order, prototype role, or parity target must update this document in the same change.
- Do not introduce parallel Windows approaches in code or docs without updating this plan and the parity matrix.

## Immediate Next Steps

1. Introduce the required platform contracts in the current app without changing macOS behavior.
2. Extract shared transcription, settings, model, and history logic behind those contracts.
3. Stand up the native WPF Windows shell and Win32-backed adapters.
4. Keep the Python MVP available only until the native shell completes core-flow parity.
