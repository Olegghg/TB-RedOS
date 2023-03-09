#!/bin/bash
sudo dnf install -y python3
sudo dnf install -y python3-pip
sudo pip3 install tk
sudo pip3 install pillow
sudo pip3 install pygubu

APP="$(pwd)/app.py"
ICON_NAME="pmtbredos"

echo "[Desktop Entry]
Type =Application
Terminal=true
Name=$ICON_NAME
Icon=images/desktop.png
Exec=$APP" > ~/Рабочий\ стол/$ICON_NAME.desktop

chmod +x ~/Рабочий\ стол/$ICON_NAME.desktop
echo "Приложение готово к работе :)"
