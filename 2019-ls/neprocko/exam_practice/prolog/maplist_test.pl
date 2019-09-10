je_delitelny(X, Y) :-
    0 is X mod Y.

vyfiltruj(L, NewL) :-
    findall(X, (member(X, L), je_delitelny(X, 3)), NewL).