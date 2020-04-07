## Laboratorium 1
Zadanie polega na stworzeniu analizatora leksykalnego (skanera) dla prostego języka umożliwiającego obliczenia na macierzach. Analizator leksykalny powinien rozpoznawać następujące leksemy:

- operatory binare: +, -, *, /
- macierzowe operatory binarne (dla operacji element po elemencie): .+, .-, .*, ./
- operatory przypisania: =, +=, -=, *=, /=
- operatory relacyjne: <, >, <=, >=, !=, ==
- nawiasy: (,), [,], {,}
- operator zakresu: :
- transpozycja macierzy: '
- przecinek i średnik: , ;
- słowa kluczowe: if, else, for, while
- słowa kluczowe: break, continue oraz return
- słowa kluczowe: eye, zeros oraz ones
- słowa kluczowe: print
- identyfikatory (pierwszy znak identyfikatora to litera lub znak _, w kolejnych znakach mogą dodatkowo wystąpić cyfry)
- liczby całkowite
- liczby zmiennoprzecinkowe
- stringi

Dla rozpoznanych leksemów stworzony skaner powinien zwracać:
- odpowiadający token
- rozpoznany leksem
- numer linii
- Następujące znaki powinny być pomijane:
- białe znaki: spacje, tabulatory, znaki nowej linii
- komentarze: komentarze rozpoczynające się znakiem # do znaku końca linii

Przykład.
Dla następującego kodu:
```
A = zeros(5); # create 5x5 matrix filled with zeros <br>
B = ones(7);  # create 7x7 matrix filled with ones <br>
I = eye(10);  # create 10x10 matrix filled with ones on diagonal and zeros elsewhere <br>
D1 = A.+B' ;  # add element-wise A with transpose of B <br>
D2 -= A.-B' ; # substract element-wise A with transpose of B <br>
D3 \*= A.\*B' ; # multiply element-wise A with transpose of B <br>
D4 /= A./B' ; # divide element-wise A with transpose of B <br>
```
Analizator leksykalny powinien zwracać następującą sekwencję i wypisywać ją na standardowym wyjściu: <br>

(1): ID(A) <br>
(1): =(=) <br>
(1): ZEROS(zeros) <br>
(1): ((() <br>
(1): INTNUM(5) <br>
(1): )())<br>
(1): ;(;)<br>
(2): ID(B)<br>
(2): =(=)<br>
(2): ONES(ones)<br>
(2): ((()<br>
(2): INTNUM(7)<br>
(2): )())<br>
(2): ;(;)<br>
(3): ID(I)<br>
(3): =(=)<br>
(3): EYE(eye)<br>
(3): ((()<br>
(3): INTNUM(10)<br>
(3): )())<br>
(3): ;(;)<br>
(4): ID(D1)<br>
(4): =(=)<br>
(4): ID(A)<br>
(4): DOTADD(.+)<br>
(4): ID(B)<br>
(4): '(')<br>
(4): ;(;)<br>
(5): ID(D2)<br>
(5): SUBASSIGN(-=)<br>
(5): ID(A)<br>
(5): DOTSUB(.-)<br>
(5): ID(B)<br>
(5): '(')<br>
(5): ;(;)<br>
(6): ID(D3)<br>
(6): MULASSIGN(\*=)<br>
(6): ID(A)<br>
(6): DOTMUL(.*)<br>
(6): ID(B)<br>
(6): '(')<br>
(6): ;(;)<br>
(7): ID(D4)<br>
(7): DIVASSIGN(/=)<br>
(7): ID(A)<br>
(7): DOTDIV(./)<br>
(7): ID(B)<br>
(7): '(')<br>
(7): ;(;)<br>

Do rozwiązania zadania należy użyć generatora skanerów, np. generatora PLY.
Skaner powinien rozpoznawać niepoprawne leksykalnie wejście. W takim przypadku powinien zostać wypisany numer niepoprawnej linii wraz z szczegółową informacją o błędzie.

### Autor

*Mikołaj Sikora*
