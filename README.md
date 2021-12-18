# Syntian

Syn'tian :
* syn means syntax and synthesis
* syntian = 3 days, which means the project is finished in 3 days. Hhhh.

## From TA
A simple framework for Syntax-Guided Synthesis problem.

The framework now supports:
* Only Int sort
* Only one synth-fun expression
* No define-fun expression

## Features
* multiqueue with keywords (num_op, depth, num_nonterminal)
* equivalance reduction (+, *, and, or) : swap
* pattern:
  * f(list, args) = if (g(head(list), args)) f_then(tail(list),h_then(args)) f_else(tail(list), h_else(args))

## Usage
