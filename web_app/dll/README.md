## Jak to działa?

Mamy nasz plik `custom_function.pyx` w folderze dll, który zawiera implementacje funkcji. Jest to plik Cythona, czyli C-podobna implementacja Pythona, która jest kompilowana do C.
Używamy jej, ponieważ Python jest interpretowanym językiem i nie wiem jak można z jego kodu zrobić DLL, no a używając kompilowanych języków jest to proste.

## Jak dodać customową funkcję?

Otwieramy plik `custom_function.pyx` i zmieniamy metodę `fobj`. Teraz musimy zrekompilować ten plik (Musimy go rekompilować, za każdym razem gdy zmieniamy ten plik).
Jeżeli już istnieje plik `\*.pyd` w tym katalogu, to trzeba go manualnie usunąć, bo inaczej się nie skompiluje (Chciałem to usuwać skryptem, ale permisje na
windowsie to żart i nie wiem jak to zrobić).
W folderze dll wpisujemy

```bash
  python setup.py build_ext --inplace
```

Dostajemy `custom_functioon.\*.pyd`, który jest naszym modułem, który będziemy importować

Cały kod ładowania DLL'a jest w pliku `get_function_obj.py` w funkcji `get_function_obj`
