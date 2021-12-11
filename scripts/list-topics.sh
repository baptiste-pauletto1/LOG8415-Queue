#!/bin/bash

aws sns list-topics --query 'Topics[*].TopicArn' --output text
