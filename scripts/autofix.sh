#!/bin/bash

# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

find . -name "*.py" -not -path "./.*" | xargs autopep8 --in-place --aggressive --aggressive
find . -name "*.py" -not -path "./.*" | xargs isort
