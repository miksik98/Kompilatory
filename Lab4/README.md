## Laboratorium 4
Zadanie jest kontynuacją poprzedniego zadania.
Zadanie polega na stworzeniu analizatora błędów semantycznych.

Analizator semantyczny powinien wykrywać następujące błędy semantyczne:
- inicjalizacja macierzy przy użyciu wektorów o różnych rozmiarach
- dla danej operacji binarnej użycie stałej, skalara, wektora lub macierzy o niekompatybilnych typach lub rozmiarze
- użycie funkcji inicjalizujących (funkcje eye, zeros, ones) z niepoprawnymi parametrami
- użycie instrukcji break lub continue poza pętlą

Analiza błędów semantycznych nie powinna być przerywana po
napotkaniu pierwszego błędu, lecz wykrywać jak największą liczbę błędów. 
Z każdym błędem powinna być skojarzona informacja o miejscu wystąpienia błędu (nr linii, ew. numer kolumny).
### Autor

*Mikołaj Sikora*