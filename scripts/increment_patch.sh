#!/bin/bash

# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

if ! git diff-index --quiet HEAD --; then
    echo "There are uncommitted changes in the working directory"
    exit 1
fi

latest_tag=$(scripts/get-latest-tag.sh)
if [[ $latest_tag =~ ^v([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
    major=${BASH_REMATCH[1]}
    minor=${BASH_REMATCH[2]}
    patch=${BASH_REMATCH[3]}
    new_tag="v$major.$minor.$((patch + 1))"
    ./scripts/update_version.sh "${new_tag}"
    echo "Creating new tag $new_tag"
    git tag $new_tag
    git push origin $new_tag
else
    echo "Latest tag is not in the expected format: $latest_tag"
    exit 1
fi
