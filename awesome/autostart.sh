#!/bin/sh

compton --config ~/.config/awesome/compton.conf &
nitrogen --restore 
# xset r rate 300 50
nm-applet &