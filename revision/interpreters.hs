import Data.Maybe
import Control.Monad

data Expr = Lit Int | Add Expr Expr | Mul Expr Expr | Sub Expr Expr | Div Expr Expr
| Var String | Let String Expr Expr
deriving Show

type Env = [(String, Int)]

eval :: Expr -> Int
eval (Lit x) = x
eval (Add x y) = eval x + eval y
eval (Mul x y) = eval x * eval y
eval (Sub x y) = eval x - eval y

safeEval :: Expr -> Maybe Int
safeEval (Lit x) = return x

safeEval (Add x y) = do
    a <- safeEval x
    b <- safeEval y
    return (a + b)

safeEval (Mul x y) = do
    a <- safeEval x
    b <- safeEval y
    return (a * b)

safeEval (Sub x y) = do
    a <- safeEval x
    b <- safeEval y
    return (a - b)

safeEval (Div x y) = do
    a <- safeEval x
    b <- safeEval y
    if b == 0 then Nothing
    else return (a `div` b)

envEval :: Env -> Expr -> Maybe Int

envEval env (Add x y) = do
    a <- envEval env x
    b <- envEval env y
    return (a + b)

envEval env (Mul x y) = do
    a <- envEval env x
    b <- envEval env y
    return (a * b)

envEval env (Sub x y) = do
    a <- envEval env x
    b <- envEval env y
    return (a - b)

envEval env (Div x y) = do
    a <- envEval env x
    b <- envEval env y
    if b == 0 then Nothing
    else return (a `div` b)

envEval env (Var name) =
    lookup name env

envEval env (Let name expr body) = do
    value <- envEval env expr
    envEval ((name, value) : env) body

data Source = SLit Int | SVar String | SAdd Source Source | SSub Source Source
| SNeg Source | SIf Source Source Source

data Target = TLit Int | TVar String | TAdd Target Target | TMul Target Target

translate :: Source -> Target
translate (SLit n) = TLit n
translate (SVar x) = Tvar x
translate (SAdd a b) = TAdd (translate a) (translate b)

translate (SSub a b) = TAdd (translate a) (TMul (TLit (-1)) (translate b))

translate (SNeg a) = TMul (TLit (-1)) (translate a)

translate (SIf c t e) = TAdd
                            (TMul (translate c) (translate t))
                            (TMul
                                (TAdd (TLit 1) (TMul (TLit (-1)) (translate c)))
                                (translate e))

vars :: Target -> [String]
vars (TLit _) = []
vars (TVar x) = [x]
vars (TAdd a b) = vars a ++ vars b
vars (TMul a b) = vars a ++ vars b