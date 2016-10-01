#! /bin/bash

p4a apk --private $PWD/Game --orientation landscape --icon $PWD/Game/assets/icon.png \
        --package=org.trumpstamp.trumpstamp --name "TrumpStamp" \
        --version $1 --bootstrap=sdl2 --requirements=python2,kivy --arch=armeabi-v7a,x86
