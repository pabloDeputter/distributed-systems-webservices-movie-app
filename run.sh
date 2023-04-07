#!/bin/bash

# Introduce DistributedSystemsProject
echo -e "Welcome to DistributedSystems Project, by Pablo Deputter."

# Check if virtual environment exists
if [ ! -d "api/venv" ]
then
  # Create virtual environment and activate it
  virtualenv api/venv
  source api/venv/bin/activate
  
  # Install required packages
  pip install -r api/requirements.txt
  cd frontend || exit
  npm install
  cd ..
else
    # Activate the environment and install required packages
    source api/venv/bin/activate
    pip install -r api/requirements.txt
    cd frontend || exit
    npm install
    cd ..
fi

# Prompt for dev or prod mode
read -p "Enter dev, prod or clean mode: " mode

if [ "$mode" = "dev" ]
then
  # Start development servers
  cd api || exit
  python manage.py dev &
  pid1=$!
  cd ../frontend || exit
  npm run dev -- --port 5177 &
  pid2=$!
  
  # Wait for Ctrl-C
  trap "kill $pid1 $pid2" SIGINT

  # Wait for both servers to finish
  wait $pid1 $pid2
elif [ "$mode" = "prod" ]
then
  # Start production servers
  cd api || exit
  python manage.py prod &
  pid1=$!
  cd ../frontend || exit
  npm run preview -- --port 5177 &
  pid2=$!
  
  # Wait for Ctrl-C
  trap "kill $pid1 $pid2" SIGINT

  # Wait for both servers to finish
  wait $pid1 $pid2
# Format code
elif [ "$mode" = "clean" ]
then
    cd frontend || exit
    npm run lint
    npm run format
else
  # Invalid mode
  echo "Invalid mode: $mode"
fi