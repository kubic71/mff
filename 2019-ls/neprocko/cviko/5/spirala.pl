rotate(Empty, []) :-
    % check if the matrix is empty ( [[], [], []...])
    check_empty(Empty).

check_empty([]).

check_empty([[] | Rest]) :-
    check_empty(Rest).

rotate(Matrix, [Last_Column | Rest_Rotated]) :- 
    get_last_column(Matrix, Rest, Last_Column),
    rotate(Rest, Rest_Rotated).


% split matrix into last column and the rest of matrix
get_last_column(Matrix, Rest, Last_Column) :-
    get_last_column(Matrix, Rest, Last_Column, [], []).

% base case
% only elements were appended to accumulators in wrong order, so they need to be reversed
get_last_column([], Rest, Last_Column, RestRev, Last_ColumnRev) :- 
    reverse(RestRev, Rest),
    reverse(Last_ColumnRev, Last_Column).


get_last_column([FirstRow | RestOfMatrix], Rest, Last_Column, Rest_Ac, Last_Column_Ac) :-
    last(FirstRow, LastElement),
    append(FirstPartOfFirstRow, [LastElement], FirstRow),   % split first row into first n-1 elements and the last element
    get_last_column(RestOfMatrix, Rest, Last_Column, [FirstPartOfFirstRow | Rest_Ac], [ LastElement | Last_Column_Ac]).  % append to accumulators


spiral([], []) :- !. 


spiral(Matrix, WholeSpiral) :- % rotate, take the first row, and solve recursively
    rotate(Matrix, [FirstRow | Rest]),
    spiral(Rest, RestOfSpiral),
    append(FirstRow, RestOfSpiral, WholeSpiral).

