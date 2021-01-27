#!/bin/bash
function isVersionAtHead() {
	if [ -z "$TAG" ]
	then
		echo "TAG must be non-empty at HEAD"
		return 1
	fi
	return 0
}

REPOSITORY="gcr.io/staging-kawa/sample-decoder-image"
MASTER_BRANCH="master"
TAG=`git tag --points-at`
BRANCH=`git branch --show-current`
IMAGE="${REPOSITORY}:${TAG}"
if [ "$BRANCH" != "$MASTER_BRANCH" ]
then
	echo "Branch is not Master"
	exit 1
fi

echo "=== Branch is Master"
if git diff-index --quiet HEAD --; then
    isVersionAtHead

    if [ $? -ne 0 ]
    then
	exit 1
    fi

    echo "=== building image ${IMAGE}"

    docker build . -t "${IMAGE}"

    echo "=== pushing image ${IMAGE}"

    docker push "${IMAGE}"

    if [ $? -ne 0 ]
    then
        echo "Failed to Push Image ${IMAGE}"
        exit 1
    fi
    
    echo "Successfully Pushed Image ${IMAGE}"
    exit 0
else
    # Changes
    echo "Uncommitted changes in Master"
    exit 1
fi

