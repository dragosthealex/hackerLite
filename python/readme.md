# LILO compiler

Lilo is a minimalistic language that compiles in python. It has dynamic typing, a box (variable) supporting integers, floats and strings.
It is able to perform arithmetic operations +,-,/,*,% as well as logical ones (<, >, <=, >=, =, !=, &&, ||).

Declaration is in place in order to make everything explicit.
Assignment is very intuitive.
```
box bar <- 123.
box foo <- 'a string'.
box baz1 <- 323, baz2 <- 'another string'.
```
Before every assignment statement or compund assingment statement keyword **box** is mandatory.
After every statement the statement-ending symbol **.** is also needed.

Printing is also straightforward
```
say 'hello world'.

box bar <- 123, foo = 'hello'.
say bar.
say foo.
```
There is no support for reading input, as it is primarily designed for basic programming lessons in a mobile environment.
We plan to add support for this in the future.

**Lilo** treats new lines, tabs and blanks as white spaces, to make it easy to write even on old feature phones.

After any block of instructions (if, while, functions), the keyword **end** is mandatory, to mark the end of the block.
It doesn't use curly braces or indentation as they are harder to write on the mobile phone.

It has a single loop structure, namely while
```
box bar <- 2.
while (bar < 12)
bar <- bar + 1.
end
```

The if else structure is exactly as expected: 
```
box foo <-2, bar <-4.
if foo < bar
say 'foo is smaller than bar'
else
say 'foo is bigger than bar'
end
```

###Functions
Basic function implementation. Functions are declared with **dog** keyword (got it? you call a dog to bring something).
They can have any number of parameters. There is not yet any support for default parameters.
```
/* Prime number implementation */
dog prime (number)
  box d <- 2.
  while number % d = 1 && d <= number/2
    d <- d + 1.
  end
  say 'current number:'.
  say number.
  if (d % 2 != 0)
    say 'the number is prime'.
  else
    say 'the number is not prime'.
  end
end

call prime(20).
call prime(5).
```

### To do:
- String concatenation
- String + int concatenation
- Default types
- Read from file
- Cmd line parameters
- Lists
- Dictionaries
