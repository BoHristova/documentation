---
title: Vale Linter
---

The Gardener documentation uses [Vale](https://vale.sh/) to enforce writing style and consistency. Vale runs automatically on pull requests and checks only the lines you changed.

## Install Vale Locally

Run the install script for your operating system from the repository root. The script installs Vale and syncs the Gardener style rules.

**macOS**

```bash
bash hack/install-vale-macos.sh
```

**Linux**

```bash
bash hack/install-vale-linux.sh
```

**Windows** (PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File hack/install-vale-windows.ps1
```

## Run Vale Locally

To lint the files you have changed compared to `origin/master`:

```bash
make vale
```

This mirrors what runs in CI — only your changed lines are checked.

## Editor Integration

Install the [Vale VS Code extension](https://marketplace.visualstudio.com/items?itemName=ChrisChinchilla.vale-vscode) to see Vale issues inline as you write. The extension picks up `.vale.ini` automatically and highlights problems on save.

For JetBrains IDEs, install the [Vale plugin](https://plugins.jetbrains.com/plugin/19613-vale-cli).

## Rules

The following rules are active for all Gardener documentation:

| Rule | Level | What it checks |
|:---|:---|:---|
| `Gardener.Articles` | warning | Correct "a" vs "an" before acronyms (e.g. "an API", "a VM") |
| `Gardener.BritishSpellings` | warning | American English spelling ("color" not "colour") |
| `Gardener.CommandPrompt` | error | No `$` prefix in code blocks |
| `Gardener.Links` | warning | No generic link text ("here", "click here") |
| `Gardener.SecondPerson` | warning | Address the reader as "you", not "the user" |
| `Gardener.Terms` | error | Correct capitalisation of brand names (Kubernetes, GitHub, etc.) |
| `Gardener.WordChoice` | warning | Inclusive terminology (allowlist, denylist, etc.) |
| `Vale.Repetition` | error | Repeated consecutive words ("the the") |
| `Vale.Spelling` | error | Spelling against Gardener, Kubernetes, and tech vocabulary |

## Suppressing False Positives

To disable Vale for a section of a file:

```markdown
<!-- vale off -->

Content that should not be checked.

<!-- vale on -->
```

To disable a single rule inline:

```markdown
<!-- vale Gardener.Terms = NO -->
This is an exception.
<!-- vale Gardener.Terms = YES -->
```
