
zretez([], Ys, Ys).
zretez([X | Xs], Ys, [X | Zs]) :- zretez(Xs, Ys, Zs). 

prefix(Xs, Ys) :- zretez(Xs, _, Ys).  

get_trans(Perm, X, Y) :- append(_, [[X, Y] | _], Perm).

perm([], []).

perm([X | Xs], Zs) :-
    append(Ys1, Ys2, Ys),
    append(Ys1, [X | Ys2], Zs),
    perm(Xs, Ys).