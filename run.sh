#!/bin/bash

SESSION=hmm-scaler
API_SERVER="python3 api-server/run.py"
COLLECTOR="python3 metric-collector/run.py"
DETECTOR="python3 scaling-detector/run.py"

tmux new-session -d -s $SESSION
tmux split-window -v -t $SESSION:0.0
tmux split-window -h -t $SESSION:0.1

tmux send-keys -t $SESSION:0.0 "$API_SERVER" C-m
sleep 1

tmux send-keys -t $SESSION:0.1 "$COLLECTOR"  C-m
tmux send-keys -t $SESSION:0.2 "$DETECTOR"   C-m

tmux attach-session -t $SESSION
