- przejście po drzewie plików

- parametry (plik konfiguracyjny)
    - sugerowana zawartość atrybutów (rw-r--r--)
    - znaki kłopotniwe (", ', ., :, ;, *, ?, $, #, |, \\)
    - znak substytut (_ lub -)
    - rozszerzenia plików tymczasowych (*~, *.tmp)

- wyszukiwanie
        - [c]ontent - plików o identycznej zawartości (hash => porównanie całości)
        - [e]mpty - plików pustych
        - [n]ame - plików o tej samej nazwie
        - [t]emporary - plików tymczasowych
        - [s]ymbols - plików o nazwach z kłopotliwymi znakami
    - [r]ights - plików o dziwnych atrybutach (rwxrwxrwx)

- akcje
    - plik jest w Y, ale nie w X - przenieś
    - złe atrybuty - zmień
    - kłopotliwa nazwa - zmień
    - pliki tymczasowe, puste, duplikaty - usuń
    - pozostaw bez zmian - nic
    - starsze wersje (nazwa) - nadpisz nowymi
    - nowsze wersje (zawartość) - nadpisz starszymi

- flagi
    - [a]ll - przytakni na wszystko