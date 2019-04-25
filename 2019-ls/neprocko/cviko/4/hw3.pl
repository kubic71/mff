:- op(100, xfy, ~).
:- op(100, xfy, ..).



valid(A, B, C) :- 
    (A < B, A < C);
    (A > B, A > C).


ar_seq(A, _, A, [A]) :- !.

ar_seq(A, B, C, []) :-
    not(valid(A, B, C)),
    !.

ar_seq(A, B, C, [A | Z]) :-
    valid(A, B, C),
    Q is B - A,
    NEWB is B + Q,
    ar_seq(B, NEWB, C, Z).


seq(A, B, X) :-
    A < B,
    A1 is A + 1,
    ar_seq(A, A1, B, X).


seq(A, B, []) :-
    A > B.

seq(A, A, [A]).

% pokud neni co rozvinout, skonci
rozvin(S, S) :-
    not(append(Z, [A..B| K], S)),
    not(append(Z, [A~B..C| K], S)).


% postupne nahrazuje rady a, a+1, a+2...b v seznamu
rozvin(S, V) :- 
    append(Z, [A..B| K], S),
    seq(A, B, X),
    append(Z, X, Z1),
    append(Z1, K, NewS),
    rozvin(NewS, V),
    !.


% postupne nahrazuje aritmeticke sekvence v seznamu
rozvin(S, V) :- 
    append(Z, [A~B..C| K], S),
    ar_seq(A, B, C, X),
    append(Z, X, Z1),
    append(Z1, K, NewS),
    rozvin(NewS, V),
    !.




% rozvin(+StrucnySeznam,-UplnySeznam) 
%?-rozvin([10,1..4,13,14~12..9 ,5..5,4..3],X) 
 % X=[10,1,2,3,4,13,14,12,10,5]