#!/bin/bash

# The complete list of 15 games ordered from Easiest to Hardest
GAMES=("mspacman" "frostbite" "skiing" "gravitar" "montezumarevenge")

# Loop through each game and run the dreamer script
for GAME in "${GAMES[@]}"
do
    echo "=================================================="
    echo "Starting training for: $GAME"
    echo "=================================================="
    
    # Run the python script with the custom config
    python3 dreamer.py --env $GAME --config dreamer.yaml
    
    # THE FIX: Immediately rename the output folder to save the data securely!
    if [ -d "rl_experiments/dreamerv3" ]; then
        mv "rl_experiments/dreamerv3" "rl_experiments/dreamerv3_$GAME"
    fi
    
    echo "Finished training for $GAME. Results saved to rl_experiments/dreamerv3_$GAME!"
done

echo "All 15 games finished!"