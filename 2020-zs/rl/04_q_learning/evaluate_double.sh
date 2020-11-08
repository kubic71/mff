#!/bin/bash


evalFor=100
seeds=12

rm -f /tmp/$1

echo "Evaluating $1"
for i in $(seq $seeds)
do
#     echo $i
    python lunar_lander_double.py --render_each 1000000 --episodes=0 --load_from="$1" --evaluate_for $evalFor --seed $i | tail -n1 | cut -d' ' -f7 >> /tmp/$1 &
    waitFor="$waitFor $!"
done

echo "Processes PIDs: $waitFor"
wait $waitFor

echo Evaluation $seeds x $evalFor
cat /tmp/$1 | awk '{ sum += $1; n++ } END { if (n > 0) print sum / n; }'


