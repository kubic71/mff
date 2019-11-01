#!/bin/fish


for test_file in (ls -d $PWD/test_files/*)
	echo $test_file
	echo "dotnet run --project petr $test_file $test_file.petr $argv[1]" 
	dotnet run --project petr $test_file $test_file.petr $argv[1]
	dotnet run --project block_alignment $test_file $test_file.me $argv[1]
	diff $test_file.petr $test_file.me

end
