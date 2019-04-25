get_max(nil, 0).

get_max(b(K, L, P), M) :-
    get_max(L, M1),
    get_max(P, M2),
    X is max(M1, M2),
    M is max(X, K).

zapis(nil, Val, nil).

zapis(b(K, L, P), Val, b(Val, L1, P2)) :-
    zapis(L, Val, L1),
    zapis(P, Val, P2).

trans(StromIn, StromOut) :-
    get_max(StromIn, M),
    zapis(StromIn, M, StromOut).


% trans(b(2, b(1, nil, nil), b(10, b(20, nil, nil), b(15, nil, nil))))