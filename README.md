# Agentic Mobile Rules

A collection of Cursor rule files (`.mdc`) that turn the Cursor agent into a
productive mobile-dev teammate — without requiring Android Studio or Xcode
for day-to-day work.

These rules were built for and live-demonstrated in the talk
**"Mobile development, without a mobile IDE"**. The full talk runbook lives
in `mdrtacademy_android/MDRTAcademy/docs/agentic-showcase.md`; this folder
is the **portable, shareable artifact** of that talk — drop these rules into
any mobile project's `.cursor/rules/` directory and the agent picks up the
behaviors.

## What's in here

```
agentic-mobile-rules/
├── README.md                    ← you are here
├── Android/
│   ├── ADAPTING.md              ← find-and-replace guide for your project
│   ├── android-project.mdc              (alwaysApply: true — every-chat behavior)
│   ├── android-project-onboarding.mdc   (on-demand — joining an existing team)
│   ├── android-project-bootstrap.mdc    (on-demand — brand-new project from zero)
│   └── scripts/
│       └── agent-boot-emulator.py       (Python launcher for the AVD — solves agent-shell + snapshot issues)
└── iOS/
    ├── README.md                ← iOS-specific overview + comparison table
    ├── ADAPTING.md              ← find-and-replace guide for your project
    ├── ios-project.mdc                  (alwaysApply: true — every-chat behavior)
    ├── ios-project-onboarding.mdc       (on-demand — joining an existing team)
    └── ios-project-bootstrap.mdc        (on-demand — brand-new project from zero)
```

## What these rules teach the agent to do

**Android:**
- **Drive the Android toolchain via CLI** — Gradle, `adb`, `sdkmanager`,
  `emulator`, `scrcpy`. No Android Studio open day-to-day.
- **Interact with a running emulator like a web agent uses a browser** —
  install APKs, launch the app, tap, swipe, screenshot, toggle nav modes,
  read `dumpsys`.
- **Recover from common toolchain failures** — recognize the cryptic
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
- **Bootstrap a brand-new project from zero** — Firebase, distribution
  channels, signing, Gradle plugins (Android) or Fastlane lanes (iOS),
  safety guards on production publishes.
- **Present a 3-option menu on every release request** — let the user pick
  whether the agent runs the release, gives them the command to run, or
  walks them step-by-step through the Console UI.

## How to use these in your project

1. **Copy the relevant subfolder** (`Android/` or `iOS/`) into your project's
   `.cursor/rules/` directory:
   ```bash
   mkdir -p /path/to/your/project/.cursor/rules
   cp Android/*.mdc /path/to/your/project/.cursor/rules/
   ```
2. **Adapt the placeholder values** to your project — see `Android/ADAPTING.md`
   for the find-and-replace checklist.
3. **Open Cursor in your project** and verify the rule loaded:
   > What do you know about this project?

   The agent should recite back the env vars, package id(s), and Gradle
   tasks from the main rule.

## Here is how to onboard your project

Once the rules are in your project, the onboarding rule does the rest.
Open Cursor and tell the agent something like:

> I'm setting up this repo for CLI development.

The agent picks up `android-project-onboarding.mdc` (or the iOS equivalent)
and walks you through it step by step:

1. Confirms your OS, shell, admin access, and that the repo is cloned.
2. Audits what's already installed — routes to install steps only for what's missing.
3. Sets shell env vars (`JAVA_HOME`, `ANDROID_HOME`, `PATH`) in your rc file.
4. Walks you through acquiring credential files (team members ask the project
   owner; solo devs go through Firebase Console + Cloud Console + `keytool`).
5. Creates an AVD and boots it (Android) or boots a Simulator (iOS).
6. Runs a smoke build to verify the whole chain.
7. Smoke-tests the agent loop with a trivial prompt.

Total: ~60–90 minutes the first time, mostly waiting on SDK downloads.
After that, every future bug on this project is just a prompt.

If you are setting up a **brand-new project** (no Firebase or Play Console
yet), say so explicitly. The agent then picks up the bootstrap rule instead,
which adds Firebase project creation, Play Console signup, plugin wiring,
and a tested DRAFT-safety guard on top of the onboarding flow above.

## Anatomy of the three-tier rule pattern

| Tier | File | Loads | What it does |
|---|---|---|---|
| **Always-on conventions** | `*-project.mdc` | Every chat | Codifies env vars, codebase orientation, on-device interaction vocabulary, release-three-options behavior, common gotchas. |
| **On-demand: onboarding** | `*-project-onboarding.mdc` | When user asks to set up an existing project | Walks through installing toolchain, env vars, credential acquisition, smoke build. |
| **On-demand: bootstrap** | `*-project-bootstrap.mdc` | When user asks to set up a brand-new project | Walks through Firebase + Play Console + plugin wiring + safety guards from zero. |

This pattern is portable across mobile platforms (Android, iOS, React Native,
Flutter) because the *shape* of the work is the same — only the toolchain
names change.

## Provenance

Built and shipped as part of the **"Mobile development, without a mobile IDE"**
talk by Jose David Bayona at LaunchPad Lab / SPACE. The companion docs in the
`mdrtacademy_android` repo explain the talk's three pillars:

1. Your IDE doesn't matter. The CLI does.
2. The agent drives the simulator like a web agent drives the browser.
3. One afternoon of setup, then every future delivery is one prompt.

These rules are the embodiment of pillar #3 — the one-time setup made durable
and shareable.

## License

(Add your preferred license — MIT / Apache-2.0 / CC0 are common choices for
this kind of shareable agent-config artifact.)
