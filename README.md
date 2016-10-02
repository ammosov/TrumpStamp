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
export ANDROIDAPI="21"  # Target API version, better use v.21 because it failed in my case with ANDROIDAPI > 21
export ANDROIDNDKVER="r12b"  # Version of NDK you installed
```
* Add path to $ANDROIDSDK/tools and $ANDROIDSDK/platform-tools to your $PATH
* Run `./build_android_debug.sh APK_VERSION` in project directory to build debug apk and place it into build/android
* RUN `./build_android_release.sh APK_VERSION KEYSTORE KEYNAME STOREPASS KEYPASS` to build and sign release apk and put it into build/android

## How to build Xcode project

* Install Xcode
* Run `./build_xcode_project.sh` in project directory
