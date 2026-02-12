#!/bin/bash

# Lab 3 Script 1: Analyze Moby Dick
# This script searches for a word in Moby Dick and counts occurrences

SEARCH_PATTERN="$1"
OUTPUT="$2"

# Download Moby Dick
curl -o mobydick.txt "https://gist.githubusercontent.com/StevenClontz/4445774/raw/1722a289b665d940495645a5eaaad4da8e3ad4c7/mobydick.txt"

# Search for the pattern and count occurrences
OCCURRENCES=$(grep -o "$SEARCH_PATTERN" mobydick.txt | wc -l)

# Write results to output file
echo "The search pattern \`$SEARCH_PATTERN\` was found \`$OCCURRENCES\` time(s)." > "$OUTPUT"
