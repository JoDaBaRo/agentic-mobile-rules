# Adapting these rules to your iOS project

These rules were written for the MDRT Academy iOS app and contain
project-specific values (bundle IDs, scheme names, team IDs, credential
paths, private dependency names). To use them in your own project, do a
global find-and-replace.

The fastest workflow:

1. Copy the three `.mdc` files to your project's `.cursor/rules/` directory.
2. Open them in your editor.
3. Walk the table below top-to-bottom, find-and-replace each value.
4. Read through once to catch anything project-specific the table missed.
5. Open Cursor in your project and ask *"what do you know about this
   project?"* — the agent should recite back the schemes, bundle IDs, and
   fastlane lanes correctly. If anything is wrong, that's where the rule
   needs more adapting.

## Required find-and-replace (do these first)

| Find | Replace with | Notes |
|---|---|---|
| `com.mdrt.MDRTAcademy-QA` | `<your-qa-bundle-id>` | Delete row from environments table if no QA env |
| `com.mdrt.MDRTAcademy-PreProduction` | `<your-preprod-bundle-id>` | Delete row if no preprod |
| `com.mdrt.MDRTAcademy-Staging` | `<your-staging-bundle-id>` | Delete row if no staging |
| `com.mdrt.MDRTAcademy` (production) | `<your-production-bundle-id>` | Always exists |
| `MDRTAcademy/MDRTAcademy.xcodeproj` | `<your-project-path>/<YourApp>.xcodeproj` | The Xcode project path |
| `Release - QA` | `<your-qa-distribution-scheme>` | Or delete if not using per-env schemes |
| `Release - PreProd` | `<your-preprod-distribution-scheme>` | |
| `Release - Production` | `<your-production-scheme>` | |
| `QA - English` | `<your-debug-scheme>` | Whatever scheme you use for everyday development |
| `6DMKJU6X25` | `<your-apple-team-id>` | Find in Apple Developer portal under Membership |
| `jose.bayona@launchpadlab.com` | `<your-apple-id>` | The Apple ID with Developer Program access |
| `Million Dollar Round Table` | `<your-team-name>` | |
| `LPL-iOS` | `<your-firebase-test-group>` | Your Firebase App Distribution tester group |
| `EightBitVideo` | `<your-private-spm-dep>` | Delete the private-repo sections entirely if you have no private SPM deps |
| `iPhone 16` | `<your-preferred-simulator>` | Or leave as-is; any recent iPhone simulator works |

## Files you DON'T rename

These filenames are conventions enforced by Apple / Firebase tooling:

- `GoogleService-Info.plist` — Firebase config, **must** be this exact name in the Xcode project
- `Info.plist` — iOS app metadata, required by the system
- `Appfile` — Fastlane convention (must be at `fastlane/Appfile`)
- `Fastfile` — Fastlane convention (must be at `fastlane/Fastfile`)
- `Pluginfile` — Fastlane convention

## Adaptations that need real thinking (not just find-and-replace)

### `ios-project.mdc` → "Search Before You Write" section

Lists where networking, models, constants, and strings live in the MDRT
repo. Update to match your project's structure:

- Networking entry point (Alamofire service? URLSession wrapper? Moya?)
- Models directory
- Constants file
- Strings / localization mechanism (SwiftGen? manual .strings? String catalogs?)
- View Controllers / SwiftUI views directory structure

### `ios-project.mdc` → "Delivery pipeline guardrails" section

References MDRT-specific files (`config.yml` structure, `Appfile` lanes).
Update to match your Fastlane setup. If you use `fastlane match` instead of
manual cert/profile management, rewrite the signing-related guardrails.

### `ios-project.mdc` → "Common gotchas" → EightBitVideo bullet

This gotcha is specific to MDRT's private SPM dependency. Either:
- **Delete this bullet entirely** if you have no private SPM deps
- **Update** to reference your own private dependency and its cache path
- **Keep the pattern** but change the dependency name

### `ios-project.mdc` → "On-device interaction" section

The bundle IDs in the `simctl` commands are MDRT-specific. Update to your
bundle IDs. The command patterns themselves are universal.

### `ios-project.mdc` → "App environments and bundle IDs" table

Rewrite entirely to match your project's environments. Some projects have:
- Only `debug` + `release` (two rows)
- `dev` / `staging` / `production` (three rows)
- Full `qa` / `preprod` / `staging` / `production` (four rows)

### `ios-project-onboarding.mdc` → Step 4 (SPM + private repos)

If your project has no private SPM dependencies, delete this step entirely.
If it uses CocoaPods instead of SPM, replace with:
```bash
cd <project-root> && bundle install && bundle exec pod install
```
And change the entry point from `.xcodeproj` to `.xcworkspace`.

### `ios-project-onboarding.mdc` → Step 5 (Code signing)

If your team uses `fastlane match` (shared certs via git repo or Google
Cloud Storage), replace Steps 5a-5c with:
```bash
fastlane match development
fastlane match adhoc
fastlane match appstore
```
This is simpler but requires the match repo/bucket to be already configured.

### `ios-project-bootstrap.mdc` → mostly project-agnostic already

Uses `<your-...>` placeholders throughout. Should work for any new iOS
project with minimal adaptation. The main things to customize are the
Fastfile template (Step 6e) and the scheme names.

## Verification checklist

After adapting, open Cursor in your project and run these sanity-checks:

- [ ] **Conventions loaded:** *"What simulator should I use for testing?"* → agent names your preferred device
- [ ] **Codebase known:** *"Where does this project define its API client?"* → agent points at YOUR networking file, not MDRT's
- [ ] **Release behavior fires:** *"Ship a build to my testers."* → agent responds with the 3-option AskQuestion menu (NOT just runs the command)
- [ ] **Onboarding loads:** *"Help me set up this project for the first time."* → agent starts the step-by-step walkthrough
- [ ] **Bootstrap loads:** *"I want to wire Fastlane into a brand-new iOS app."* → agent loads the bootstrap rule and starts Step 0
- [ ] **Scheme awareness:** *"Build the app for QA."* → agent uses the correct scheme name from your environments table

## When to deviate from these rules

These rules encode opinions:

- CLI-first with Xcode only for Interface Builder / debugger / Instruments
- Fastlane as the distribution abstraction (vs. raw `xcodebuild export` + `altool`)
- 3-option menu on every release (always, never skip)
- TestFlight upload as human-gated (never auto-submit for review)
- `.cursor/rules/` as the durable agent-config layer

Most of these are defensible defaults. The most likely to vary by team:

- **3-option menu may feel paternalistic** for senior teams — soften by
  changing from "ALWAYS present" to "present when ambiguous."
- **Fastlane vs. Xcode Cloud** — if your team uses Xcode Cloud for CI/CD,
  the Fastlane sections don't apply. Replace with Xcode Cloud workflow
  references and the agent's role becomes "trigger a workflow" rather than
  "run a lane."
- **CocoaPods vs. SPM** — if you use CocoaPods, add `bundle exec pod install`
  to the build-verification section and change the entry point to `.xcworkspace`.
- **fastlane match vs. manual certs** — match is more team-friendly but
  requires its own setup. If you use match, simplify the signing sections.

Edit freely. The rules are a starting point, not a contract.
