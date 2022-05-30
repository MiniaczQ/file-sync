# Konfiguracja

Poprzez plik JSON.
- pattern - Wzór prawa dostępu do plików jako 9-literowy string.  
  `rwxrwxrwx` - pełny dostęp dla wszystkich  
  `rwx------` - pełny dostęp tylko dla właściciela  
  `rwxr__r__` - pełny dostęp dla właściciela, odczyt dla każdego, inne nieistotne

- symbols - Zabronione symbole w nazwach plików, jako pojedynczy string.  
  `$` - Zabraniamy tylko `$`  
  `#$%^` - Zabraniamy wszystkich 4. znaków  
  Uwaga:  
  Znaki te obejmują __całą__ nazwę pliku, razem z rozszerzeniem.  
  Powodem na to jest możliwość zagnieżdżania rozszerzeń, np. `.tar.gz`.

- substitute - Znak zastępczy dla zabronionych symboli, jako 1-znakowy string.  
  `_` - Zabronione znaki zastąpimy `_`

- endings - Zakończenia nazw sugerujące, że plik jest tymczasowy, jako lista stringów.  
  `.temp`  
  `.tmp`  
  `~`

Plik konfiguracyjny można podać we fladze `--config <ścieżka>`.
# Przykłady

## Help
`python3 manage.py -h`

## Przekopiowanie brakujących plików z katalogu Y i Z do X bez interakcji
`python3 manage.py X -s Y -s Z -c cp-all`

### Usunięcie plików pustych, tymczasowych oraz plików identycznych treścią lub nazwą z katalogu X. (z interakcją, w tej kolejności)
`python3 manage.py X -e -t -n -d`
