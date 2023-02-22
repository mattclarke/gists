#!/bin/sh
session="nicos"

tmux start-server
tmux new-session -d -s $session
tmux send-keys ". venv/bin/activate" C-m
tmux split-window -ht $session:0
tmux send-keys ". venv/bin/activate" C-m

tmux new-window -t $session:1 -n services
tmux send-keys ". venv/bin/activate" C-m
tmux split-window -t $session:1
tmux send-keys ". venv/bin/activate" C-m
tmux split-window -t $session:1
tmux send-keys ". venv/bin/activate" C-m
tmux split-window -t $session:1
tmux send-keys ". venv/bin/activate" C-m

tmux attach-session -t $session
