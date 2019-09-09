% Prolog: Generování výrokových formulí (5 bodů)
% Formule výrokového počtu jsou sestavené z (výrokových) proměnných ve funktoru var/1 a logických spojek negace, konjunkce a disjunkce (bez konstant). Dále máte dány v argumentech predikátu gen/3 číslo k pro velikost formule a seznam jmen proměnných. Generujte backtrackingem všechny logické formule (každou jednou), které obsahují proměnné ze seznamu a ve kterých je počet spojek a výskytů proměnných dohromady právě k.

% Definujte predikát gen(+K, +Jmena, -Fle). Na pořadí generovaných formulí nezáleží, ale měli byste vygenerovat každou právě jednou. K řešení není potřeba predikát =../2 (univ).

% Příklad:

% ?- gen(4,[p],F).

% F = not(not(not(var(p))));
% F = not(and(var(p),var(p)));
% F = not(or(var(p),var(p)));
% F = and(not(var(p)),var(p));
% F = and(var(p),not(var(p)));
% F = or(not(var(p)),var(p));
% F = or(var(p),not(var(p)));
% false.

gen(1, P, var(V)) :- member(V, P).
gen(2, P, not(F)) :- gen(1, P, F).

gen(N, Jmena, not(F)) :-
    N > 2,
    N1 is N - 1,
    gen(N1, Jmena, F).

gen(N, Jmena, F) :-
    N > 2,
    C is N - 2,
    C1 is N - 1,
    between(1, C, A),
    B is C1 - A,
    gen(A, Jmena, F1),
    gen(B, Jmena, F2),
    (F = and(F1, F2); F= or(F1, F2)).

power(0, A, 1).
power(N, A, Res) :- 
    N >= 1,
    Nm1 is N - 1,
    power(Nm1, A, X),
    Res is A * X.