% soucet(+strom, -soucet, -strom_stejne_struktury_s_odkazem)
soucet(t(nil, V, nil), V, t(nil, Y, nil)) :- !.

soucet(t(L, V, P), Soucet, t(t(L1, Y, P1), Y, t1(L2, Y, P2))) :-
    soucet(L, SL, t(L1, Y, P1)),
    soucet(P, SP, t(L2, Y, P2)),
    Temp is SL + SP,
    Soucet is Temp + V.

soucet(Strom, t(OdkazL, Soucet, OdkazP)) :-
    soucet(Strom, Soucet, t(OdkazL, Soucet, OdkazP)).
    
% t(t(nil, 2, nil), 3, t(nil, 5, nil))

komb(_, 0, []).

komb([X|Xs], N, [X|Ys]) :-
    N > 0,
    N1 is N-1,
    komb(Xs, N1, Ys).

komb([_|Xs], N, Ys) :-
    N > 0,
    komb(Xs, N, Ys). 

kombset(Xs, N, Set) :-
    findall(K, komb(Xs, N, K), Set).


