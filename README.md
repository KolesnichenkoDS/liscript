# LiScript
Lisp dialect written in Python

## Installation

```bash
sudo pip3 install liscript  # or just `pip'
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
