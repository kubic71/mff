data Tree a = Nil | Node a (Tree a) (Tree a)

count_baddness a predeccessors = length $ filter (\(p,op) -> op a p) predeccessors

getBadOnes tree = 
    findBadOnes [] [] tree


findBadOnes path currentBadList Nil = currentBadList
findBadOnes path currentBadList (Node a left right) =
    let list1 = findBadOnes ((a, (>)):path) currentBadList left
        list2 = findBadOnes ((a, (<)):path) list1 right
        baddness = count_baddness a path 
    in
        if (baddness > 0) then (a, baddness):list2 else list2

getTree = Node 3 (
    Node 2 (
        Node 0 Nil Nil
    ) (
        Node 1 Nil Nil
    )
 ) (
     Node 6 (
         Node 8 Nil Nil
     ) (
         Node 7 Nil (Node (-1) Nil Nil)
     )
 )

