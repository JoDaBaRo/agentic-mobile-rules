# Agentic Mobile Rules

A collection of Cursor rule files (`.mdc`) that turn the Cursor agent into a
productive mobile-dev teammate.

## What's in here

```
agentic-mobile-rules/
├── README.md                    ← you are here
├── Android/
│   ├── ADAPTING.md              ← find-and-replace guide for your project
│   ├── android-project.mdc              (alwaysApply: true — every-chat behavior)
│   ├── android-project-onboarding.mdc   (on-demand — joining an existing team)
│   └── android-project-bootstrap.mdc    (on-demand — brand-new project from zero)
└── iOS/
    ├── README.md                ← iOS-specific overview + comparison table
    ├── ADAPTING.md              ← find-and-replace guide for your project
    ├── ios-project.mdc                  (alwaysApply: true — every-chat behavior)
    ├── ios-project-onboarding.mdc       (on-demand — joining an existing team)
    └── ios-project-bootstrap.mdc        (on-demand — brand-new project from zero)
```

## What these rules teach the agent to do

**Android:**
- **Drive the Android toolchain via CLI** Gradle, `adb`, `sdkmanager`,
  `emulator`, `scrcpy`. No Android Studio open day-to-day.
- **Interact with a running emulator like a web agent uses a browser**
  install APKs, launch the app, tap, swipe, screenshot, toggle nav modes,
  read `dumpsys`.
- **Recover from common toolchain failures** recognize the cryptic
  "No matching variant ... compatible with Java 8" wall as `JAVA_HOME`-not-set
  in disguise, kill stale Gradle daemons, fix and retry.

**iOS:**
- **Drive the iOS toolchain via CLI** — `xcodebuild`, `xcrun simctl`,
  `fastlane`, `swiftgen`, `agvtool`. No Xcode open day-to-day.
- **Interact with the Simulator like a web agent uses a browser** — install
  apps, launch, screenshot, deep link, push notifications, toggle appearance.
- **Distribute builds through Fastlane** — Firebase App Distribution for QA,
  TestFlight for broader testing, App Store Connect for production.

**Both platforms:**
- **Onboard a new developer** to an existing configured project (~60 min
  walkthrough including credential acquisition + smoke build).
- **Bootstrap a brand-new project from zero** Firebase, distribution
  channels, signing, Gradle plugins (Android) or Fastlane lanes (iOS),
  safety guards on production publishes.
- **Present a 3-option menu on every release request** let the user pick
  whether the agent runs the release, gives them the command to run, or
  walks them step-by-step through the Console UI.

## How to use these in your project

1. **Copy the relevant subfolder** (`Android/` or `iOS/`) into your project's
   `.cursor/rules/` directory:
   ```bash
   mkdir -p /path/to/your/project/.cursor/rules
   cp Android/*.mdc /path/to/your/project/.cursor/rules/
   ```
2. **Adapt the placeholder values** to your project see `Android/ADAPTING.md`
   for the find-and-replace checklist.
3. **Open Cursor in your project** and verify the rule loaded:
   > What do you know about this project?

   The agent should recite back the env vars, package id(s), and Gradle
   tasks from the main rule.

## Anatomy of the three-tier rule pattern

| Tier | File | Loads | What it does |
|---|---|---|---|
| **Always-on conventions** | `*-project.mdc` | Every chat | Codifies env vars, codebase orientation, on-device interaction vocabulary, release-three-options behavior, common gotchas. |
| **On-demand: onboarding** | `*-project-onboarding.mdc` | When user asks to set up an existing project | Walks through installing toolchain, env vars, credential acquisition, smoke build. |
| **On-demand: bootstrap** | `*-project-bootstrap.mdc` | When user asks to set up a brand-new project | Walks through Firebase + Play Console + plugin wiring + safety guards from zero. |

This pattern is portable across mobile platforms (Android, iOS, React Native,
Flutter) because the *shape* of the work is the same   only the toolchain
names change.

## Provenance

Built and shipped as part of the **"Mobile development, without a mobile IDE"**
talk by Jose David Bayona at LaunchPad Lab / SPACE. The companion docs in the
`mdrtacademy_android` repo explain the talk's three pillars:

1. Your IDE doesn't matter. The CLI does.
2. The agent drives the simulator like a web agent drives the browser.
3. One afternoon of setup, then every future delivery is one prompt.

These rules are the embodiment of pillar #3 the one-time setup made durable
and shareable.

## License

TBD — license to be decided before public release. Until then, treat as
**all rights reserved**. MIT / Apache-2.0 / CC0 are the most likely
candidates for the final license.
