%  koncept([ [barva-modra, motor-diesel, pocet_kol-6], [barva-bila, motor-plyn, pocet_mist-40], [motor-elektro, pocet_mist-5] ], Koncept).

koncept(Objekty, Koncept) :- 
    mnozina_klicu(Objekty, MK),
    maplist(f, MK, Initial_koncept),
    koncept1(Objekty,  MK, Initial_koncept, Duplicate_Koncept),
    remove_duplicates(Duplicate_Koncept, [], Koncept).



remove_duplicates([], K, K).
remove_duplicates([Klic-Seznam|Rest], Old_K, K) :-
    sort(Seznam, UniqS),
    remove_duplicates(Rest, [Klic-UniqS | Old_K], K).



koncept1([], _, K, K).
koncept1([Objekt | Zbytek], MK, Stavajici_koncept, Koncept) :-
    pridej_do_konceptu(Objekt, MK, Stavajici_koncept, Novy_koncept),
    koncept1(Zbytek, MK, Novy_koncept, Koncept).



prostredni([A], A).
prostredni([A,B], A).
prostredni([A,B], B).

prostredni([H | Xs], Mid) :-
    append(Zbytek, [_], Xs),
    prostredni(Zbytek, Mid).


prunik([],_,[]).
prunik(_,[],[]).
prunik([X|Xs], Y, [X|Z]):-member(X,Y), prunik(Xs,Y,Z), !.
prunik([_|Xs], Y, Z):-prunik(Xs,Y,Z).

prunik([H|A], B, P) :-
    prunik(A, B, P).

delka([], 0).
delka([_|Xs], D) :-
    delka(Xs, D1),
    D is D1 + 1.

mocnina(_, 0, 1).
mocnina(A, N, X) :-
    N > 0,
    Nm1 is N - 1,
    mocnina(A, Nm1, X1),
    X is X1 * A.

min(X, Y, X) :- X < Y.
min(X, Y, Y) :- X >= Y.

minSeznam([X], X).

minSeznam([H|T], Min) :- 
    minSeznam(T, Min1),
    min(Min1, H, Min).


minSeznam2([H|T], Min) :- minSeznam2(T, H, Min).
minSeznam2([], A, A).
minSeznam2([H|T], A, Min) :-
    H < A,
    minSeznam2(T, H, Min).
minSeznam2([H|T], A, Min) :-
    A =< H,
    minSeznam2(T, A, Min).



nTy([X|_], 0, X).

nTy([_|T], N, Y) :-
    N > 0,
    N1 is N - 1,
    nTy(T, N1, Y).


union(A, B, D) :-
    append(A, B, C),
    sort(C, D).
    




f2([], []).
f2([K|Rest], [K-nedef| Zbytek]) :- 
    f2(Rest, Zbytek).


zmen(Object, Klic, Hodnota, NovyObject) :- 
    append(Start, [Klic-_ | Konec], Object),
    append(Start, [Klic-Hodnota | Konec], NovyObject).


zapis([], OK, OK).
zapis([Klic-Hodnota | Rest], StaryOK, FinalOK) :-
    zmen(StaryOK, Klic, Hodnota, NovyOK),
    zapis(Rest, NovyOK, FinalOK).

    


pridej_do_konceptu(Objekt, MK, Stavajici_koncept, Novy_koncept) :-
    f2(MK, OK),
    zapis(Objekt, OK, Objekt_projekce),
    merge_koncept(Objekt_projekce, Stavajici_koncept, Novy_koncept).
    
merge_koncept([], K, K).
merge_koncept([Klic-Hodnota | Rest], Stavajici_koncept, Vysledny_koncept) :-
    append(ZK, [Klic-Seznam | KK], Stavajici_koncept),
    append(Seznam, [Hodnota], NovySeznam),
    append(ZK, [Klic-NovySeznam | KK], Novy_koncept),
    merge_koncept(Rest, Novy_koncept, Vysledny_koncept).



f(Klic, Y) :- Y=Klic-[].

union([], L2, L2).
union([H | L1], L2, Result) :- 
    member(H, L2),
    union(L1, L2, Result).

union([H | L1], L2, Result) :-
    not(member(H, L2)),
    union(L1, [H | L2], Result).



mnozina_klicu_objektu([], Mnozina, Mnozina).
mnozina_klicu_objektu([Klic-_| Zbytek_objektu], Stara_mnozina, Vysledna_mnozina) :- 
    union([Klic], Stara_mnozina, Nova_mnozina),
    mnozina_klicu_objektu(Zbytek_objektu, Nova_mnozina, Vysledna_mnozina).

mnozina_klicu([], []).

mnozina_klicu([Objekt | Zbytek], Mnozina) :-
    mnozina_klicu(Zbytek, Mnozina2),
    mnozina_klicu_objektu(Objekt, [], Mnozina1),
    union(Mnozina1, Mnozina2, Mnozina).


% pridej_prvek_do_konceptu(Klic-Hodnota, Stavajici_koncept, Vysledny_koncept) :-

sum([], 0).
sum([H|T], S) :-
    sum(T, S1),
    S is S1 + H.

vyber(S, N, Z) :- 
    vyber(S, N, [], Z).

vyber([], N, Z, Z) :- sum(Z, N).
vyber([H|T], N, Z1, Z) :- 
    sum([H | Z1], SumCurrent),
    N_zbytek is N - SumCurrent,
    vyber(T, N_zbytek, Z2),
    append([H|Z1], Z2, Z).

vyber([H|T], N, Z1, Z) :- 
    sum(Z1, SumCurrent),
    N_zbytek is N - SumCurrent,
    vyber(T, N_zbytek, Z2),
    append(Z1, Z2, Z).

vyber2([], 0, []).
vyber2([H|T], N, [H|Z1]) :-
    NMH is N - H,
    vyber2(T, NMH, Z1).
vyber2([_|T], N, Z) :-
    vyber2(T, N, Z).


vymaz(X,[X|Xs],Xs).
vymaz(X,[Z|Xs],[Z|Y]) :- vymaz(X,Xs,Y).



vyber3(X, N, Z):-vyber3(X, N, 0, [], Z).
vyber3(_, N, N, Z, Z).
vyber3(X, N, A, Z, V):-member(P, X), B is A + P, B =< N,
                       vymaz(P, X, Xz), vyber3(Xz, N, B, [P|Z], V).

rozdel([], N, [], []).
rozdel([H|T], N, [H | Mensi], Vetsi) :-
    H < N,
    rozdel(T, N, Mensi, Vetsi).

rozdel([H|T], N, Mensi, [H| Vetsi]) :-
    H >= N,
    rozdel(T, N, Mensi, Vetsi).

spojeni([], A, A).
spojeni([H|T], B, [H|V]) :-
    spojeni(T, B, V).



zretezRozdil(A-B, B-C, A-C).

obycToRozdil([], X-X).
obycToRozdil([H|T], [H|S]-X) :-
    obycToRozdil(T, S-X).

rozdilToObyc(Xs-[], Xs).

qsort(S, Sorted) :-
    obycToRozdil(S, Rs),
    qsortRS(Rs, Rs_sorted),
    rozdilToObyc(Rs_sorted, Sorted).

qsortRS(X-X, X-X).

qsortRS([H|T]-X, V) :-
    rozdelRS(T-X, H, Mensi, Vetsi),
    qsortRS(Mensi, Mensi_sorted),
    qsortRS(Vetsi, Vetsi_sorted),
    zretezRozdil(Mensi_sorted, [H|X2]-X2, Temp),
    zretezRozdil(Temp, Vetsi_sorted, V).

rozdelRS(X-X, _, Y-Y, Z-Z).
rozdelRS([A|T]-X1, H, [A|Mensi]-X2, Vetsi) :-
    A < H,
    rozdelRS(T-X1, H, Mensi-X2, Vetsi).
    
rozdelRS([A|T]-X1, H, Mensi, [A|Vetsi]-X2) :-
    A >= H,
    rozdelRS(T-X1, H, Mensi, Vetsi-X2).

