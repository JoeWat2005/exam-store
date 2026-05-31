import Data.List (transpose)

data Pair a = Pair a a

instance Functor Pair where
    fmap f (Pair x y) = Pair (f x) (f y)

data Tree a = Leaf | Node (Tree a) a (Tree a)

instance Functor Tree where
    fmap f Leaf = Leaf
    fmap f (Node left x right) =
        Node (fmap f left) (f x) (fmap f right)

data Rose a = Rose a [Rose a]

instance Functor Rose where
    fmap f (Rose x children) =
        Rose (f x) (map (fmap f) children)

data MyEither e a = MyLeft e | MyRight a

instance Functor (MyEither e) where
    fmap f (MyLeft x) = MyLeft x
    fmap f (MyRight x) = MyRight (f x)

fmap id = id
fmap (g . h) = fmap g . fmap h

data Identity a = Identity a

instance Applicative Identity where
    pure x = Identity x
    Identity f <*> Identity x = Identity (f x)

instance Monad Identity where
    return x = Identity x
    Identity x >>= f = f x

myTranspose :: [[a]] -> [[a]]
myTranspose [] = []
myTranspose ([]:_) = []
myTranspose rows =
    map head rows : myTranspose (map tail rows)

rowSums :: Num a => [[a]] -> [a]
rowSums rows = map sum rows

colSums :: Num a => [[a]] -> [a]
colSums rows = map sum (myTranspose rows)

diag :: [[a]] -> [a]
diag xs = zipWith (!!) xs [0..]

antiDiag :: [[a]] -> [a]
antiDiag xs = zipWith (!!) xs (reverse [0 .. length xs - 1])

isMagicSquare :: [[Int]] -> Bool
isMagicSquare [] = False
isMagicSquare xs = 
    let target = sum (head xs)
        rowsOk = all (== target) (rowSums xs)
        colsOk = all (== target) (colSums xs)
        diagsOk = sum (diag xs) == target && sum (antiDiag xs) == target
    in rowsOk && colsOk && diagsOk

allRowsUnique :: Eq a => [[a]] -> Bool
allRowsUnique [] = True
allRowsUnique (x:xs) =
    notElem x xs && allRowsUnique xs