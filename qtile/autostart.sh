#!/bin/bash

#~/.local/bin/3-monitors.sh &
# wal -R &
/usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1 &
nitrogen --restore &
compton --config ~/.config/compton/compton.conf &
xsetroot -cursor_name left_ptr
nm-applet &
