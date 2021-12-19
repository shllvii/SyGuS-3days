# Syntian

Syn'tian :
* syn means syntax and synthesis;
* syntian sounds like 'san tian', which means the project is finished in 3 days...

We have to acknowledge that we fail to implement a general solver for all the testbenches. We combine multiple case-specific solvers to pass the open cases, and we feel sorry about that. (We hope that we could get some score for our efforts. >_<)

## Features

### Top-down search
We extend the given top-down search from TA with the following features:
* BFS with a priority queue. We use the function `numOps * 4 + numNonTermial * 2 + depth` for priority evaluation. 
  * See `src/bfsqueue.py` for implementation.
* Preprocessing. Remove the excess rules from the production sets. For example, remove ">=" rule if there exists "<=" for the same non-terminal symbol.
  * See `src/preprocess.py` for implementation.
* Equivalence reduction. We adopt a hash strategy and remove the equivalent candidates. In general, we flatten associative operations and sort the operands of a commutative operation. For examples, `(+ b (+ a c))` is flattened to `(+ b a c)`, and then sorted to `(+ a b c)` according to the hash values `h(a)<h(b)<h(c)`. The hash strategy works in a recursive manner. Only candidiates with a hash value which has never appeared would be inserted to the queue.
  * See `src/optimize.py` for implementation.
* Strategy check. During the hash evaluation, the strategy is abandoned if it contains any invalid expressions, such as `ite cond x x`. The check procedure depends on our hash method.
  * See `src/optimize.py` for implementation.

The entry of the top-down search is in `src/search.py`. This method passs `max2.sl, three.sl, tutorial.sl` for less than 1s (`tutorial.sl` for 0.910137s).
### Pattern-based search

We find it really hard to optimize our search algorithm to get good performance for `maxk.sl` and `array_search_k.sl` cases. Their solutions need much `ite cond then else` statements, which result in a pretty large search space. Thus we manually design a generation "pattern" for list enumeration cases. The idea origins from the functional programming and domain-specific languages (DSL, such as Halide, Chisel, and etc.).

To be specific, we design a function `generate`, which takes a tuple `(ls, args, cond, f_then, f_else, bound)`, and generates a solution:
* `ls` represents the list, such as `[x2, x3, x4, x5]` for `max5.sl` and `[(x1, 0), (x2, 1), (x3, 2)` for `array_search_3.sl`;
* `args` represents the initial arguments for the enumeration, such as `(x1)` for `max5.sl` and `(k1, 4)` for `array_search_3.sl`;
* `cond` represents the condition generator for the `ite` of each enumeration. It consists of operations and elements in `head(ls)` (which may be a tuple) and arguments. For example, the `cond` is `lambda hd, args: ['<=', hd, args[0]]` for `maxk.sl` cases.
* `f_then` and `f_else` determines the `then of the `ite`, 

## From TA
A simple framework for Syntax-Guided Synthesis problem.

The framework now supports:
* Only Int sort
* Only one synth-fun expression
* No define-fun expression

## Usage
