data HTML a = Elm String [(HTML a)] | Txt a

mapHTML::(a->b)->HTML a->HTML b
mapHTML fun (Txt text) = Txt (fun text) 
mapHTML fun (Elm e content) = Elm e (map (mapHTML fun) content)