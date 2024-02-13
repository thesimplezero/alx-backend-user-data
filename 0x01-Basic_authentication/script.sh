#!/bin/bash

# Function to recursively add files in a directory, excluding venv
function add_files_recursive() {
    local dir="$1"
    for file in "$dir"/*; do
        if [ -d "$file" ]; then
            if [ "${file##*/}" != "venv" ]; then
                add_files_recursive "$file"
            fi
        elif [ -f "$file" ]; then
            git add "$file"
            read -rp "Enter commit message for '$file': " commit_msg
            git commit -m "$commit_msg"
            ((count++))
        fi
    done
}

# Detect the git repository
repo=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$repo" ]; then
    echo "Error: Not inside a git repository."
    exit 1
fi

# Change directory to the repository
cd "$repo" || exit

# Add and commit files
count=0
add_files_recursive "$repo"

# Display total files committed
echo "Total files committed: $count"
