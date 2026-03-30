# SpeakType Windows Adaptation Plan

## 1) Objective
Adapt SpeakType from a macOS-only desktop app into a Windows-capable app while preserving core behavior:
- Push-to-talk global hotkey recording
- Local/offline transcription
- Instant insertion into the active app
- Menu/tray-driven control flow
- Model download and local model management

## 2) Current-State Assessment (from this repo)
The current implementation is tightly coupled to Apple platforms:
- **Build/toolchain**: Xcode project, `xcodebuild`, macOS packaging/signing/notarization scripts.
- **UI/app lifecycle**: SwiftUI app with `NSApplicationDelegateAdaptor`, `MenuBarExtra`, AppKit window control.
- **macOS system APIs**:
  - Accessibility trust checks: `AXIsProcessTrusted*`
  - Input/shortcut hooks: `NSEvent`, `CGEventTap`, `CGEvent`
  - Clipboard/paste: `NSPasteboard` + synthetic Cmd+V
  - Windowing and shell actions: `NSWindow`, `NSPanel`, `NSWorkspace`, `NSAlert`
- **Audio stack**: AVFoundation capture and playback.
- **ML runtime**: WhisperKit/CoreML-first assumptions.

## 3) Target Cross-Platform Strategy
Use a **shared core + platform adapters** architecture.

### 3.1 Core (shared)
Keep or extract into shared modules:
- Domain models (`AIModel`, settings, history, transcription state)
- Business logic (download workflow, transcription orchestration, trial/license policy)
- Persistence and app settings contracts
- Logging contracts

### 3.2 Platform adapters
Introduce interfaces and two concrete implementations:
- **macOSAdapter** (existing behavior)
- **WindowsAdapter** (new)

Adapter responsibilities:
- Global hotkey registration and key state tracking
- Microphone permission checks/prompts
- Accessibility/input-injection capability checks
- Clipboard operations and active-app paste execution
- App lifecycle hooks, tray icon behavior, notifications, URL/open actions
- OS-specific file paths for models/cache/history

## 4) Dependency and API Migration Plan
Replace direct macOS framework usage behind abstractions.

| Capability | Current (macOS) | Windows Target |
|---|---|---|
| Global hotkeys | `NSEvent`, `CGEventTap` | Win32 `RegisterHotKey` (or low-level keyboard hook when required) |
| Text insertion | `CGEvent` Cmd+V + Accessibility | Clipboard + synthetic Ctrl+V using `SendInput` (or UI Automation fallback) |
| Permission checks | Accessibility + AVFoundation authorization | Microphone capability checks, UAC-sensitive input simulation checks |
| Clipboard | `NSPasteboard` | Win32 clipboard API (`OpenClipboard`, `SetClipboardData`) |
| Tray/menu | `MenuBarExtra` / AppKit | System tray (`Shell_NotifyIcon`) via chosen UI framework |
| Launch URLs/files | `NSWorkspace` | `ShellExecute`/`Process.Start` equivalent |
| Audio capture | AVFoundation | WASAPI/MediaCapture abstraction |
| Whisper runtime | WhisperKit/CoreML | ONNX Runtime + whisper.cpp backend (evaluate and choose) |

## 5) Architecture Refactor Workstreams

### Workstream A: Platform Abstraction Layer
1. Identify all direct AppKit/Cocoa/ApplicationServices usage.
2. Define protocol boundaries for:
   - `HotkeyService`
   - `ClipboardService`
   - `PermissionService`
   - `WindowOverlayService`
   - `SystemIntegrationService` (open URL/file, app activation)
3. Move current macOS implementations behind these protocols.
4. Ensure no feature module calls macOS APIs directly.

### Workstream B: App Shell Strategy
Choose one of:
1. **Swift cross-platform shell** if feasible for Windows delivery requirements.
2. **Native Windows shell + shared core** (recommended if tray/hotkey/input reliability is priority).

Decision criteria:
- Reliability for global hotkeys and foreground paste
- Tray/overlay UX parity
- Team expertise and maintenance burden
- Packaging/signing simplicity on Windows

### Workstream C: Audio + Transcription Runtime
1. Decouple transcription engine from WhisperKit-specific types.
2. Introduce `TranscriptionEngine` interface.
3. Provide:
   - macOS WhisperKit adapter
   - Windows engine adapter (ONNX/whisper.cpp)
4. Standardize model metadata, storage layout, checksum validation.
5. Add migration logic for model location differences by OS.

### Workstream D: UX/Behavior Parity
1. Recreate mini recorder overlay and status states.
2. Recreate onboarding for permissions and first-model setup.
3. Preserve push-to-talk and toggle modes.
4. Maintain history/statistics/settings behavior with platform-aware options.

### Workstream E: Build, Packaging, and Distribution
1. Add Windows build pipeline (Debug + Release).
2. Add Windows installer flow (MSIX or signed installer).
3. Add release automation equivalent to current macOS release scripts.
4. Add update strategy for Windows (in-app updater or installer-based updates).

### Workstream F: Test and Quality Strategy
1. Extend unit tests to target platform-agnostic core.
2. Add adapter contract tests per platform.
3. Add smoke tests for:
   - global hotkey capture
   - recording start/stop
   - transcription completion
   - clipboard paste into common apps (Notepad, browser text fields, Office app)
4. Add regression suite for model download/cancel/retry and corrupted model recovery.

## 6) Incremental Delivery Phases

### Phase 0: Discovery & Design
- Finalize shell/runtime choices.
- Produce API boundary spec and dependency decision record.
- Define parity requirements and non-goals.

### Phase 1: Refactor for Separation (macOS still primary)
- Introduce interfaces and macOS adapters.
- Remove direct platform calls from core logic.
- Keep behavior unchanged on macOS.

### Phase 2: Windows MVP (functional parity for core flow)
- Global hotkey
- Audio capture
- Local transcription
- Clipboard insert/paste
- Basic tray control + settings + model download

### Phase 3: Hardening and UX parity
- Overlay polish, onboarding parity, update flow, error recovery.
- Performance tuning and startup latency optimization.

### Phase 4: Release Readiness
- Signed builds
- Installer validation
- Cross-version upgrade tests
- Support docs and troubleshooting guide

## 7) Risk Register and Mitigations
- **Risk: Input injection blocked by policy/app context**  
  Mitigation: layered fallbacks (clipboard-only mode, UI Automation fallback, clear user guidance).

- **Risk: Global hotkey collisions / unreliable keyboard hooks**  
  Mitigation: configurable shortcuts, conflict detection, robust hook lifecycle management.

- **Risk: Whisper runtime performance gaps on low-end Windows devices**  
  Mitigation: model tier recommendations, RAM checks, dynamic defaults, benchmark gate before release.

- **Risk: Divergent behavior across platform code paths**  
  Mitigation: shared core contracts + cross-platform behavioral tests + parity checklist.

- **Risk: Installer/update trust issues (AV false positives, signing mistakes)**  
  Mitigation: code signing in CI, reputation-building release cadence, staged rollout.

## 8) Definition of Done (Windows adaptation)
A Windows release is considered complete when:
1. User can install/uninstall cleanly.
2. App can run at login (if enabled), live in tray, and open settings/dashboard.
3. Hotkey reliably starts/stops recording.
4. Speech transcribes locally with downloadable models.
5. Result text inserts into common target apps with documented fallback behavior.
6. Crash/error telemetry/logging is available for support.
7. CI builds and tests pass for both macOS and Windows targets.
8. User documentation includes Windows setup, permissions, troubleshooting, and known limitations.

## 9) Adaptation Backlog Status (execution)

Status legend:
- ✅ Completed
- 🔄 In progress
- ⏭️ Next
- 🧪 User-testing prep

### 9.1 Platform strategy
1. 🔄 Approve target Windows shell and long-term transcription backend.
2. ⏭️ Confirm adapter boundaries for hotkey, clipboard/paste, permission, and system integration services.

### 9.2 Current MVP delivery
1. ✅ Minimal Windows prototype exists for hotkey + recording + transcription + paste.
2. ✅ Prototype supports hold and toggle modes, device selection, language override/auto, and clipboard-only fallback.
3. 🔄 Harden insertion behavior and fallback guidance for apps that block synthetic paste.

### 9.3 Core adaptation work
1. ⏭️ Implement platform abstraction interfaces in current codebase.
2. ⏭️ Migrate existing macOS services behind adapter layer with no behavior change.
3. ⏭️ Introduce cross-platform transcription engine contract and Windows implementation path.

### 9.4 Build/release and validation
1. ⏭️ Establish Windows CI build and artifact publishing.
2. ⏭️ Add repeatable Windows smoke tests for key workflows (Notepad, browser textarea, Office app).
3. 🧪 Publish test runbook and issue template for user testing feedback capture.

## 10) Windows User Testing Readiness (post-PR target)

This fork is targeting post-PR Windows user testing of the MVP flow with clear support guidance.

### Ready now
- Working prototype CLI flow in `windows-prototype/`.
- Local transcription (faster-whisper), global hotkey capture, clipboard + paste attempt.
- Validation checklist and runtime options documented.

### Must be true before test invitation
1. A single canonical support guide exists and matches current CLI/runtime flags.
2. Known limitations are explicit (admin requirements, app-specific paste blocking, no tray UI yet).
3. Testers can collect and share reproducible bug reports (input device, mode, target app, error text).
4. Backlog priorities for blocking issues are clearly marked.

### Go/No-Go gate for user testing
- **Go**: setup succeeds on clean Windows 10/11 machine, hold/toggle flows transcribe, clipboard fallback works.
- **No-Go**: cannot reliably complete basic record/transcribe/copy flow in common apps.
