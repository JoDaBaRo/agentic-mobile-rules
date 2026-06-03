# iOS Agentic Rules

The iOS sibling rule set, following the same three-tier pattern as `../Android/`.

## Files

```
iOS/
├── README.md                        ← you are here
├── ADAPTING.md                      ← find-and-replace guide for your project
├── ios-project.mdc                  (alwaysApply: true — every-chat behavior)
├── ios-project-onboarding.mdc       (on-demand — joining an existing team)
└── ios-project-bootstrap.mdc        (on-demand — brand-new project from zero)
```

## What these rules teach the agent to do

- **Drive the iOS toolchain via CLI** — `xcodebuild`, `xcrun simctl`,
  `fastlane`, `swiftgen`, `agvtool`, `PlistBuddy`. No Xcode open day-to-day.
- **Interact with the Simulator like a web agent uses a browser** — install
  apps, launch, screenshot, deep link, push notifications, toggle appearance.
- **Distribute builds through Fastlane** — Firebase App Distribution for
  internal QA, TestFlight for broader testing, App Store Connect for
  production. One command per target.
- **Present a 3-option menu on every release request** — let the user pick
  whether the agent runs the release, gives them the command to run, or walks
  them step-by-step through the App Store Connect / Firebase Console UI.
- **Onboard a new developer** to an existing configured project (~60 min
  walkthrough: Xcode, signing certs, Fastlane, simulator, smoke build).
- **Bootstrap a brand-new project from zero** — Apple Developer enrollment,
  App IDs, certificates, provisioning profiles, Fastlane setup, Firebase
  App Distribution, TestFlight first-build review dance.

## How the three tiers map

| Tier | File | Loads | What it does |
|---|---|---|---|
| **Always-on conventions** | `ios-project.mdc` | Every chat | CLI-first mandate, scheme/bundle-ID reference, on-simulator interaction vocabulary, release-three-options behavior, delivery guardrails, common gotchas. |
| **On-demand: onboarding** | `ios-project-onboarding.mdc` | When user asks to set up an existing project | Walks through Xcode install, SPM deps, code signing, Fastlane config verification, smoke build. |
| **On-demand: bootstrap** | `ios-project-bootstrap.mdc` | When user asks to set up a brand-new project | Apple Developer enrollment → App IDs → certs → profiles → Firebase → Fastlane → App Store Connect → TestFlight first upload. |

## iOS vs. Android — key structural differences

| Concern | Android approach | iOS approach |
|---|---|---|
| Build system | Gradle (build + distribute in one) | `xcodebuild` (build only) + Fastlane (distribute) |
| Code signing | Single keystore + properties file | Certificate + provisioning profile + Apple team |
| Internal QA | Gradle `appDistributionUpload*` task | `fastlane ios qa` (wraps Firebase plugin) |
| Production release | Gradle `publishProductionReleaseBundle` | `fastlane ios appstore` (wraps TestFlight upload) |
| Safety guard | `releaseStatus.DRAFT` in Gradle config | `skip_waiting_for_build_processing: true` (human submits for review) |
| Env vars needed | `JAVA_HOME`, `ANDROID_HOME`, `PATH` | None (Xcode bundles everything; just `xcode-select`) |
| IDE dependency | None for CLI builds | Xcode must be installed (provides SDK + simulator runtimes) |
| Annual cost | $25 one-time (Play Console) | $99/year (Apple Developer Program) |

## Quick start

```bash
mkdir -p /path/to/your/ios-project/.cursor/rules
cp iOS/*.mdc /path/to/your/ios-project/.cursor/rules/
```

Then follow `ADAPTING.md` to replace MDRT-specific values with your own.
