% Jsou dány predikáty muz/1, zena/1 a rodina(Otec, Matka, Deti)
% kde Deti je seznam dětí od nejstaršího k nejmladšímu

muz(adam).  muz(jan).   muz(petr).  muz(pavel). 

zena(eva).  zena(anna). zena(marie).

rodina(adam, eva, [jan, petr, marie, pavel]).
rodina(petr, anna, []).

% Definujte predikáty starsibratr/2, nejstarsibratr/2 a bratri/2.
startsibratr(Kdo, Koho) :- 
    rodina(_, _, S),
    append(Starsi, [Koho | _], S),
    member(Kdo, Starsi),
    muz(Kdo).

% starsibratr(?Kdo, +Koho) :- Kdo je starším bratrem Koho. 
f(X) :- X = 5.

% ?- starsibratr(Kdo,pavel).
%  Kdo = jan ;
%  Kdo = petr

vyberMuze([X | Zbytek], [X | Bratri]) :-
    muz(X).


    
bratri(Koho) :- 
    rodina(_, _, Deti),
    select(Koho, Deti, Sourozenci),
    vyberMuze(Sourozenci, Bratri). 
    

% nejstarsibratr(?Kdo, +Koho) :- Kdo je nejstarším bratrem osoby Koho.
nejstarsibratr(Kdo, Koho) :-
    bratri([Kdo | _], Koho).


otestuj([H | T]) := muz(H).
% ?- nejstarsibratr(Kdo, petr). 
%  Kdo = jan

% ?- nejstarsibratr(Kdo, jan). 
%  Kdo = petr


% bratri(?Bratri, +Koho) :- Bratri jsou seznamem všech bratrů osoby Koho.

% ?- bratri(Bratri, petr). 
%  Bratri = [jan, pavel]