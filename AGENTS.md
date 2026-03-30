# AGENTS

This repository does not use a full `.agent/` workflow tree. This file is the lightweight agent and contributor guide for Windows-port work.

## Canonical Sources

- Windows architecture, sequencing, parity targets, and packaging order live in [`docs/windows-adaptation/README.md`](docs/windows-adaptation/README.md).
- The runnable transitional Windows MVP lives in [`windows-prototype/`](windows-prototype/README.md).
- Root project messaging in [`README.md`](README.md) should summarize status, not redefine the Windows strategy.

## Required Rules

- Treat [`docs/windows-adaptation/README.md`](docs/windows-adaptation/README.md) as the source of truth for Windows-port decisions.
- Do not introduce a second Windows architecture path in docs or code without updating the canonical plan.
- Do not position the Python MVP as the long-term Windows product shell.
- Keep the parity matrix and packaging progression current when strategy or status changes.
- If a change alters Windows scope, milestones, or responsibilities, update the canonical doc in the same change.

## Documentation Responsibilities

- Update [`README.md`](README.md) when Windows status messaging changes.
- Update [`windows-prototype/README.md`](windows-prototype/README.md) only for tester bootstrap, runtime flags, troubleshooting, and prototype limitations.
- Update [`RELEASE.md`](RELEASE.md) when Windows packaging or release workflow changes.
- Update [`CHANGELOG.md`](CHANGELOG.md) when Windows strategy or support docs are materially revised.
