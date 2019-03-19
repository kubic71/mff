perm([], []).
perm([X | Xs], Zs) :- 
    select(X, Zs, Ys),
    perm(Xs, Ys).


% prirozene_cislo(?X) :- X je přirozené číslo. 
prirozene_cislo(0). 
prirozene_cislo(s(X)) :- prirozene_cislo(X).
% mensi(+X,+Y):- X je ostře menší než Y. 
mensi(0,s(X)) :- prirozene_cislo(X). 
mensi(s(X),s(Y)) :- mensi(X,Y).

mensi2(X,s(X)) :- prirozene_cislo(X). 
mensi2(X,s(Y)) :- mensi2(X,Y).


% soucet(+X,+Y,?Z) :- Z=X+Y.
soucet(0,X,X) :- prirozene_cislo(X).
soucet(s(X),Y,s(Z)) :- soucet(X,Y,Z).

 % soucin(+X,+Y,?Z) :- Z=X*Y. 
soucin(0,X,0) :- prirozene_cislo(X). 
soucin(s(X),Y,Z) :- soucin(X,Y,W),soucet(W,Y,Z). 

% soucin2(+X,+Y,?Z) :- alternativní definice 
soucin2(0,X,0) :- prirozene_cislo(X). 
soucin2(s(X),Y,Z) :- soucet(W,Y,Z),soucin2(X,Y,W).



rodic(jan, petr).
rodic(jan, elis).
rodic(petr, kuba).


predek2(X,Y) :- rodic(X,Y).
predek2(X,Z) :- predek2(Y,Z), rodic(X,Y).


max(X, Y, X) :- X >= Y.
max(X, Y, Y) :- X < Y.