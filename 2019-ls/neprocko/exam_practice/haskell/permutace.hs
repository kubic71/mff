import qualified Data.List as L
-- permutace seznam dvojice = 

check _ [] = True
check perm ((a,b):dvojice) = (ai < bi) && (check perm dvojice)
    where Just ai = L.elemIndex a perm
          Just bi = L.elemIndex b perm

permutace seznam dvojice = filter (\perm -> check perm dvojice) $ permutations seznam 

permutace1 :: (Eq a, Show a) => [a] -> [a] -> [(a, a)] -> IO ()
permutace1 [] acc dvojice = if valid then putStrLn (show acc) else return ()
    where valid = check acc dvojice

-- permutace1

permutations :: Eq a => [a] -> [[a]]
permutations [x] = [[x]]
permutations as = foldl (\acc (x,sel) -> acc ++ (putAtStart x (permutations sel))) [] $ selections as

putAtStart :: a -> [[a]] -> [[a]]
putAtStart _ [] = []
putAtStart x (l:ls) = (x:l):(putAtStart x ls)

selections [] = []
selections (x:xs) = (x, xs): [(y, x:ys)  | (y, ys) <- selections xs]