zena(z1).
zena(z2).
zena(z3).
zena(z4).
zena(z5).
zena(z6).


filter(L, Out):-
    filter(L, [], Out).
filter([], Ak, Ak).

filter([H | L], Ak, Out) :-
    zena(H),
    filter(L, [H | Ak], Out).

filter([H | L], Ak, Out) :-
    not(zena(H)),
    filter(L, Ak, Out).


sedi_pocty([], [_]).
sedi_pocty([_], []).
sedi_pocty([], []).

sedi_pocty([_ | Zs1], [_ | Zs2]) :- 
    sedi_pocty(Zs1, Zs2).

pul(S, L1, L2) :- 
    append(L1, L2, S),
    filter(L1, Z1),
    filter(L2, Z2),
    sedi_pocty(Z1, Z2).

