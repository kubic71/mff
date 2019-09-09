# Ďábelské miny
Hrají se stejně jako běžné hledání min, ale jsou ďábelské, pokud hráč odhalí políčko, na kterém může být mina, mina tam vždy bude. Hráč tedy může vyhrát pouze tehdy, pokud odhaluje políčka, na kterých mina zaručeně není.

# Uživatelské dokumentace
### Spuštění 
Před spuštěním je třeba hru nejdříve zkompilovat: `ghc mines.hs`, poté stačí zkompilovanou hru z příkazové řádky sputit.
### Ovládání 
Hra se ovládá z příkazové řádky. Při každém tahu se zobrazí hráči hrací plocha a hráč zadáním souřadnic zvolí, které políčko chce odkrýt.
### Herní fáze 
Hra má 2 herní fáze - normální a ďábelskou. Prvních pár tahů probíhá stejně jako v obyčejných minách. Tato první fáze slouží k částečnému odhalení herní plochy, aby hra byla vůbec hratelná. Poté se po určitém počtu kroků hra přepne do oné ďábelské fáze. 
### Konec hry
Hráč prohrává v případě, že odhalil políčko s minou. Vyhrát může v normální fázi nebo v ďábelské fázi. V normální fázi hráč vyhrává tehdy, pokud odhalí všechna políčka, na kterých není mina. V ďábelské fázi hráč vyhrává tehdy, pokud na všech neodhalených políčkách musí být mina.

# Ukázka hry v normálním režimu
```
$ mines.exe

 0 1 2 3 4 5
 ------------
0|* * * * * *
1|* * * * * *
2|* * * * * *
3|* * * * * *
4|* * * * * *
5|* * * * * *
Devil mode: INACTIVE YET
Devil mode countdown: 3
input space-separated x y coordinates:
0 0
  0 1 2 3 4 5
 ------------
0|0 1 * * * *
1|0 1 * * * *
2|1 2 * * * *
3|* * * * * *
4|* * * * * *
5|* * * * * *
Devil mode: INACTIVE YET
Devil mode countdown: 2
input space-separated x y coordinates:
5 5
  0 1 2 3 4 5
 ------------
0|0 1 * * * *
1|0 1 * * * *
2|1 2 1 1 1 *
3|* * 1 0 1 *
4|* * 1 0 1 1
5|* * 1 0 0 0
Devil mode: INACTIVE YET
Devil mode countdown: 1
input space-separated x y coordinates:
3 0
  0 1 2 3 4 5
 ------------
0|0 1 * 1 * *
1|0 1 * * * *
2|1 2 1 1 1 *
3|* * 1 0 1 *
4|* * 1 0 1 1
5|* * 1 0 0 0
```

# Ukázka stejného původního rozložení min, akorát ďábelská fáze nastane o krok dříve

```
$ mines.exe

  0 1 2 3 4 5
 ------------
0|* * * * * *
1|* * * * * *
2|* * * * * *
3|* * * * * *
4|* * * * * *
5|* * * * * *
Devil mode: INACTIVE YET
Devil mode countdown: 2
input space-separated x y coordinates:
0 0
  0 1 2 3 4 5
 ------------
0|0 1 * * * *
1|0 1 * * * *
2|1 2 * * * *
3|* * * * * *
4|* * * * * *
5|* * * * * *
Devil mode: INACTIVE YET
Devil mode countdown: 1
input space-separated x y coordinates:
5 5
  0 1 2 3 4 5
 ------------
0|0 1 * * * *
1|0 1 * * * *
2|1 2 1 1 1 *
3|* * 1 0 1 *
4|* * 1 0 1 1
5|* * 1 0 0 0
Devil mode: ACTIVE!
input space-separated x y coordinates:
3 0
You lost!
  0 1 2 3 4 5
 ------------
0|0 1 2 X X X
1|0 1 X 3 3 2
2|1 2 1 1 1 1
3|X 3 1 0 1 X
4|X X 1 0 1 1
5|X 3 1 0 0 0

```
Zde je vidět, že ďábel zařídil, aby na políčku 3 0 byla mina, ač tam v normálním režimu nebyla.