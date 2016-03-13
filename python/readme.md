# LILO compiler

Lilo is a minimalistic language that compiles in python. It has dynamic typing, a box (variable) supporting integers, floats and strings.
It is able to perform arithmetic operations +,-,/,* as well as logical ones (<, >, <=, >=, =, !=, &&, ||).

Declaration is in place in order to make everything explicit.
Assignment is very intuitive.
```
box bar <- 123.
box foo <- 'a string'.
box baz1 <- 323, baz2 <- 'another string'.
```

Printing is also straightforward
```
say 'hello world'.

box bar <- 123, foo = 'hello'.
say bar.
say foo.
```

It has a single loop structure, namely while
```
while (bar = 12)
bar <- bar + 1.
end
```
