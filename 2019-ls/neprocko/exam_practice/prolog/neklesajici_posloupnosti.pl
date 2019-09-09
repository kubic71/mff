seznam(N, S) :-
    seznam(N, 0, 1, [], S1),
    reverse(S1, S).

seznam(N, N, _, S, S).

seznam(N, CurrentSum, CurrentNumber, CurrentList, S) :- 
    UpperLimit is N - CurrentSum,
    between(CurrentNumber, UpperLimit, NextNumber),
    NextCurrentSum is CurrentSum + NextNumber,
    seznam(N, NextCurrentSum, NextNumber, [NextNumber|CurrentList], S).
