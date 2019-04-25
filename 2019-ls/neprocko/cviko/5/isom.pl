isom(t(V, []), t(V, [])).
isom(t(V, S1), t(V, S2)) :- 
    isom_children(S1, S2).

% children are isomorphic if there exists bijection between the two lists where if f(x)=y, then x is isomorphic to y
isom_children([], []).

isom_children(S1, S2) :-
    length(S1, Length),
    length(S2, Length),  % lists of children must have the same length
    select(t(V_S1, S_S1), S1, NewS1),  % select two subtrees from lists S1 and S2 and check if they are isomorphic
    select(t(V_S1, S_S2), S2, NewS2),
    isom_children(S_S1, S_S2),
    isom_children(NewS1, NewS2).   % the rest of children still has to be isomorphic