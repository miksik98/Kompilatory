## Laboratorium 2
Zadanie polega na stworzeniu i wypisaniu abstrakcyjnego drzewa składni 
(ang. abstract syntax tree, AST). Drzewo składni powinno uwzględniać 
w swoich węzłach następujące konstrukcje:
- wyrażenia binarne
- wyrażenia relacyjne
- instrukcję przypisania
- instrukcję warunkową if-else
- pętle: while and for
- instrukcje break, continue oraz return
- instrukcję print
- instrukcje złożone
- tablice oraz ich zakresy

Przykładowo, dla poniższego kodu:

```
Input:
A = zeros(5); # create 5x5 matrix filled with zeros
D = A.+B' ;   # add element-wise A with transpose of B

for j = 1:10 
    print j;
```
translator powinien stworzyć odpowiadające mu drzewo składni (AST) 
oraz wypisać jego tekstową reprezentację na standardowym wyjściu:

```
Output:
=
|  A
|  zeros
|  |  5
=
|  D
|  .+
|  |  A
|  |  TRANSPOSE
|  |  |  B
FOR
|  j
|  RANGE
|  |  1
|  |  10
|  PRINT
|  |  j
```
### Autor

*Mikołaj Sikora*