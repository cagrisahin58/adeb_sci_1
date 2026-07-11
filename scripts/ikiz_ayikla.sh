#!/bin/bash
# tmux revpipe'a bagli docker-exec'i bulup konteyner bash'iyle eslestirir,
# tmux'a bagli OLMAYAN (oksuz) pipeline bash + python'unu raporlar.
set -u
PANE=$(tmux list-panes -t revpipe -F '#{pane_pid}' 2>/dev/null)
echo "pane_pid=$PANE"
echo "--- pane cocuklari (docker exec bekleniyor):"
ps -o pid,lstart,cmd --ppid "$PANE" --no-headers 2>/dev/null | cut -c1-100
EXEC_PID=$(ps -o pid= --ppid "$PANE" 2>/dev/null | head -1 | tr -d ' ')
echo "exec_pid=$EXEC_PID"
if [ -n "${EXEC_PID:-}" ]; then
    echo "--- exec baslangic:"
    ps -o lstart= -p "$EXEC_PID"
fi
echo "--- konteyner pipeline bashleri:"
docker exec adeb_eval ps -o pid,lstart,cmd --no-headers -C bash 2>/dev/null | grep revision | cut -c1-100
