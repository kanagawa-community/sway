# Window hook for .github/scripts/capture-windows.sh: sway itself is the window: each theme
# is included with two terminals and a bar that uses the theme's variables, so
# focused and unfocused borders, the bar and the workspace buttons show. It is a
# whole desktop, so it gets no window frame.
# Requires: foot.
# shellcheck shell=bash
name=Sway
frame=none
size=1200x700

capture() {
  local theme="$root/themes/kanagawa-$1" bg fg term
  bg=$(sed -n 's/^set \$kanagawa_bg #\(.*\)/\1/p' "$theme")
  fg=$(sed -n 's/^set \$kanagawa_fg #\(.*\)/\1/p' "$theme")
  term="foot -o colors-dark.background=$bg -o colors-dark.foreground=$fg -o colors-light.background=$bg -o colors-light.foreground=$fg"
  start_sway "include $theme
default_border pixel 3
bar {
    position top
    font monospace 11
    status_command while echo kanagawa-$1; do sleep 60; done
    tray_output none
    colors {
        background \$kanagawa_bg_dark
        statusline \$kanagawa_fg
        focused_workspace  \$kanagawa_accent \$kanagawa_accent \$kanagawa_bg
        inactive_workspace \$kanagawa_bg_dark \$kanagawa_bg_dark \$kanagawa_fg_dim
        urgent_workspace   \$kanagawa_urgent \$kanagawa_urgent \$kanagawa_bg
    }
}
exec env LESS= LESSOPEN= $term less $root/README.md
exec sleep 0.5 && env LESS= LESSOPEN= $term less $theme"
  sleep 5
  WAYLAND_DISPLAY=$socket grim "$2"
  stop_display
}
