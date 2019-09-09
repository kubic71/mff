type Polynomial =  [Double]
-- polynomy jsou reprezentovany jako seznamy koeficientu
-- koeficient s indexem 0 odpovida koeficientu u clenu x^0, index 1 odpovida koeficientu clenu x^1 atd.

-- pomocne funkce
degree polynom = length (dropWhile (== 0) (reverse(polynom))) - 1

padTo targetDeg polynom = polynom ++ (take diff (repeat 0))
    where diff = max (targetDeg - (degree polynom)) 0 

alignPolynomials p1 p2 = (padTo d p1, padTo d p2) where d = max (degree p1) (degree p2)

add_polynomials p1 p2 = zipWith (+) padded_p1 padded_p2
    where (padded_p1, padded_p2) = alignPolynomials p1 p2

-- multiply by a constant
mul polynom num = map (* num) polynom
substract_polynomials p1 p2 = add_polynomials p1 (mul p2 (-1))

leadingCoeff polynom = polynom !! degree polynom

shiftr polynom n = take n (repeat 0) ++ polynom



polydiv :: Polynomial -> Polynomial -> (Polynomial, Polynomial)
polydiv delenec delitel 
    | degree delitel == -1 = error "Cannot divide by zero!"
    | degree(delenec) < degree(delitel) = ([0], delenec)
    | otherwise = (add_polynomials (shiftr [a/b] diff) podil2, zbytek) 
    where 
          diff = degree delenec - degree delitel
          a = leadingCoeff delenec
          b = leadingCoeff delitel
          (podil2, zbytek) = polydiv (substract_polynomials delenec (shiftr (mul delitel(a/b)) diff)) delitel
    

    
tp1 = [-4.0, 0.0, 2.0, -1.0, 0.0, 1.0]
tp2 = [0.0, 2.0, 0.0, 1.0]

