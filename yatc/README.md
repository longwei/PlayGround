

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
each individual type node will have it own parser. This parser will consume some of the tokens and output a sub-AST and the remaining token stream, recursively apply parser to the tokens stream will result the final AST

1 + 2

parser = (con(con(INT(1) +) INT(2) ))