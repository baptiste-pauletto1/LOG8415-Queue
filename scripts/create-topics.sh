#!/bin/bash

# Script used to create FIFO topics for our SNS application 
for topic_name in "$@"
do
	aws sns create-topic --name $topic_name --attributes FifoTopic=true,ContentBasedDeduplication=true
done

