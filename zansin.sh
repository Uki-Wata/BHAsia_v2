#!/bin/bash

# 色定義
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
RESET="\033[0m"

# ZANSIN を大きく表示する関数（色を引数で受け取るように変更）
print_zansin() {
    local color=$1
    echo -e "${color}"
    echo "███████╗  █████╗  ███╗   ██╗ ███████╗ ██╗ ███╗   ██╗██╗"
    echo "╚══███╔╝ ██╔══██╗ ████╗  ██║ ██╔════╝ ██║ ████╗  ██║██║"
    echo "  ███╔╝  ███████║ ██╔██╗ ██║ ███████╗ ██║ ██╔██╗ ██║██║"
    echo " ███╔╝   ██╔══██║ ██║╚██╗██║ ╚════██║ ██║ ██║╚██╗██║╚═╝"
    echo "███████╗ ██║  ██║ ██║ ╚████║ ███████║ ██║ ██║ ╚████║██╗"
    echo "╚══════╝ ╚═╝  ╚═╝ ╚═╝  ╚═══╝ ╚══════╝ ╚═╝ ╚═╝  ╚═══╝╚═╝"
    echo -e "${RESET}"
}

# 進捗表示関数
deploy_status() {
    local message=$1
    local color=$2
    echo -e "${color}${message}${RESET}"
}

# メイン処理
clear
print_zansin $CYAN
deploy_status "Deploying ZANSIN Control Server..." $YELLOW
sleep 2 # 進捗のシミュレーション

deploy_status "ZANSIN Control Server Deployed!" $GREEN
sleep 2 # 進捗のシミュレーション

deploy_status "Deploying Training Machine..." $YELLOW
sleep 2 # 進捗のシミュレーション

deploy_status "Training Machine Deployed!" $GREEN
sleep 2 # 最終状態を見せる
