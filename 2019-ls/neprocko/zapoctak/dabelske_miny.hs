import Data.Array
import System.Random

main = do
    g <- newStdGen
    print . take 10 $ (randomRs ('a', 'z') g)