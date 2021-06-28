#!/usr/bin/env bash

tmux new -s 'writing-thesis' -d

tmux send-keys -t 'writing-thesis' 'vi related-work.tex' C-m
sleep .2

tmux new-window -t 'writing-thesis'
tmux send-keys -t 'writing-thesis' 'vi main.tex' C-m
sleep .2

tmux new-window -t 'writing-thesis'
tmux send-keys -t 'writing-thesis' 'vi references.bib' C-m
sleep .2

tmux new-window -t 'writing-thesis'
tmux send-keys -t 'writing-thesis' 'vi glossary.tex' C-m
sleep .2

tmux new-window -t 'writing-thesis'

tmux attach -t 'writing-thesis'

open main.pdf
