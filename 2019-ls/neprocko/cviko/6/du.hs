data Oper = Plus | Minus | Krat | Div

data Exp = Konst Int | Exp Oper Exp Exp 

instance Show Oper where
    show Plus = "+"
    show Minus = "-"
    show Krat = "*"
    show Div = "`div`"



instance Show Exp where
    show (Konst n) = show n
    show (Exp op l r) = zavorky l ++ show op ++ zavorky r
        where zavorky (Konst n) = show n
              zavorky exp = "(" ++ show exp ++ ")"

-- evaluate expression
eval (Konst n) = n
eval (Exp Plus l r) = (eval l) + (eval r)
eval (Exp Minus l r) = (eval l) - (eval r)
eval (Exp Krat l r) = (eval l) * (eval r)
eval (Exp Div l r) = (eval l) `div` (eval r)

op_list = [Plus, Minus, Krat, Div]

-- split list of numbers into 2 halves, all possible ways 
split_list list = [(take i list, reverse (take (size - i) (reverse list)))  | i <- [1..size - 1]]
    where size = length list

-- combine left and right expressions with all possible Juoperators    
combine_expressions l_list r_list = [Exp op l r | l <- l_list, r <- r_list, op <- op_list, if (show op) == "`div`" then (eval r) /= 0 else True]

-- generate all expressions 
gen_exp number_list
    | size == 0 = []
    | size == 1 = [ Konst (head number_list) ]
    | otherwise = concat [combine_expressions (gen_exp l) (gen_exp r) | (l, r) <- split_list number_list] -- 
    where size = length number_list

-- filter out expressions not equal to target value
arit number_list target = [ exp | exp <- (gen_exp number_list), (eval exp) == target ] 
