rozdel :: (Num a, Eq a) => [a] -> Maybe ([a], [a])
rozdel multi = rozdel1 multi [] []

rozdel1 [] cast1 cast2
    | sum cast1 == sum cast2 = Just (cast1, cast2)
    | otherwise = Nothing

rozdel1 (h:t) cast1 cast2 = if verze1 == Nothing then verze2 else verze1
    where verze1 = rozdel1 t (h:cast1) cast2
          verze2 = rozdel1 t cast1 (h:cast2)

