#! /bin/bash

if [ ! -d kivy-ios ]; then
    git clone git://github.com/kivy/kivy-ios
fi
cd kivy-ios
./toolchain.py build kivy
./toolchain.py create TrumpStamp "$PWD/../Game"
open ./trumpstamp-ios/trumpstamp.xcodeproj
