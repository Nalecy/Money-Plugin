#!/bin/bash

echo start collect

while [ 1 ]
do
    sleep 1
    python data_collect.py --origin "/Users/nalecyxu/Downloads/nft_origin" --target "/Users/nalecyxu/Downloads/nft_target"
done