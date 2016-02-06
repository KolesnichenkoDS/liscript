# LiScript
Lisp dialect written in Python

## Installation

```bash
sudo pip install liscript
# or #
sudo pip3 install liscript
```

## Usage
```bash
lirepl            # open liscript repl
lirun <filename>  # run liscript code
```

## Overview

### Syntax

```clojure
;; Atoms
x   ; will return the value of variable `x'

;; Getters
:x  ; will return function that returns attribute `x' of its argument

;; Numbers
1
1.5
-1

;; Strings
"Hello, world!"

;; Expressions (lists)
(+ 1 2)   ; apply function `+' to 1 and 2; will return 3

;; Quoted lists
'(1 (+ 1 1) (+ 1 1 1))  ; elements are evaluated when the list is initialized; will return '(1 2 3)

;; Lazy lists
[1 (+ 1 1) (+ 1 1 1)]   ; elements are evaluated manually; will return [1 (+ 1 1) (+ 1 1 1)]  

;; Dictionaries
{:x 1
 :y 2
 :z 3}
```

### Standard functions

#### let, modify
```clojure
> (let [x] 0)
> x
  -> 0
> (modify [x] [+ 1])  ; same as `(let [x] (+ 1 x))'
> x
  -> 1
```

#### fn, def
```clojure
> (def [sqr x] [* x x])   ; same as `(let [sqr] (fn [x] [* x x]))'
> (sqr 9)
  -> 81
```

#### class, new
```clojure
> (class [Point] {:constructor (fn [self x y] [set self [x] x] [set self [y] y])})
> (let [p] (new Point 3 5))
> (:x p)
  -> 3
> (:y p)
  -> 5
```

#### +, -, *, /
```clojure
> (+ 1 2)
  -> 3
> (- 5 1)
  -> 4
> (* 2 3)
  -> 6
> (/ 5 2)
  -> 2.5
```

#### >, <, =, !=
```clojure
> (> 1 2)
  -> #f
> (< 5 1)
  -> #f
> (= 2 2)
  -> #t
> (!= 5 2)
  -> #t
```

#### if, unless, case
```clojure
> (if #t [say "true"] [say "false"])
true
> (unless #t [say "true"] [say "false"])
false
> (case [= 1 0] [say "1 = 0"] [> 1 0] [say "1 > 0"] otherwise [say "1 < 0"])
1 > 0
```

#### list, cons
```clojure
> (list 1 2 3)
  -> '(1 2 3)
> (cons 1 '(2 3))
  -> '(1 2 3)
```

#### head, tail
```clojure
> (head '(1 2 3))
  -> 1
> (tail '(1 2 3))
  -> '(2 3)
```

#### push
```clojure
> (push 3 '(1 2))
  -> '(1 2 3)
```

#### !!, slice
```clojure
> (!! '(1 2 3) 1)
  -> 2
> (slice '(1 2 3 4 5 6 7 8 9 10) 5)
  -> '(6 7 8 9 10)
> (slice '(1 2 3 4 5 6 7 8 9 10) 1 5)
  -> '(2 3 4 5)
```

#### eval-list
```clojure
> (eval-list '(+ 1 2))
  -> 3
> (eval-list [* 2 2])
  -> 4
```

#### say, read
```clojure
> (read)
user input
  -> "user input"
> (say "hello, world")
hello, world
```

#### exit
```clojure
> (exit)  ; exit with code 0
```
