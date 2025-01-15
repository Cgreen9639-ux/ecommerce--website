#!/bin/bash

# Add changes to app.py and Dockerfile
git add app.py Dockerfile

# Commit the changes with a message
git commit -m "Update Flask app and Dockerfile to serve static files"

# Push the changes to the main branch
git push origin main
