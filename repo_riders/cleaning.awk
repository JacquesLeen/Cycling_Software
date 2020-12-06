#!/bin/sh

awk '{print $1,$2,$3,$4}' riders-raw.txt > temp.txt #prints only first four data entries
tr -d 0-9 < temp.txt >output.txt #removes numeric charachters
rm temp.txt
awk '{sub(/Stagista/, ""); print}' output.txt > temp.txt #removes the word stagista
rm output.txt
awk '{sub(/\|/, ""); print}' temp.txt > riders.txt #removes the | sign -> need to unlock its use
rm temp.txt

