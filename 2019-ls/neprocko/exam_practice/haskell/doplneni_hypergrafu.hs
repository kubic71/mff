import qualified Data.Set as S
import qualified Data.List as L

-- Haskell: Doplnění hypergrafu (5 bodů)
-- Hypergraf je zadán množinou vrcholů a množinou hyperhran, což jsou alespoň dvouprvkové podmnožiny množiny vrcholů.
--  Naší cílem je definovat funkci doplnění, která doplní do hypergrafu H všechny dvouprvkové (hyper)hrany pro ty dvojice vrcholů, 
-- které nejsou společně obsaženy v žádné hyperhraně vstupního hypergrafu H. Funkce tedy např. z hypergrafu

--     s vrcholy {1,2,3,4,5} a hyperhranani {1,3,5} a {2,3,4}
--     vytvoří hypergraf se stejnými vrcholy a hyperhranami {1,3,5},{2,3,4},{1,2},{1,4},{5,2} a {5,4}


-- (a) Definujte datový typ pro reprezentaci hypergrafu. 
-- Pokuste se o co nejobecnější definici (vrcholy mohou být reprezentovány nejen čísly, ale i znaky, řetězci apod.)

-- (b) Specifikujte typovou signaturu funkce

-- doplneni ::

-- (c) Funkci definujte.

data HyperGraph a = HyperGraph [a]  [Edge a]
type Edge a = S.Set a

instance (Show a) => Show (HyperGraph a) where  
    
    show (HyperGraph vertices edges) = "Vertices:\n" ++ (show vertices) ++ "\n\nEdges:" ++ (show $ map S.toList edges)

doplneni :: Ord a => HyperGraph a -> HyperGraph a
doplneni (HyperGraph vertices edges) = HyperGraph vertices (edges ++ missing_edges)
    where missing_edges = filter (\edge -> edgeNotSubsetOfOtherEdge edge edges  )$ getAll2Edges vertices

edgeNotSubsetOfOtherEdge edge edges = all (\e -> not (edge `S.isSubsetOf` e)) edges

getAll2Edges vertices = [S.fromList [x, y] | x <- vertices, y <- vertices, x < y]



