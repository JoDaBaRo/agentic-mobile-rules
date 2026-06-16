#!/usr/bin/env python3
"""
Reliably boot the project AVD from inside an agent shell.

Why this exists (two failure modes a naive `emulator -avd ... &` hits):

1. Process-group teardown. Agent shell harnesses tear down the process group
   of a backgrounded command when the spawning shell returns, which kills the
   emulator a second or two after launch ("boots, then the window vanishes").
   macOS has no `setsid`, so we daemonize here with a double-fork + os.setsid()
   to fully detach the emulator into its own session.

2. Corrupt Quick Boot snapshot. A stale `default_boot` snapshot can fail GPU
   restore ("Failed to find ColorBuffer:0") and crash qemu right after the
   window appears. We always cold-boot (`-no-snapshot-load`) to sidestep it.
   The AVD is also configured with `fastboot.forceColdBoot = yes` so even a
   plain launch is safe.

Usage:
    python3 scripts/agent-boot-emulator.py [AVD_NAME]

Then wait for boot (env must have platform-tools on PATH):
    adb wait-for-device
    until [ "$(adb shell getprop sys.boot_completed | tr -d '\\r')" = "1" ]; do sleep 2; done

Log is written to /tmp/agent-emulator.log.
"""
import os
import sys

AVD = sys.argv[1] if len(sys.argv) > 1 else "Medium_Phone_API_36"
LOG = "/tmp/agent-emulator.log"

# Double-fork + setsid so the emulator survives the caller's shell teardown.
if os.fork() > 0:
    sys.exit(0)
os.setsid()
if os.fork() > 0:
    sys.exit(0)

home = os.path.expanduser("~")
sdk = os.environ.get("ANDROID_HOME", os.path.join(home, "Library/Android/sdk"))
os.environ.setdefault("JAVA_HOME", "/Applications/Android Studio.app/Contents/jbr/Contents/Home")
os.environ["ANDROID_HOME"] = sdk
os.environ["PATH"] = f"{sdk}/platform-tools:{sdk}/emulator:" + os.environ.get("PATH", "")

logfd = os.open(LOG, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
os.dup2(logfd, 1)
os.dup2(logfd, 2)
os.dup2(os.open("/dev/null", os.O_RDONLY), 0)

os.execv(f"{sdk}/emulator/emulator", [
    "emulator", "-avd", AVD,
    "-no-snapshot-load",          # always cold-boot; never restore a stale snapshot
    "-no-boot-anim",              # shave a few seconds off boot
    "-gpu", "swiftshader_indirect",  # software GPU: reliable in headless/agent contexts
    "-partition-size", "8192",    # headroom so large APK installs don't hit INSUFFICIENT_STORAGE
    "-dns-server", "8.8.8.8,8.8.4.4",
])
