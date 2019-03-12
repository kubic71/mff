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


perm2cyk([[a,b], [b,c], [c,a], [d,d], [e,f], [f,e]], Cycles).