zip(Xs, Ys, Zs) :-
    zip(Xs, Ys, [], Zs).

zip([], [], Zs, Zs).
zip([], [_ | _], Zs, Zs).
zip([_ | _], [], Zs, Zs).

zip([X | Xs], [Y | Ys], Temp, Zs) :- 
    append(Temp, [X-Y], NewTemp),
    zip(Xs, Ys, NewTemp, Zs).
