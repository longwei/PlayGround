

Overview
===
1. tokenized string into tokens
2. parsing the tokens into AST, which is intermediate representation
3. eval the each node of AST and emit the statement

lex
===
This part is using regex to slit the string
see lex or flex as example, basically:

* a list of token and their regex
* the re state machine will eat char by char and split out the first match as a token
* the end result will be a stream of (value, tag) pairs

parsing
===
each individual type node will have it own parser(which is a class type). This parser will consume some of the tokens and output a sub-AST and the remaining token stream, recursively apply parser to the tokens stream will result the final AST.

parser combinator is a higher-order function that accpect sveral parser as input and return a new parser as output

```
if 1 < 2 then x = 3 else x = 4 end
IfStatement(RelopBexp('<', IntAexp(1), IntAexp(2)),
            AssignStatement('x', IntAexp(3)),
            AssignStatement('x', IntAexp(4)))
```


combinator helper to glue AST:

* concat: (left, right)
* alternative: 	left ? left : right
* opt: parser ? result : None
* rep: loop
* process: if parser? lambda(result.value)
* lazy, evaluated till applied
* phrase, take a parser, applied all token
* Exp

AST class:

* arithmetic
  * integer literal
  * variables
  * binary operation
* boolean expression
  * relatonal expression
  * And
  * Or
  * Not 
* statments
  * assignment
  * compound
  * conditional
  * loop      
 
 
* primitives parser
* arithmetic express
  * we dont want them to be evaluated right away because some parser haven't defined yet
  * () grouping

```
4 * a + b / 2 - (6 + c)
E0(4) * E0(a) + E0(b) / E0(2) - E0(6+c)
E1(4*a) + E1(b/2) - E1(6+c)
E2((4*a)+(b/2)-(6+c))
```

REF:
http://jayconrod.com/posts/38/a-simple-interpreter-from-scratch-in-python-part-1