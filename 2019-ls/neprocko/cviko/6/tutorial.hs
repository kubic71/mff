-- sgn :: Int -> Int
-- sgn 0 = 0
-- sgn n = if n > 0 then 1 else -1

fib :: Int -> Int

fib 1 = 1
fib 2 = 1
fib n = fib(n-1) + fib(n-2)


fib1 n = if n==1 || n==2 then 1 
        else fib1(n-1) + fib1(n-2)

fib2 n | n==1 = 1
        | n==2 = 1
        | n>2 = fib2(n-1) + fib2(n-1)
        | otherwise = error "chybny argument"


-- hlava seznamu
head' :: [a] -> a
head' (x:_) = x
tail' :: [a] -> [a]
tail' (_:xs) = xs


druhy :: [a] -> a
druhy (_: d:_) = d

druhy2 :: [a] -> a
druhy2 xs = head(tail xs )

druhy4 = head.tail

otoc xs = otoc2 xs []
otoc2 [] as = as 
otoc2 (x:xs) ys = otoc2 xs (x:ys)


shiftl n xs = drop n xs ++ take n xs


shiftl2 n xs = drop m xs ++ take m xs
                where m = n `mod` length xs

prumer xs = sum xs / fromIntegral (length xs)


zip2 [] _ = []
zip2 _ [] = []
zip2 (x:xs) (y:ys) = (x, y):(zip2 xs ys)

delitele :: Int -> [Int]
delitele n = [m | m <- [1..n], n `mod` m == 0 ]

prvocisla n = [m | m <- [1..n], length (delitele m) == 2]


-- DU definovat funkci, ktera vrati horni celou cast ceiling 