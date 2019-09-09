-- Je dána číselná matice A. Definujte funkci

-- kumulace :: Num a => [[a]] -> [[a]]

-- která z matice A vyrobí matici B stejných rozměrů (viz příklad níže)

-- každý prvek na souřadnicích (i,j) bude roven součtu všech hodnot
-- v submatici s levým horním rohem (0,0)
-- a pravým dolním rohem (i,j)

-- Poznámka: Snažte se vyhnout opakování stejných výpočtů.


soucet i j matice = sum $ [ matice !! x !! y | x <- [0..i], y <- [0..j]]

kumulace :: Num a => [[a]] -> [[a]]
kumulace m = [[ soucet i j m | j <- [0..(length (m !! 0))-1] ] | i <- [0..(length m)-1] ]

-- spocita dalsi radek souctu matice, dostane predchozi radek souctu matice a soucty dalsiho radku
kumulace_radek :: Num a => [a] -> [a] -> [a]
kumulace_radek prev_sum row_sum = zipWith (+) prev_sum row_sum

soucty_radku = scanl1 (+)

kumulace2 m = tail $ scanl (\soucty_matice dalsi_radek -> kumulace_radek soucty_matice $ soucty_radku dalsi_radek) (take (length (m !! 0)) $ repeat 0) m