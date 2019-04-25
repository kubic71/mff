# Hubaty program na reseni minimalniho vrcholoveho pokryti
param N := 5;
set Vertices := (1..N);
set Edges := {(1,2),(1,3),(1,4),(2,4),(3,5),(2,5)};
var x{i in Vertices}, >= 0, <= 1, integer;
minimize obj: sum{i in Vertices} x[i];
condition_edge{(i,j) in Edges}: x[i] + x[j] >= 1;
solve;
printf "#OUTPUT:\n";
printf{i in Vertices} "Vrchol %d ma hodnotu %d\n", i, x[i];
printf "Vrchol 1 %s\n" , (if (x[1] = 1) then "byl pouzit" else "nebyl pouzit");
printf (if x[3] > 0 then "Vrchol %d byl pouzit\n" else ""), 3;
printf "#OUTPUT END\n";
end;
