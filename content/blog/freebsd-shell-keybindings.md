Title: Fixing a FreeBSD annoyance: shell editing keybindings
Slug: freebsd-shell-keybindings
Date: 2008-02-04 13:28
Status: published
Category: FreeBSD

Unlike all the other systems I use, FreeBSD is lacking in one tiny little area: default shell keybindings. Specifically, there's no keybindings associated with the arrow keys when _CTRL_ is held down.

I'm used to being able to move back a word with _CTRL+LeftArrow_ is pressed, being able to move forward a word with _CTRL+RightArrow_, being able to move to the start of the line with _CTRL+UpArrow_, and being able to move to the start of the line with _CTRL+DownArrow_, but none of the shells are configured with these bindings by default. There _are_ bindings for the particular functions though, just not these particular ones.

This is a bit of an annoyance, but it's only recently that I've became sufficiently annoyed to fix it. Here's my _zsh_ bindings, which also work with _tcsh_:

```sh
bindkey '\e[1;5D' backward-word
bindkey '\e[1;5C' forward-word
bindkey '\e[1;5A' beginning-of-line
bindkey '\e[1;5B' end-of-line
```

Here's the _bash_ bindings:

```sh
bind '"\e[1;5D": backward-word'
bind '"\e[1;5C": forward-word'
bind '"\e[1;5A": beginning-of-line'
bind '"\e[1;5B": end-of-line'
```

And finally, the FreeBSD _sh_ bindings:

```sh
bind "^[[1;5D" ed-prev-word
bind "^[[1;5C" ed-next-word
bind "^[[1;5A" ed-move-to-beg
bind "^[[1;5B" ed-move-to-end
```

There, fixed.
