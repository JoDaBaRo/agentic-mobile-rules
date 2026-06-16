# Adapting these rules to your Android project

These rules were written for the MDRT Academy Android app and contain
project-specific values (package ids, file paths, line numbers, credential
filenames, backend URLs). To use them in your own project, do a global
find-and-replace.

The fastest workflow:

1. Copy the three `.mdc` files to your project's `.cursor/rules/` directory.
2. Open them in your editor.
3. Walk the table below top-to-bottom, find-and-replace each value.
4. Read through once to catch anything project-specific the table missed.
5. Open Cursor in your project and ask *"what do you know about this
   project?"* — the agent should recite back the env vars, package id, and
   tasks correctly. If anything is wrong, that's where the rule needs more
   adapting.

## Required find-and-replace (do these first)

| Find | Replace with | Notes |
|---|---|---|
| `com.mdrt.mdrtacademy.qa` | `<your-app-qa-package-id>` | If you don't have flavors, replace with your single package id |
| `com.mdrt.mdrtacademy.preproduction` | `<your-app-preprod-package-id>` | Delete the row in the flavors table if no preprod |
| `com.mdrt.mdrtacademy.staging` | `<your-app-staging-package-id>` | Delete row if no staging |
| `com.mdrt.mdrtacademy` (production) | `<your-app-production-package-id>` | Always exists |
| `MDRTAcademy/` | `<your-module-dir>/` | Often just `app/` for simpler projects |
| `mdrtacademy-qa-1db5bc700e4e.json` | `<your-play-publisher>.json` | Your Google Play API service account JSON filename |
| `keystores/mdrtacadedmy-release` | `keystores/<your-release-keystore>` | Or wherever your release keystore lives |
| `LPL+MDRT` | `<your-tester-group-alias>` | Your Firebase App Distribution tester group |
| `qa.mdrtacademy.org` / `preproduction.mdrtacademy.org` / `stg.mdrtacademy.org` / `mdrtacademy.org` | `<your-backend-urls>` | Per-flavor backend URLs (only appears in commentary, not enforced) |
| `MDRTAcademy/scripts/agent-boot-emulator.py` | `<your-module>/scripts/agent-boot-emulator.py` | Path to the emulator launcher script — see "The boot launcher" section below |
| `Medium_Phone_API_36` | `<your-AVD-name>` | Your AVD name. The launcher defaults to this; pass yours as `python3 scripts/agent-boot-emulator.py YourAvdName` to override |
| `Medium_Phone.avd` | `<your-AVD-data-dir>` | The AVD's *data directory* under `~/.android/avd/` (frequently differs from the AVD name — check with `ls ~/.android/avd/`) |

## Files you DON'T rename

These filenames are conventions enforced by Firebase / Google tooling — keep
them as-is:

- `firebase-service-account.json` — Firebase Admin SDK key, name is conventional but flexible
- `google-services.json` — Firebase config, **must** be exactly this name + at `app/google-services.json`
- `keystore.properties` — Gradle convention

## The boot launcher (`scripts/agent-boot-emulator.py`)

A Python launcher that reliably boots the AVD from inside an agent shell. It
solves two real failure modes documented in its own header:

1. **Process-group teardown** — `nohup emulator -avd ... &` from an agent
   shell gets killed when the spawning shell returns. The launcher
   double-forks + calls `os.setsid()` to fully detach.
2. **Corrupt Quick Boot snapshots** — a stale `default_boot` snapshot can
   crash qemu on GPU restore. The launcher always passes `-no-snapshot-load`.

It also uses software GPU (`-gpu swiftshader_indirect`) for headless
reliability and a larger `-partition-size` to avoid `INSTALL_FAILED_INSUFFICIENT_STORAGE`
on large APK installs.

### How to install in your project

```bash
mkdir -p <your-module>/scripts
cp /path/to/agentic-mobile-rules/Android/scripts/agent-boot-emulator.py <your-module>/scripts/
chmod +x <your-module>/scripts/agent-boot-emulator.py
```

Then either pass your AVD as an arg, or edit line 31 of the script to change
the default from `Medium_Phone_API_36` to your AVD name. Same applies for the
JDK path on line 43 if you're not using Android Studio's bundled JBR.

### Recommended companion AVD config

For belt-and-suspenders cold-booting (so even a non-launcher invocation is
safe), add this line to `~/.android/avd/<your-AVD>.avd/config.ini`:

```
fastboot.forceColdBoot = yes
```

This makes the AVD ignore the Quick Boot snapshot regardless of how it's
launched. Pairs well with the launcher's `-no-snapshot-load` flag.

### When to update the rule's path references

After installing, update the path in your project's copy of
`android-project.mdc` (search for `MDRTAcademy/scripts/agent-boot-emulator.py`
and replace with your actual path — likely `app/scripts/agent-boot-emulator.py`
or just `scripts/agent-boot-emulator.py`). Same for
`android-project-onboarding.mdc`'s Step 5 callout.

## Adaptations that need real thinking (not just find-and-replace)

These sections of the rules reference codebase specifics that may not exist
in your project. Read and adapt:

### `android-project.mdc` → "Codebase orientation" section

Lists where networking, models, constants, and strings live in the MDRT
repo. Update to match your project's structure:

- Networking entry point (Retrofit service, Ktor client, etc.)
- Models directory
- Constants / build-config field declarations
- Strings file(s)
- BaseActivity / base ViewModel / app-wide extension points

### `android-project.mdc` → "Delivery pipeline guardrails" section

References line numbers in `app/build.gradle` (e.g. "lines 211–220 of
`app/build.gradle`" for the `releaseStatus.DRAFT` block). Re-find the
equivalent lines in your build.gradle and update the line numbers, OR remove
the line-number references and just describe the block.

### `android-project.mdc` → "Common gotchas" → edge-to-edge bullet

The last gotcha mentions `BaseActivity.kt`'s `shouldApplyDefaultSystemBarInsets()`,
`statusBarBleedColor()`, `navigationBarBleedColor()`, `onSystemBarInsetsChanged()`
hooks. These are specific to the MDRT codebase's edge-to-edge handling.
Either:

- **Delete this bullet entirely** if your project doesn't have similar hooks
- **Update** to point at your project's equivalent extension points
- **Keep as inspiration** if you want to add similar hooks to your project

### `android-project.mdc` → "Release request behavior" Gradle one-liners

The Firebase + Play Console Gradle task names assume specific flavor names
(`assembleQaRelease`, `appDistributionUploadQaRelease`,
`publishProductionReleaseBundle`). Update to your flavor names:

- `:app:assemble<YourFlavor>Release` instead of `:app:assembleQaRelease`
- `:app:appDistributionUpload<YourFlavor>Release` etc.

### `android-project-onboarding.mdc` → Step 4 (Credential files)

The table of credential files references MDRT-specific names. Update to
match your project (this is largely covered by the find-and-replace above,
but verify the table is accurate end-to-end).

### `android-project-bootstrap.mdc` → mostly project-agnostic already

This one is intentionally generic — uses `<your-app>` and `<your-app-name>`
placeholders. Should work for any new Android project with minimal
adaptation.

## Verification checklist

After adapting, open Cursor in your project and run through these
sanity-checks:

- [ ] **Conventions loaded:** *"What env vars do I need to set?"* → agent recites JAVA_HOME / ANDROID_HOME / PATH
- [ ] **Codebase known:** *"Where does this project define its API client?"* → agent points at your networking file, not MDRT's
- [ ] **Release behavior fires:** *"Ship a build to my testers."* → agent responds with the 3-option menu (NOT just runs the command)
- [ ] **Onboarding loads:** *"Help me set up this project for the first time."* → agent loads the onboarding rule and starts Step 0
- [ ] **Bootstrap loads:** *"I want to wire Firebase into a brand-new Android app."* → agent loads the bootstrap rule and starts Step 0
- [ ] **Boot launcher works:** `python3 <your-module>/scripts/agent-boot-emulator.py` → after `adb wait-for-device` returns and `sys.boot_completed = 1`, your AVD is up. If the window appears for ~1s then vanishes, the launcher's process-group fix isn't kicking in — verify the script's `os.setsid()` call ran by checking `/tmp/agent-emulator.log` exists and has emulator startup output.

If any of those don't fire correctly, the `description` field on the
relevant rule needs adjustment to match the phrasing your agent (and your
team) actually use.

## When to deviate from these rules

These rules encode opinions:

- Hybrid Cursor + Android Studio (open AS only for debugger / Profiler) — vs. pure Cursor or pure AS
- Pre-build APKs for some demos, live-build for delivery demos
- `releaseStatus.DRAFT` as a human-gated safety guard on production publishes
- 3-option menu on releases (always, never skip)
- `.cursor/rules/` as the durable agent-config layer

Most of these are defensible defaults. The most likely to vary by team:

- **3-option menu may feel paternalistic** for senior teams that just want
  the agent to ship — soften by changing the rule from "ALWAYS present the
  menu" to "present the menu when the request is ambiguous."
- **DRAFT guard** is non-negotiable for production publishing, but you might
  want a similar guard on Firebase preprod releases too if your preprod is
  user-facing.
- **Hybrid IDE stance** can be tightened to "pure CLI" for teams that don't
  use AS at all (delete the "When Android Studio GUI Is Unavoidable" section
  entirely).

Edit freely. The rules are a starting point, not a contract.
