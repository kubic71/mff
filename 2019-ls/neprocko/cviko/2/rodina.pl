

zretez([], Ys, Ys).
zretez([X | Xs], Ys, [X | Zs]) :- zretez(Xs, Ys, Zs). 

prefix(Xs, Ys) :- zretez(Xs, _, Ys).
