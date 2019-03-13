get_trans(Perm, X, Y) :-
    append(_, [[X, Y] | _], Perm).

find_cycle(Perm, X, Arc, Arc) :-
    member(X, Arc).

find_cycle(Perm, X, Arc, Cycle) :-
    not(member(X, Arc)),
    get_trans(Perm, X, Y),
    append([X], Arc, NewArc),
    find_cycle(Perm, Y, NewArc, Cycle).


remove_cycle_from_perm(Perm, [], Perm).

remove_cycle_from_perm(Perm, [X | Rest_of_cycle], NewPerm) :-
    append(Perm1, [[X | _] | Perm2], Perm),
    append(Perm1, Perm2, ShorterPerm),
    remove_cycle_from_perm(ShorterPerm, Rest_of_cycle, NewPerm).
    

find_all_cycles([], Cycles, Cycles).


find_all_cycles(Perm, CurrentCycles, Cycles) :- 
    append([[X, Y]], _, Perm),
    find_cycle(Perm, X, [], FoundCycle),
    remove_cycle_from_perm(Perm, FoundCycle, NewPerm),
    append([FoundCycle], CurrentCycles, NewCurrentCycles),
    find_all_cycles(NewPerm, NewCurrentCycles, Cycles).
    

perm2cyk(Perm, Cycles) :-
    find_all_cycles(Perm, [], Cycles).


% perm2cyk([[a,b], [b,c], [c,a], [d,d], [e,f], [f,e]], Cycles).






% -------------------------------------- %
% ----------- Bonusovy ukol ------------ %
% -------------------------------------- %

zena(z1).
zena(z2).
zena(z3).
zena(z4).
zena(z5).
zena(z6).


% filter out non-women
filter(L, Out):-
    filter(L, [], Out).
filter([], Ak, Ak).

filter([H | L], Ak, Out) :-
    zena(H),
    filter(L, [H | Ak], Out).

filter([H | L], Ak, Out) :-
    not(zena(H)),
    filter(L, Ak, Out).


sedi_pocty([], [], []).
sedi_pocty([_], [], []).
sedi_pocty([], [_], []).
sedi_pocty([], [], [_]).
sedi_pocty([_], [_], []).
sedi_pocty([], [_], [_]).
sedi_pocty([_], [], [_]).

sedi_pocty([ _ | Zs1], [ _ | Zs2], [ _ | Zs3]) :- 
    sedi_pocty(Zs1, Zs2, Zs3).

tret(S, T1, T2, T3) :-
    append(Temp, T3, S),
    append(T1, T2, Temp),
    filter(T1, Z1),
    filter(T2, Z2),
    filter(T3, Z3),
    sedi_pocty(Z1, Z2, Z3).


% tret([z1, a, b, z2, c,  z3, z4], T1, T2, T3).

pul(+S, -P1, -P2) :-
    append(P1, P2, S).