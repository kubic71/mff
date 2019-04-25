ceiling2 :: Double -> Int
ceiling2 x = getClosestBiggerInt (getBiggerInt 0 1 x) x

-- find some integer that is bigger in O(log(n)) time
getBiggerInt :: Int -> Int -> Double -> Int
getBiggerInt candidate stepsize x
    | fromIntegral candidate > x = candidate
    | otherwise = getBiggerInt (candidate + stepsize) (stepsize * 2) x

-- return biggest power of two, that is smaller or equal to x (x >= 1)
biggestPowerOfTwo :: Double -> Int
biggestPowerOfTwo x = biggestPowerOfTwo2 1 x

biggestPowerOfTwo2 :: Int -> Double -> Int
biggestPowerOfTwo2 current x
    | fromIntegral(current * 2) > x = current
    | otherwise = biggestPowerOfTwo2 (current * 2) x

-- given some integer bigger than x, return the closest bigger integer to x
getClosestBiggerInt :: Int -> Double -> Int
getClosestBiggerInt bigger x
    | (fromIntegral(bigger) - x) < 1 = bigger
    | otherwise = getClosestBiggerInt (bigger - biggestPowerOfTwo(fromIntegral(bigger) - x)) x