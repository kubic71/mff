%uloz(+Halda, +Prvek, -NovaHalda) :- ...

uloz(nil, P, t(nil, P, nil)).

uloz(t(L, X, P), Y, t(P , Y, L1)) :- Y =< X, uloz(L, X, L1).
uloz(t(L, X, P), Y, t(P , X, L1)) :- Y > X, uloz(L, Y, L1).