### struktura
_____________

- config/ #pliki konfikuracyjne, stałe itp.
- bin/ #moduły, kod źródłowy
    - \_\_init__.py
    - simulation/ #właściwy program
        -  \_\_init__.py
        - numerical/ #Numeryka
            - \_\_init__.py
            - positions.py
            - velocity.py
            - force.py
            - energy.py
        - visualization/ #reprezentacja wizualna
            - \_\_init__.py
            - visual.py 
    - gui/ #jakies ładne gui w Qt
        - \_\_init__.py
        - ...
- doc/ #dokumetacja
- src/ # ew coś kompilowalnego jakby python za wolno liczył, Fortran? XD/
- examples/
- README.md
- LICENSE
- AUTHORS
- setup.py #plik instalacyjny albo run.sh do odpalania
- .gitignore