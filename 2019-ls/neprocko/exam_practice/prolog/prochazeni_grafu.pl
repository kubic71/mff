projdi(Dag, Start, InTimes, OutTimes) :- 
    projdi(Dag, [Start], 0,[], [], [], InTimes, OutTimes).

projdi(g(V, E), [], Time, Seen, CurrentInTimes, CurrentOutTimes, CurrentInTimes, CurrentOutTimes).

getUnseenNeighbours(Edges, V, Seen, UnseenNeighbours) :-
    findall(X, (member(V-X, Edges), \+ member(X, Seen)), UnseenNeighbours).

projdi(g(V, E), [CurrentVertex|RestOfQueue], Time, Seen, CurrentInTimes, CurrentOutTimes, InTimes, OutTimes) :-
    % out 
    member(CurrentVertex, Seen),
    NewOutTimes = [CurrentVertex-Time|CurrentOutTimes],
    Time1 is Time + 1,
    projdi(g(V, E), RestOfQueue, Time1, Seen, CurrentInTimes, NewOutTimes, InTimes, OutTimes).

projdi(g(V, E), [CurrentVertex|RestOfQueue], Time, Seen, CurrentInTimes, CurrentOutTimes, InTimes, OutTimes) :-
    % in
    \+ member(CurrentVertex, Seen),
    NewInTimes = [CurrentVertex-Time|CurrentInTimes],
    getUnseenNeighbours(E, CurrentVertex, Seen, ToVisit),
    Time1 is Time + 1,
    append(ToVisit, [CurrentVertex|RestOfQueue], NewQueue),
    projdi(g(V, E), NewQueue, Time1, [CurrentVertex|Seen], NewInTimes, CurrentOutTimes, InTimes, OutTimes).

% projdi(g([1,2,3,4,5,6,7], [1-2, 2-3, 2-4, 2-5, 5-6, 5-7]), 1, InTimes, OutTimes).