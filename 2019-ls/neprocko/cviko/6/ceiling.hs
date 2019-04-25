fib1 n = if n==1 || n==2 then 1 
        else fib1(n-1) + fib1(n-2)



ciel :: Double -> Double
ciel n = if fromIntegral(floor n)==n then n else fromIntegral((floor n) + 1)

