#!/bin/bash

for f in *; do
    spleeter separate -p spleeter:5stems -o $f $f
done