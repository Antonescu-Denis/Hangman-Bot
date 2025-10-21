## Descriere
Acest proiect implementează un **bot de spânzurătoare** pentru cuvinte românești
Botul ghicește litere pe baza unor reguli simple:
- diferențiere între vocale și consoane, schimband intre vocale si consoane pentru ghicire
- identificarea diftongilor și hiaturilor (sanse mari de success, dar nu garantate)
- cazuri speciale pentru literele sau combinatii specifice de litere
- schimbarea strategiei după mai multe încercări eșuate consecutive

Rezultatul: botul rezolvă automat lista data de cuvinte in folderul "data" și salvează rezultatele în "results/results.txt"

---

## Structura Proiect
```
├── src/
│   └── hangman.py
├── data/
│   └── words.txt
├── results/
│   ├── results.txt
│   └── errors.txt
├── docs/
├── requirements.txt
└── README.md
```

---

## Cerinte
- Python **3.6+**

---

## Format fișier de input
Fiecare linie din words.txt trebuie să fie de forma urmatoare
```
Exemplu:
1;**a*i**i;omagiali
```

---

## Format fișier de output `results.txt`:  
```
game_id, attempts, solution, status, guessed_sequence
```
Exemplu:
1, 12, omagiali, OK, omagil
```

La final, este afișat și numărul total de încercări

---

## Ghid Rulare
```
1. Asigură-te că ești în folderul principal al proiectului.
2. Asigură-te că fisierul "data\words.txt" exista si este valid
3a. Rulează cu double click:
   src/hangman.py
sau, din command prompt:
3b. {locatia folderului de proiect}\src\hangman.py
```

Botul va:
    - citi cuvintele din data/words.txt
    - încerca să le rezolve
    - scrie rezultatele în results/results.txt
    - nota erorile în results/errors.txt