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

head' :: [a] -> a  
head' [] = error "Can't call head on an empty list, dummy!"  
head' (x:_) = x  


getFirstTwo :: [a] -> [a]
getFirstTwo (x:y:_) = [x, y]

lastTwo :: [a] -> [a]
lastTwo l = reverse(getFirstTwo(reverse l))

bmiTell weight height  
     | bmi <= skinny = "You're underweight, you emo, you!"  
        | bmi <= normal = "You're supposedly normal. Pffft, I bet you're ugly!"  
     | bmi <= fat    = "You're fat! Lose some weight, fatty!"  
 | otherwise     = "You're a whale, congratulations!"  
    where 
        bmi = weight / height ^ 2  
        skinny = 18.5
        normal = 24.2
        fat = 30

cal :: (RealFloat a) => a -> a -> a
cal x y = s * y where s = x ** 2; t = y ** 3 