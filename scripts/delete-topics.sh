#!/bin/bash

# Script used to delete topics formerly created
function deleteTopics(){
	for topic_arn in "$@"
	do
		aws sns delete-topic --topic-arn $topic_arn
	done
}

deleteTopics "$@"


