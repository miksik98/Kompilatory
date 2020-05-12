## Laboratorium 2
Zadanie polega na stworzeniu parsera języka do operacji macierzowych. Parser powinien rozponawać (akceptować) kod źródłowy w formie tokenów, bądz zglaszać bląd parsingu w przypadku nieprawidlowego wejścia. Parser powinien rozpoznawać następujące konstrukcje:
- wyrażenia binarne, w tym operacje macierzowe 'element po elemencie'
- wyrażenia relacyjne
- negację unarną
- transpozycję macierzy
- inicjalizację macierzy konkretnymi wartościami
- macierzowe funkcje specjalne
- instrukcję przypisania, w tym różne operatory przypisania
- instrukcję warunkową if-else
- pętle: while and for
- instrukcje break, continue oraz return
- instrukcję print
- instrukcje złożone
- tablice oraz ich zakresy

Przykładowo, parser powinien akceptować następujący kod:

```A = zeros(5); # create 5x5 matrix filled with zeros
B = ones(7);  # create 7x7 matrix filled with ones
I = eye(10);  # create 10x10 matrix filled with ones on diagonal and zeros elsewhere
D1 = A.+B' ;  # add element-wise A with transpose of B
D2 -= A.-B' ; # substract element-wise A with transpose of B
D3 *= A.*B' ; # multiply element-wise A with transpose of B
D4 /= A./B' ; # divide element-wise A with transpose of B
```

### Autor

*Mikołaj Sikora*
