relace x y = x `mod` 3 == y `mod` 3

-- pomocna funkce dostane relaci, seznam prvku a vrati dvojici (zbyle_prvky:jednu_tridu_ekvivalence)
get_class rel prvky = ([zbyly | zbyly <- prvky, not (rel prvni zbyly)], [x | x <- prvky, rel prvni x])
    where prvni = prvky !! 0

rozklad rel [] = []
rozklad rel prvky = (prvni_trida:rozklad rel zbytek)
    where (zbytek, prvni_trida) = get_class rel prvky

-- rozklad relace [1..10]