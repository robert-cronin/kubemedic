#!/bin/bash

# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

if ! git diff-index --quiet HEAD --; then
    echo "There are uncommitted changes in the working directory"
    exit 1
fi

# Updates version in Chart.yaml
update_version() {
    local new_version=$1

    if ! sed -i "s/appVersion: \".*\"/appVersion: \"$new_version\"/" chart/Chart.yaml; then
        echo "Error updating Chart.yaml"
        return 1
    fi

    git add chart/Chart.yaml chart/templates/deployment.yaml
    git commit -m "Bump version to $new_version"
    git push origin main
    echo "Chart version updated to $new_version"
}

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <new_version>"
    exit 1
fi

new_version=$1

update_version "$new_version"
