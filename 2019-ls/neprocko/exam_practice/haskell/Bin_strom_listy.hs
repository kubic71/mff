import qualified Data.List as L
data Tree a = Leaf a | Tree (Tree a) (Tree a) deriving (Show)

countRightEdges :: Tree a -> Int -> [(a, Int)]
countRightEdges (Leaf a) currentEdges = [(a,currentEdges)] 
countRightEdges (Tree left right) currentEdges = leftList ++ rightList
    where leftList = countRightEdges left currentEdges
          rightList = countRightEdges right (currentEdges + 1)

-- countRightEdges 
getTree =  Tree (Tree (Leaf 1) (Leaf 2) ) (Tree  (Leaf 3) (Leaf 4) )

getSets tree = map extractFromTuples $ L.groupBy (\(_, v1) (_, v2) -> v1 == v2) counts
    where counts = countRightEdges tree 0

extractFromTuples list = map (\(a, b) -> a) list
