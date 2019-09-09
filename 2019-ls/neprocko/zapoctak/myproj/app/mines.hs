import System.Random
import System.IO
import Debug.Trace
import Control.Monad(when) 
import qualified Data.Map as M
import qualified Data.List as L
import qualified Data.Set as S



data Point = Point {x :: Int, y :: Int } deriving (Show, Eq, Ord)
-- data CellInfo = CellInfo {}

data GameInfo = GameInfo {boardSize :: Int} deriving (Show, Eq)


-- list of mines
data Mines = Mines [Point] deriving (Show)
emptyBoard = Mines []

isMineHere :: Mines -> Point -> Bool
isMineHere (Mines mines) point = elem point mines


-- stores whether cell is uncovered, and if it is, how many mines are in its surrounding
data Info = Covered | Uncovered Int deriving (Show, Eq)

data MinesInfo = MinesInfo (M.Map Point Info)

instance Show MinesInfo where
    show (MinesInfo info) = show info

changeInfo :: MinesInfo -> Point -> Info -> MinesInfo
changeInfo (MinesInfo m) point newInfo = MinesInfo (M.insert point newInfo m)

getInfo :: MinesInfo -> Point -> Info
getInfo (MinesInfo m) point = info
    where Just info = M.lookup point m

getRandomPoint gen size = let (x, newGen) = randomR (0, size-1) gen
                              (y, newGen2) = randomR (0, size-1) newGen
                              in (Point x y, newGen2)

getCoveredBoard size = MinesInfo $ M.fromList $ [(Point x y, Covered) | x <- [0 .. size-1], y <- [0 .. size-1]]

placeMinesRandomly :: (RandomGen gen) => gen -> Int -> Int -> Mines -> Mines
placeMinesRandomly gen board_size n (Mines mines)
    | n == 0 = Mines mines
    | n > 0 = placeMinesRandomly newGen board_size (if invalid_point then n else n-1) (if invalid_point then (Mines mines) else (Mines (point:mines)))
    where (point@(Point x y), newGen) = getRandomPoint gen board_size
          invalid_point = point `elem` mines

inBounds :: Int -> Point -> Bool
inBounds size (Point x y)  = (x >= 0) && (x < size) && (y >= 0) && (y < size)

getNeighbouringPoints :: Point -> Int -> [Point]
getNeighbouringPoints (Point x y) size = filter (inBounds size) $ [Point (x + xplus) (y + yplus) | xplus <- [-1, 0, 1], yplus <- [-1, 0, 1]]

 
getNumberOfMinesAround :: Mines -> Point -> Int -> Int
getNumberOfMinesAround mines point size = length $ filter (\p -> isMineHere mines p ) $ getNeighbouringPoints point size

uncoverSafeCells :: MinesInfo -> Mines -> Point -> Int -> MinesInfo
uncoverSafeCells minesInfo mines start size = recursivelyUncoverCells minesInfo mines [start] S.empty size

recursivelyUncoverCells :: MinesInfo -> Mines -> [Point] -> S.Set Point -> Int -> MinesInfo
recursivelyUncoverCells minesInfo mines [] seen size = minesInfo
recursivelyUncoverCells minesInfo mines (pointToVisit:rest) seen size
    | mines_around == 0 = recursivelyUncoverCells newMinesInfo mines newToVisit newSeen size
    | otherwise = recursivelyUncoverCells newMinesInfo mines rest newSeen size
    where 
          mines_around = getNumberOfMinesAround mines pointToVisit size
          newMinesInfo = changeInfo minesInfo pointToVisit (Uncovered mines_around)
          newToVisit = filter (\p -> not (p `elem` seen)) $ L.union rest (getNeighbouringPoints pointToVisit size)
          newSeen = S.insert pointToVisit seen


          
getCoveredSquares :: MinesInfo -> Int -> [Point]
getCoveredSquares minesInfo size = [Point x y | x <- [0..size-1], y <- [0..size-1], getInfo minesInfo (Point x y) == Covered]

-- mine in mineAssignment has one of 3 values: mine, not mine, unassigned
data MinePossibility = Mine | NotMine | Unassigned deriving (Show, Eq)


-- when player clicks to reveal covered square, the devil tries to come up with mine placement, that is consistent
-- with MinesInfo (information about the number of neighbouring mines for each uncovered square) and has mine at the clicked square
-- If the devil finds such placement, the player lost
-- If there is no such mine placement, that has mine at the clicked square, there is a mine placement that doesn't have mine there
-- generateDevilMines tries to find those mine placements
generateDevilMines :: MinesInfo -> Maybe Point -> Int -> Maybe [Point]
generateDevilMines minesInfo (Just whereMustBeMine) size = generateMines minesInfo intialAssignment 1
        where intialAssignment = (whereMustBeMine, Mine):(map (\p -> (p, Unassigned)) $ L.delete whereMustBeMine $ getCoveredSquares minesInfo size)
                                                                
generateDevilMines minesInfo Nothing size = generateMines minesInfo intialAssignment 0
        where intialAssignment = map (\p -> (p, Unassigned)) $ getCoveredSquares minesInfo size


checkOneSquare :: [(Point, MinePossibility)] -> Point -> Info -> Bool
checkOneSquare _ _ Covered = True
checkOneSquare partialMinesPlacement (Point x y) (Uncovered n_neighbouring) = if incomplete_assignment then True else (n_neighbouring == computed_neighbouring_mines)
    where neighbouring_possible_mines = map (\(Just mine_possibility) -> mine_possibility) $ filter (not.null) $ [L.lookup (Point (x + xplus) (y + yplus)) partialMinesPlacement | xplus <- [-1, 0, 1], yplus <- [-1, 0, 1]]
          incomplete_assignment = Unassigned `elem` neighbouring_possible_mines
          computed_neighbouring_mines = length $ filter (\mine_possibility -> mine_possibility == Mine) neighbouring_possible_mines        

-- return True if partial mine placement is consistent so far with mines info
checkPartialPlacement :: MinesInfo -> [(Point, MinePossibility)] -> Bool
checkPartialPlacement (MinesInfo info) partialMinesPlacement = all (\(p, state) -> checkOneSquare partialMinesPlacement p state) $ M.toList info

modifyNth :: Int -> (a -> a) -> [a] -> [a]
modifyNth _ _ [] = []
modifyNth n fun (x:xs)
    | n == 0 = (fun x):xs
    | otherwise = x:(modifyNth (n-1) fun xs)

-- helper function for generateDevilMines
-- given minesInfo, possitions of possibleMines
generateMines :: MinesInfo -> [(Point, MinePossibility)] -> Int -> Maybe [Point]
generateMines minesInfo minesAssignment i = if placementConsistent then (

        -- if placement is consistent and all covered squares have assigned mine value, return mine assignment
        if (i == (length minesAssignment)) then Just (map (\(p, state) -> p) $ filter (\(p, state) -> state == Mine) minesAssignment)

        -- no all covered squares have assigned mine value
        else (
            -- try assigning Mine and NotMine state to i-th covered square, which is the first Unassigned square
            let result_mine = generateMines minesInfo (modifyNth i (\(p, state) -> (p, Mine)) minesAssignment) (i+1)
                result_not_mine = generateMines minesInfo (modifyNth i (\(p, state) -> (p, NotMine)) minesAssignment) (i+1)
            in if (result_mine == Nothing) then result_not_mine else result_mine
        )
    )

    -- if current placement is not consistent there stop the current computation branch   
    else Nothing

    where placementConsistent = checkPartialPlacement minesInfo minesAssignment
          
    


printBoard :: MinesInfo -> Mines -> Int -> Bool -> IO ()
printBoard minesInfo mines size showMines = do
    -- print first two linesc
    let first_line = ("  " ++) $ unwords $ map show [0..size-1]
    putStrLn $ first_line
    putStrLn $ " " ++ (take ((length first_line ) - 1) $ repeat '-')

    printBoardLine 0 size minesInfo mines showMines


-- recursively print board line by line
printBoardLine :: Int -> Int -> MinesInfo -> Mines -> Bool -> IO ()
printBoardLine n_line size minesInfo mines showMines
    | n_line == size = do return ()
    | n_line < size = do

        -- decides what character to print depending on cell info
        let cellInfoToPrintable Covered = "*"
            cellInfoToPrintable(Uncovered neighbouring) = show neighbouring

        putStr $ (show n_line) ++ "|"
        putStrLn $ foldl1 (++) [ if showMines && (isMineHere mines (Point x n_line)) then "X " else (cellInfoToPrintable (getInfo minesInfo (Point x n_line)) ++ " ") | x <- [0..size-1] ]
        printBoardLine (n_line+1) size minesInfo mines showMines



-- uncover whole playing board
showMinePlacement :: MinesInfo -> Mines -> Int -> IO ()
showMinePlacement minesInfo mines size = printBoard newMinesInfo mines size True
    where newMinesInfo = foldl (\old_info p -> changeInfo old_info p (Uncovered $ getNumberOfMinesAround mines p size) ) minesInfo [Point x y | x <- [0..size-1], y <- [0..size-1]]


-- player has won when every uncovered square contains a mine
playerHasWonNormal :: MinesInfo -> Mines -> Int -> Bool
playerHasWonNormal minesInfo mines size = all (isMineHere mines) $ getCoveredSquares minesInfo size


-- player has won in devil mode, when every uncovered square must contain mine
playerHasWonDevil :: MinesInfo -> Int -> Bool
playerHasWonDevil minesInfo size = all (\p -> null $ generateMines minesInfo (initialAssignment minesInfo size p) 1) $ getCoveredSquares minesInfo size
    where initialAssignment minesInfo size point = (point, NotMine):(map (\p -> (p, Unassigned)) $ L.delete point $ getCoveredSquares minesInfo size)

getPlayerChoice :: IO Point
getPlayerChoice = do
    putStrLn "input space-separated x y coordinates:"
    input <- getLine
    let x:y:_ = map read $ words input :: [Int]
    -- putStrLn $ "Your input coords are " ++ (show x) ++ " " ++ (show y) 
    return $ Point x y


playGame mines minesInfo gameInfo devil_countdown = do
    let size = boardSize gameInfo
        devil_mode = devil_countdown <= 0

    printBoard minesInfo mines size False

    putStrLn $ "Devil mode: " ++ (if devil_mode then "ACTIVE!" else "INACTIVE YET")
    when (not devil_mode) ( do
        putStrLn $ "Devil mode countdown: " ++ (show devil_countdown)
        )

    choice <- getPlayerChoice

    
    let devil_mines = Mines (
            -- if devil mode is active, try to generate mine placement with mine on choice square, if it doesn't succeed, generate mine placement without mine on choice square
            let (Just mine_result) = (\(m, n) -> if (not.null $ m) then m else n) (generateDevilMines minesInfo (Just choice) size, generateDevilMines minesInfo Nothing size) in mine_result
            )   

        getMines = if devil_mode then devil_mines else mines
    
    


    let steppedOnMine = isMineHere getMines choice
    
    if steppedOnMine then (do 
        putStrLn "You lost!"
        showMinePlacement minesInfo getMines size 
        return ())
    else (do
        
        -- player did not step on mine, so uncover chosen cell and continue playing

        -- uncover
        let newMinesInfo = uncoverSafeCells minesInfo getMines choice size

        -- check for win
        let won = if devil_mode then playerHasWonDevil newMinesInfo size
            else playerHasWonNormal newMinesInfo mines size
        

        if won then do
            showMinePlacement minesInfo getMines size 
            putStrLn "You have won!!! Congratulations!"
            
        else
            -- Continue playing
            playGame getMines newMinesInfo gameInfo (devil_countdown - 1)
        )
    

main = do
    let size = 6
        n_mines = 5
        devil_countdown = 3
        gen = mkStdGen 42
        mines = placeMinesRandomly gen size n_mines emptyBoard
        minesInfo = getCoveredBoard size

    playGame mines minesInfo (GameInfo size) devil_countdown

