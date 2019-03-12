muz(adam).

test(X) :-  muz(X).

rozdel([H | T], H, T).

vypust(X, [X | Xs], Xs).
vypust(X, [Y | Xs], [Y | Zs]) :- vypust(X, Xs, Zs).


% built-in function append
zretez([], Ys, Ys).
zretez([X| Xs], Ys, [X | Zs]) :- zretez(Xs, Ys, Zs).

% A je v seznamu nalevo od B
sousede(A, B, S) :- append(_, [A, B | _], S).

sousede2(A, B, [A, B | _]).
sousede2(A, B, [_ | Xs]) :- sousede(A, B, Xs).


napravoOd(A, B, S) :- append(_, [A | Zs], S), member(B, Zs).

rshift(Xs, [Z | Ys]) :- 
    append(Ys, [Z], Xs).


% WTF this shit does? TODO
rshift2([X], [X]).
rshift2([X | Xs], [Z, X | Ys]) :- rshift2(Xs, [Z | Ys]).



% DU bonusova uloha:
% seznam delime na tretiny, aby v kazde bylo stejne zen (az na jednu), a naslo vsechna reseni

