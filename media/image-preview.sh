#!/bin/bash
# This script uses fd to find image files and fzf to preview them
fd -e png -e jpg --full-path . | fzf --preview 'fzf-preview.sh {}'