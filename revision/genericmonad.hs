import Control.Monad

return () :: Maybe ()
--return 5 :: Just 5

myMapM :: Monad m => (a -> m b) -> [a] -> m [b]
myMapM f [] = return [] 
myMapM f (x:xs) = do
    y <- f x
    ys <- myMapM f xs
    return (y : ys) 

mySequence :: Monad m => [m a] -> m [a]
mySequence [] = return []
mySequence (x:xs) = do
    y <- x
    ys <- mySequence xs
    return (y:ys)

replicateM' :: Monad m => Int -> m a -> m [a]
replicateM' 0 action = return []
replicateM' x action = do
    y <- action
    ys <- replicateM' action (x - 1)
    return (y:ys)

forM' :: Monad m => [a] -> (a -> m b) -> m [b]
forM' [] f = return []
forM' (x:xs) f = do
    y <- f x
    ys <- forM' xs f
    return (y:ys)

applyNTimes :: Monad m => Int -> (a -> m a) -> a -> m a
applyNTimes 0 f x = return x
applyNTimes n f x = do
    y <- f x
    applyNTimes (n - 1) f y

filterM' :: Monad m => (a -> m Bool) -> [a] -> m [a]
filterM' p [] = return []
filterM' p (x:xs) = do
    y <- p x
    ys <- filterM' p xs
    if y then return (x:ys)
    else return ys

foldM' :: Monad m => (b -> a -> m b) -> b -> [a] -> m b
foldM' f acc [] = return acc
foldM' f acc (x:xs) = do
    newAcc <- f acc x
    foldM' f newAcc xs