#!/bin/bash
# tmux Training Helper Script
#
# Creates and manages tmux sessions for long-running training jobs.
#
# Usage:
#     ./scripts/tmux_train.sh start vit_native    # Start training in tmux
#     ./scripts/tmux_train.sh attach vit_native   # Attach to session
#     ./scripts/tmux_train.sh status              # Show all sessions
#     ./scripts/tmux_train.sh stop vit_native     # Stop training

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_usage() {
    echo "Usage: $0 <command> [session_name]"
    echo ""
    echo "Commands:"
    echo "  start <name>    Start training in new tmux session"
    echo "  attach <name>   Attach to existing session"
    echo "  status          Show all training sessions"
    echo "  stop <name>     Stop training session"
    echo "  gpu             Check GPU status"
    echo ""
    echo "Examples:"
    echo "  $0 start vit_native"
    echo "  $0 attach vit_native"
    echo "  $0 status"
}

check_gpu() {
    echo -e "${GREEN}GPU Status:${NC}"
    nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader
}

start_training() {
    local session_name=$1

    if [ -z "$session_name" ]; then
        echo -e "${RED}Error: Session name required${NC}"
        print_usage
        exit 1
    fi

    # Check if session already exists
    if tmux has-session -t "$session_name" 2>/dev/null; then
        echo -e "${YELLOW}Session '$session_name' already exists.${NC}"
        echo "Use '$0 attach $session_name' to attach."
        exit 1
    fi

    # Check GPU availability
    echo -e "${GREEN}Checking GPU...${NC}"
    check_gpu

    # Determine config based on session name
    local config_file=""
    case "$session_name" in
        vit_native*)
            config_file="configs/experiments/cifar10_vit_native.yaml"
            ;;
        resnet*)
            config_file="configs/experiments/cifar10_resnet_adv.yaml"
            ;;
        trades*)
            config_file="configs/experiments/cifar10_trades.yaml"
            ;;
        *)
            config_file="configs/experiments/cifar10_vit_native.yaml"
            ;;
    esac

    echo -e "${GREEN}Creating tmux session: $session_name${NC}"
    echo "Config: $config_file"

    # Create new session
    tmux new-session -d -s "$session_name" -c "$PROJECT_ROOT"

    # Set up session
    tmux send-keys -t "$session_name" "cd $PROJECT_ROOT" Enter
    tmux send-keys -t "$session_name" "echo 'Starting training...'" Enter
    tmux send-keys -t "$session_name" "python scripts_new/train_robust.py --config $config_file --session $session_name --no-tmux" Enter

    echo -e "${GREEN}Training started in session '$session_name'${NC}"
    echo ""
    echo "To attach:  tmux attach -t $session_name"
    echo "To detach:  Ctrl+B, then D"
    echo "To stop:    $0 stop $session_name"
}

attach_session() {
    local session_name=$1

    if [ -z "$session_name" ]; then
        echo -e "${RED}Error: Session name required${NC}"
        print_usage
        exit 1
    fi

    if ! tmux has-session -t "$session_name" 2>/dev/null; then
        echo -e "${RED}Session '$session_name' does not exist.${NC}"
        echo "Available sessions:"
        tmux list-sessions 2>/dev/null || echo "  (none)"
        exit 1
    fi

    tmux attach -t "$session_name"
}

show_status() {
    echo -e "${GREEN}Active tmux sessions:${NC}"
    tmux list-sessions 2>/dev/null || echo "  (none)"
    echo ""
    check_gpu
}

stop_training() {
    local session_name=$1

    if [ -z "$session_name" ]; then
        echo -e "${RED}Error: Session name required${NC}"
        print_usage
        exit 1
    fi

    if ! tmux has-session -t "$session_name" 2>/dev/null; then
        echo -e "${YELLOW}Session '$session_name' does not exist.${NC}"
        exit 0
    fi

    echo -e "${YELLOW}Stopping session '$session_name'...${NC}"

    # Send Ctrl+C to gracefully stop training
    tmux send-keys -t "$session_name" C-c
    sleep 2

    # Kill the session
    tmux kill-session -t "$session_name"

    echo -e "${GREEN}Session '$session_name' stopped.${NC}"
}

# Main
case "$1" in
    start)
        start_training "$2"
        ;;
    attach)
        attach_session "$2"
        ;;
    status)
        show_status
        ;;
    stop)
        stop_training "$2"
        ;;
    gpu)
        check_gpu
        ;;
    *)
        print_usage
        exit 1
        ;;
esac
