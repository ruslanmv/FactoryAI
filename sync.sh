#!/bin/bash

# Ensure the script is run from the repository root
if [ ! -d .git ]; then
  echo "Error: This script must be run from the root of a Git repository."
  exit 1
fi

# Define the target directory for submodules
SUBMODULES_DIR="src"

# Create the src directory if it doesn't exist
mkdir -p "$SUBMODULES_DIR"

echo "Synchronizing all submodules into the $SUBMODULES_DIR folder..."

# Initialize and update submodules (if already present in the repository)
git submodule update --init --recursive

# Check the exit status
if [ $? -eq 0 ]; then
  echo "Submodules initialized and updated successfully."
else
  echo "Error occurred while initializing submodules."
  exit 1
fi

# Iterate through each submodule listed in .gitmodules
if [ -f .gitmodules ]; then
  echo "Processing each submodule..."

  while IFS= read -r line; do
    if [[ $line == "[submodule"* ]]; then
      # Start of a new submodule
      submodule_name=$(echo "$line" | sed 's/\[submodule "\([^"]*\)"\]/\1/')
      echo "Processing submodule: $submodule_name"
    elif [[ $line == *"url = "* ]]; then
      # Extract the submodule URL
      submodule_url=$(echo "$line" | sed 's/.*url = //')

      # Define the new submodule path inside the src folder
      submodule_path="$SUBMODULES_DIR/$submodule_name"

      # Check if the submodule directory exists
      if [ ! -d "$submodule_path" ]; then
        echo "Submodule directory does not exist. Cloning into $submodule_path..."
        git clone "$submodule_url" "$submodule_path"
      else
        echo "Submodule directory exists. Pulling latest changes into $submodule_path..."
        (cd "$submodule_path" && git fetch && git checkout $(git rev-parse @) && git pull)
      fi
    fi
  done < .gitmodules

  echo "All submodules synchronized into the $SUBMODULES_DIR folder."
else
  echo "No .gitmodules file found. Nothing to synchronize."
fi
