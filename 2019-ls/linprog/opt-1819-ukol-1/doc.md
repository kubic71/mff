#Jak program sestavit
Oba dva úkoly jsou napsány v pythonu 3, není třeba tedy nic sestavovat, pouze spustit interpretr. 

#Ovládání
Programy pro první i druhou úlohu přijímají na stdin vstup v definovaném formátu.
Pro spuštění 1. úkolu se vstupem vstup1-000.txt stačí zadat <code>cat vstup1-000.txt | python transform1.py</code>. Podobně pro druhý úkol. Program na stdout vypíše kód spustitelný glpsolverem. Program je možné spustit na všech testovacích vstupech bash skriptem <code>exec_all_{i}.sh</code>, stačí umístit složku se vstupy do stejného adresáře.

# Jak vypadá LP

## Úkol 1
Pro každý vrchol si zavedu proměnnou <code> x[i] >= 0 </code>, která bude každému vrcholu přiřazovat pořadové číslo v uspořádání. Pokud vede hrana z <code>u</code> do <code>v</code>, přidám podmínku <code>x[v] >= x[u] + 1</code>. Minimalizace maximální hodnoty pořadového čísla zajistí celočíselnost všech <code>x[i]</code>, protože pokud by nějaké <code>x[i]</code> nebylo celočíselné, pak by šlo řešení o epsilon vylepšit. 

## Úkol 2
Pro každou hranu si zavedu nula-jedničkovou proměnnou, která mi bude říkat, jestli se hrana nachází v optimálním podgrafu. Pak pro každý 3 a 4-cyklus v původním grafu si zavedu podmnínku, že v optimálním podgrafu alespoň jedna hrana cyklu nebude. Maximalizuji vážený součet zachovaných hran, neboli se minimalizuje vážený součet odstraněných hran.

# No primal solution
## Úkol 1
Topologicky uspořádat jdou pouze acyklické grafy, pokud neexistuje řešení, pak v grafu musí být cyklus.

## Úkol 2
Vždy můžu odstranit všechny hrany grafu a získat tak řešení, které nejspíš optimální nebude. 
  
