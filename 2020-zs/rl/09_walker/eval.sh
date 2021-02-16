#/bin/bash

rm -rf score

for i in $(seq $2)
do
    python walker.py --recodex --no-render --hardcore --load_from=$1 --seed=$i | tail -n1 | cut -d' ' -f7 >> score
done
