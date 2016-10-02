#! /bin/bash

git clone git://github.com/kivy/kivy-ios
./kivy-ios/toolchain.py build kivy
./kivy-ios/toolchain.py create TrumpStamp "$PWD/Game"
open ./trumpstamp-ios/trumpstamp.xcodeproj
