tick :: State int ()
tick = do
    x<-get
    put (x + 1)

tickN :: Int -> State Int ()
tick x = do
    n<-get
    put(x + n)

fresh :: State Int Int 
fresh = do
    n<-get
    put(n + 1)
    return(n)

freshN :: Int -> State Int [Int]
freshN 0 = return []
freshN n = do
    x <- fresh
    xs <- freshN (n - 1)
    return (x : xs)

data Tree a
    = Leaf
    | Node (Tree a) a (Tree a)
    deriving (Show, Eq)
    
label :: Tree a -> State Int (Tree (Int, a))
label Leaf = return Leaf
label (Node left x right) = do
    labelledLeft <- label left
    n <- fresh
    labelledRight <- label right
    return (Node labelledLeft (n, x) labelledRight)
    
labelTree :: Tree a -> Tree (Int, a)
labelTree tree =  evalState (label tree) 0