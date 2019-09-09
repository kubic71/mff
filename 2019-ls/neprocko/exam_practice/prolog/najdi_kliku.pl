podmnoziny(A, S) :-
    podmnoziny(A, [], S).

podmnoziny([], Acc, Acc).

podmnoziny([H|T], Acc, S) :-
    (podmnoziny(T, Acc, S); podmnoziny(T, [H|Acc], S)).

vede_tu_hrana(g(V, _), V1, V1) :-
    member(V1, V).

vede_tu_hrana(g(_, E), V1, V2) :- 
    member(V1-V2, E); member(V2-V1, E).


klika(g(V, E), K) :-
    podmnoziny(V, K),
    forall((member(V1, K), member(V2, K)), vede_tu_hrana(g(V, E), V1, V2)).

% g([1,2,3,4,5,6], [1-2, 2-3, 2-4, 3-5, 3-6, 5-6, 1-4])



