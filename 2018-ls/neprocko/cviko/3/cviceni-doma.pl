vypustvse(X, [], []).
vypustvse(X, [X | Xs], Zs) :-
    vypustvse(X, Xs, Zs).

vypustvse(X, [Y | Xs], Ys) :-
    X \= Y,
    vypustvse(X, Xs, Zs),
    append([Y], Zs, Ys).

