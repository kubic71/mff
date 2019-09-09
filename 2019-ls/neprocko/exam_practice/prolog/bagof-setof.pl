intersection(S1, S2, U) :- 
    setof(X,(member(X, S1), member(X, S2)), U).

union(S1, S2, U) :- 
    setof(X,(member(X, S1); member(X, S2)), U).


trida(b,sou).
trida(a,sam).
trida(c,sou).
trida(e,sam).
trida(e,sam).
trida(d,sou).


reverse([], []).
reverse([H|T], V) :- 
    reverse(T, T1),
    append(T1, [H], V).


% sat(F) :- 

all_possible_assignments([], []).

all_possible_assignments([Var|Rest], [Var-true|RestAssignment]) :-
    all_possible_assignments(Rest, RestAssignment).

all_possible_assignments([Var|Rest], [Var-false|RestAssignment]) :-
    all_possible_assignments(Rest, RestAssignment).


preorder(S) :- 
    preorder(S, 1, _).


preorder(nil, Preorder, Preorder).
preorder(t(L, _, Preorder, _, R), Preorder, X_vystupni) :-
    P1 is Preorder + 1,
    preorder(L, P1, X_vystupni_levy),
    preorder(R, X_vystupni_levy, X_vystupni).


postorder(S) :-
    postorder(S, 1, _).

postorder(nil, Postorder, Postorder).
postorder(t(L, _, _, X_vystupni_pravy, R), Postorder, X_vystupni) :-
    postorder(L, Postorder, X_vystupni_levy),
    postorder(R, X_vystupni_levy, X_vystupni_pravy),
    X_vystupni is X_vystupni_pravy + 1.

assign(S) :-
    preorder(S),
    postorder(S).

% t(t(t(nil, 4, P4, PO4, nil), 2, P2, PO2, t(nil, 5, P5, PO5, nil)), 1, P1, Po1, t(nil, 3, P3, PO3, nil))

