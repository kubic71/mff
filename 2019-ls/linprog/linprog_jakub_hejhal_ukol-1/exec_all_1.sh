#!/usr/bin/env bash

for file in vstupy/vstup1-*

# export linear programs to MathProg format
do
	base_name=$(basename $file)
	base_name=$(echo $base_name | sed 's/.txt/.mod/g')
	echo $base_name
	cat $file | python3 transform1.py > compiled/${base_name}
done

# execute glpsol

rm output/reseni1.txt 2> /dev/null

for file in compiled/vstup1-*
do
	base_name=$(basename $file)
	base_name=$(echo $base_name | sed 's/.mod/.txt/g')
	echo Executing $base_name

	{ time  glpsol -m $file > tmp ;} 2> time.txt
	time_taken=$(cat time.txt  | grep real | cut  -f2)
	min_val=$(cat tmp | grep "#OUTPUT: " | sed 's/#OUTPUT: //g')

	# if #OUTPUT: line wasn't found in glpsol output, that means program has no primal solution
	if [ -z "$min_val" ]; then
          min_val="--"
    fi

    echo -e "${base_name}\t${min_val}\t${time_taken}" >> output/reseni1.txt
done

# execute glpsol

    