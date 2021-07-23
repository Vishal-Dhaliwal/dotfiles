# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401
import subprocess
import os
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal(preference="alacritty")

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="toggle between floating mode and tiling mode"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "w", lazy.spawn("google-chrome"), desc="Spawn browser"),
    Key([mod], "f", lazy.spawn("nemo"), desc="Spawn file-manager"),
    Key([mod, "shift"], "v", lazy.spawn(terminal + "-e pulsemixer"), desc="Spawn volume"),
    Key([mod], "p", lazy.spawn("dmenu_run -p 'run: ' -fn 'Sans-9'"), desc="Spawn dmenud"),
    Key(["mod1", "control"], "Down", lazy.spawn("xbacklight -dec 10"), desc="Decrease brightness"),
    Key(["mod1", "control"], "Up", lazy.spawn("xbacklight -inc 10"), desc="Increase Brightness")
]

colors = [
    ["#1c1c1c", "#1c1c1c"],  # color 0
    ["#373b41", "#373b41"],  # color 1
    ["#c5c8c6", "#c5c8c6"],  # color 2
    ["#a54242", "#a54242"],  # color 3
    ["#5f819d", "#5f819d"],  # color 4
    ["#373b41", "#373b41"],  # color 5
    ["#b294bb", "#b294bb"],  # color 6
    ["#81a2be", "#81a2be"],  # color 7
    ["#e2c5dc", "#e2c5dc"],  # color 8
    ["#5e8d87", "#5e8d87"]   # color 9
]

# colors = []
# cache='/home/vishal/.cache/wal/colors'
# def load_colors(cache):
#     with open(cache, 'r') as file:
#         for i in range(8):
#             colors.append(file.readline().strip())
#     colors.append('#ffffff')
#     lazy.reload()
# load_colors(cache)

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
])

layouts = [
    layout.MonadTall(border_width=2, border_focus='#ef8d25', margin=8, ratio=0.55, new_client_position='top'),
    layout.Floating(border_focus=colors[2])
]

widget_defaults = dict(
    font='Sans',
    fontsize=13,
    padding=3,
)
extension_defaults = widget_defaults.copy()
widgets_list = [
    widget.GroupBox(borderwidth=4, active=colors[4], inactive=colors[2], rounded=False, highlight_color=colors[2], highlight_method="line", this_current_screen_border=colors[7], block_highlight_text_color=colors[0], hide_unused=True),
    widget.Chord(chords_colors={'launch': ("#ff0000", "#ffffff"),}, name_transform=lambda name: name.upper(),),
    widget.WindowName(),
    widget.Spacer(),
    widget.CurrentLayout(foreground=colors[3]),
    widget.Sep(linewidth = 2),
    widget.Net(format='{down}↓↑{up}', interface=['wlp13s0'], foreground=colors[4]),
    widget.Sep(padding=8,linewidth=2,),
    widget.Clock(foreground=colors[2], format='%d %b, %A',),
    widget.Sep(padding=6,linewidth=2,),
    widget.Clock(foreground=colors[6],format='%I:%M %p'),
    widget.Sep(padding=6, linewidth=2,),
    widget.Battery(discharge_char='', charge_char='', format='{char} {percent:2.0%}', foreground=colors[7]),
    widget.Sep(padding=6, linewidth=2,),
    widget.Systray(icons_size=18,),
    widget.Sep(padding=6, linewidth=0,)
]

screens = [Screen(top=bar.Bar(widgets_list, 17, opacity=1))]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    # Match(wm_class='Gpick')   # Gpick color picker
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~/')
    subprocess.call([home + '/.config/qtile/autostart.sh'])