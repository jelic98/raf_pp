#!/bin/bash

if [ $# -eq 0 ]; then
	echo "[FAIL] No arguments supplied"
else
	if [ $1 == "-e" ]; then
		clear
		python3 editor/editor.py $2;
	else
		python3 interpreter/main.py $1;
	fi
fi
