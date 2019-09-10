kombinace _ 0 = [[]]
kombinace [] _ = []

-- set != [], n > 0
kombinace (x:xs) n = k1 ++ k2
    where k1 = kombinace xs n
          k2 = insertX x (kombinace xs (n-1))

insertX x list = map (\l -> x:l ) list

