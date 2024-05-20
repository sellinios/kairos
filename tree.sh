#!/bin/bash

# Generate a tree structure of the project, up to 10 levels deep, excluding node_modules, build, assets, and __pycache__ directories
clear
tree -L 10 -I 'node_modules|build|assets|__pycache__'

