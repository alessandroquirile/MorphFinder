# MorphFinder

MorphFinder è una libreria per trovare e classificare omomorfismi tra strutture algebriche finite, tra cui: magmi,
semigruppi, monoidi, gruppi, gruppi abeliani, anelli, anelli commutativi, anelli unitari, campi.

## Background Teorico

Per una spiegazione approfondita dei fondamenti matematici, dell'algoritmo CSP di ricerca e della classificazione degli
omomorfismi, consulta il file [THEORY.md](THEORY.md).

## Installazione

```bash
# Crea e attiva un ambiente virtuale (consigliato)
python3 -m venv .venv
source .venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt
```

## Configurazione

La strategia per trovare un sistema di generatori per una data struttura algebrica può essere specificata nel file
`config.yaml`:

```yaml
strategy: greedy # o brute_force
```

## Esempio di Utilizzo

Puoi eseguire l'esempio fornito nel file `main.py` per vedere MorphFinder in azione:

```bash
python main.py
```

Questo script definisce due semplici monoidi ($\mathbb{Z}_4, +, \bar{0}$) e ($\mathbb{Z}_3, +, \bar{0}$) e cerca
omomorfismi tra di essi. L'output atteso sarà:

```text
Found 1 homomorphism(s) between given structures:
f: {0, 1, 2, 3} → {0, 1, 2} | 0 ↦ 0, 1 ↦ 0, 2 ↦ 0, 3 ↦ 0 | Properties: Trivial | Ker(f): {0, 1, 2, 3} | Im(f): {0}
```

## Esecuzione dei Test

Puoi eseguire la suite di test utilizzando `pytest`:

```bash
pytest
```
