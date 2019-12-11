#!/bin/bash
if [ $# -eq 0 ]; then
echo "[FAIL] No arguments supplied"
else
clear
python3 editor.py $1;
fi
