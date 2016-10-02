# TrumpStamp
Trump-Hillary card game

May 6 - project created

## How to build apk

* Install [python-for-android](https://python-for-android.readthedocs.io/en/latest/quickstart/#installation) and dependencies.
* Download [Android SDK](https://developer.android.com/studio/index.html) and [NDK](https://developer.android.com/ndk/downloads/index.html)
* Export all necessary environment variables:
```
export ANDROIDSDK="path_to_your_sdk"
export ANDROIDNDK="path_to_your_ndk"
export ANDROIDAPI="21"  # Target API version
export ANDROIDNDKVER="r12b"  # Version of NDK you installed
```
* Run `./build_apk.sh APK_VERSION` in project directory

## How to build Xcode project

* Install Xcode
* Clone [kivy-ios project](git clone git://github.com/kivy/kivy-ios)
* In `kivy-ios`  directory run `./toolchain.py build kivy`
* Run `./toolchain.py create TrumpStamp <path_to_trumpstamp_repo/Game>`
* Run `open trumpstamp-ios/trumpstamp.xcodeproj` - this will open Xcode project
