kombinace(Xs, K, Ys) :- kombinace(Xs, K, [], Ys).

kombinace([], 0, Ys, Ys).

kombinace([H | Xs], K, Ak, Ys) :-
    K1 is K - 1,
    kombinace(Xs, K1, [H | Ak], Ys);
    kombinace(Xs, K, Ak, Ys).

 

kombinace2([], 0, []).
kombinace2([H | Xs], K, [H | Ys]) :- K1 is K - 1, kombinace2(Xs, K1, Ys).
kombinace2([_ | Xs], K, Ys) :- kombinace2(Xs, K, Ys).


kombinace3(_, 0, []).
kombinace3([H | Xs], K, [H | Ys]) :- K > 0, K1 is K - 1, kombinace2(Xs, K1, Ys).
kombinace3([_ | Xs], K, Ys) :- K > 0, kombinace2(Xs, K, Ys).

kombinace4(_, 0, []).
kombinace4(Xs, K, [H | Ys]) :-
    K > 0,
    K1 is K - 1,
    append(_, [H | Zs], Xs),
    kombinace4(Zs, K1, Ys).
