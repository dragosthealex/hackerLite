#!/bin/bash
# Manually emulate ionic/cordova application
# Miroslav Masat 2014 

echo "Emulating..."
cd ./platforms/ios/build/emulator
var=$(pwd)

ios-sim launch "$var"/*.app