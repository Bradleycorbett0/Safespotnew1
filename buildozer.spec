[app]

# App details
title = SafeSpot
package.name = safespot
package.domain = org.yourname.safespot
version = 1.0

# Source and file types
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Dependencies
requirements = python3,kivy

# Orientation and fullscreen
orientation = portrait
fullscreen = 0

# Permissions (add more if needed later)
android.permissions = INTERNET

# API and architectures
android.api = 33
android.minapi = 21
android.archs = armeabi-v7a, arm64-v8a

# Enable backup
android.allow_backup = True

# Release build format
android.release_artifact = aab

# Uncomment and set your icons later if needed
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/splash.png

# Set this to 1 if your app should stay awake
# android.wakelock = 1


[buildozer]

log_level = 2
warn_on_root = 1