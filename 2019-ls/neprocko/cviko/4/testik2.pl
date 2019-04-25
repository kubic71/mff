zip([], [], []).
zip([], [_ | _], []).
zip([_ | _], [], []).

zip([X | Xs], [Y | Ys], [X-Y | T]) :- 
    zip(Xs, Ys, T).

