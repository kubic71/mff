
edge(V1, V1, _).
edge(V1, V2, E) :-
    member(V1-V2, E); member(V2-V1, E).
% pokud to jde, pridej_vrchol zvetsi nezavislou mnozinu o 1 vrchol, pokud nejde zvetsit, selze
pridej_vrchol(graf(V, E), NM, [V1|NM]) :-
    % V1 je kandidát na přidání do Nezávislé množiny
    member(V1, V),

    % neexistuje žádný vrchol z nezávislé množiny, který by měl s novým vrcholem V1 hranu
    \+ (member(V2, NM), edge(V1, V2, E)).

nezavisla_mnozina(G, NM) :-
    nezavisla_mnozina(G, [], NM).

% pokud nejde pridat vrchol, vrat nezavislou mnozinu
nezavisla_mnozina(G, Acc, Acc) :-
    \+ pridej_vrchol(G, Acc, _).

% Pokud jde pridat vrchol, pridavej
nezavisla_mnozina(G, Acc, NM) :- 
    pridej_vrchol(G, Acc, New_Acc),
    nezavisla_mnozina(G, New_Acc, NM).


