# MorphFinder

MorphFinder è una libreria per esplorare omomorfismi tra strutture algebriche finite.

Le strutture algebriche attualmente implementate sono magmi, semigruppi, monoidi, gruppi, gruppi abeliani, anelli, anelli commutativi, anelli unitari, campi.

# Background teorico
Date due strutture algebriche $(S,*)$ e $(T,\square)$, si vuole determinare l'insieme degli omomorfismi da S a T ovvero

$$
\mathcal{Hom}(S,T) := \lbrace f: S \to T\ \text{s.t.}\  \forall a,b \in S\ f(a*b) = f(a)\ \square\ f(b) \rbrace
$$

Si nota facilmente che $|\mathcal{Hom}(S,T)| \le |Map(S,T)| = |T|^{|S|}$, dove $Map(S,T)$ rappresenta l'insieme delle applicazioni da $S$ a $T$.

Un algoritmo che ricerca esaustivamente tutti i possibili omomorfismi da $S$ a $T$ impiegherebbe tempo esponenziale, ovvero $O(|T|^{|S|})$. Se riuscissimo a trovare un sistema di generatori $G$ per $S$, allora passeremmo da $O(|T|^{|S|})$ a $O(|T|^{|G|})$, con $|G| \ll |S|$.

Si vuole quindi determinare

$$
\mathcal{Hom}(G,T) := \lbrace f: S \to T\  \text{s.t.}\ \forall g_1,g_2 \in G\ f(g_1*g_2) = f(g_1)\ \square\ f(g_2) \rbrace
$$



## Come determino un sistema di generatori $G$ per $S$?

Per determinare un sistema di generatori $G$ per $S$ ho diverse strategie:

- Algoritmo a forza bruta: determina il sistema minimale di generatori $G$ di una struttura algebrica $S$ enumerando tutti i sottoinsiemi di $S$ in ordine di cardinalità crescente e restituendo il primo sottoinsieme $G \subseteq S$ tale che $\langle G \rangle = S$, cioè tale che la chiusura di G rispetto alle operazioni (e costanti) della struttura coincida con l’intera struttura $S$. Garantisce di trovare l'insieme di cardinalità minima globale.

- Algoritmo greedy: costruisce un insieme di generatori $G$ che aggiunge iterativamente l’elemento che massimizza l’incremento della chiusura $\langle G \rangle$ fino a coprire tutta la struttura $S$, e successivamente rimuove gli elementi ridondanti ottenendo un insieme $G$ tale che $\langle G \rangle = S$ e nessun suo sottoinsieme proprio genera ancora $S$, senza però garantire che $G$ sia di cardinalità minima globale.

## Come determino $\mathcal{Hom}(S,T)$?

Ci sono alcune considerazioni importanti da fare: innanzitutto non è detto che il sistema di generatori $G$ sia chiuso rispetto all'operazione, ovvero non è detto che $\forall a,b \in G\ a * b \in G$. Anzi, essendo $|G| \ll |S|$ è molto probabile che $a * b \in S \setminus G$.

Per convincerci di questo consideriamo, senza perdita di generalità, i seguenti monoidi $S = (\mathbb{Z}_4, +, \bar{0})$ e $T = (\mathbb{Z}_3, +, \bar{0})$, dove $+: S \times S \to S$ denota l'usuale operazione binaria di somma. Determinato $G_S = \lbrace \bar{1} \rbrace$, si nota facilmente che  $\exists g_1, g_2 \in G\ \text{s.t.}\ g_1+g_2 \notin G$, ad esempio $\bar{1}+\bar{1} = \bar{2}$. La non-chiusura di $G$ consente all'algoritmo di modellare il problema come un Constraint Satisfaction Problem (CSP) e propagare i vincoli.  Il motore CSP, infatti, opera in tre fasi:

### Funzione di genealogia
L'algoritmo costruisce una funzione $h: S \setminus G \to S \times S$ per tracciare la "genealogia" di ciascun elemento di $S$ (generatori esclusi).

Riprendendo l'esempio precedente, si ha che $h(\bar{0}) = (\bar{3}, \bar{1})$, $h(\bar{2})= (\bar{1}, \bar{1})$, $h(\bar{3}) = (\bar{2}, \bar{1})$, notando che non è necessario calcolare $h(\bar{1})$ essendo $\bar{1} \in G$.

La seguente Figura mostra la mappa di genealogia:

![Mappa della Genealogia h](assets/history.png)


### Backtracking e propagazione dei vincoli
Per costruire $\mathcal{Hom}(G,T)$, l'algoritmo inizia assegnando casualmente un valore in $T$ per ogni generatore in $G$. A questo punto entra in gioco la funzione $h$. L'algoritmo usa questa funzione come "ricettario" per costruire le immagini degli altri elementi di $S$, senza dover fare ulteriori tentativi alla cieca. Costruito un possibile omomorfismo $f$, si verifica che esso sia effettivamente un omomorfismo (ovvero che soddisfi la definizione e che preservi le eventuali proprietà intrinseche delle strutture algebriche fornite, come zero ed unità). Se si ottiene una contraddizione, scarto $f$ dai possibili omomorfismi. Se il controllo ha successo, la funzione trovata è un omomorfismo valido da $S$ a $T$.

Riprendendo l'esempio precedente, l'algoritmo assegna arbitrariamente un elemento $b \in \mathbb{Z}_4$ a $g \in G$.

Caso per $f(\bar{1}) = \bar{1}$. Si ha che:

$h(\bar{2}) = (\bar{1}, \bar{1}) \implies f(\bar{2}) = f(\bar{1}) +_T f(\bar{1}) = \bar{1} + \bar{1} = \bar{2}$
$h(\bar{3}) = (\bar{2}, \bar{1}) \implies f(\bar{3}) = f(\bar{2}) +_T f(\bar{1}) = \bar{2} + \bar{1} = \bar{0}$
$h(\bar{0}) = (\bar{3}, \bar{1}) \implies f(\bar{0}) = f(\bar{3}) +_T f(\bar{1}) = \bar{0} + \bar{1} = \bar{1}$

Quindi l'applicazione $f$ costruita è 

$$f: \mathbb{Z}_4 \to \mathbb{Z}_3$$
$$\bar{0} \mapsto \bar{1}$$
$$\bar{1} \mapsto \bar{2}$$
$$\bar{2} \mapsto \bar{1}$$
$$\bar{3} \mapsto \bar{0}$$

La funzione $f$ soddisfa la definizione di omomorfismo. Ma essendo le due strutture date dei monoidi, occorre che $f$ preservi l'esistenza dell'elemento neutro ovvero $f(\varepsilon_S) = \varepsilon_T \iff f(\bar{0}) = \bar{0}$ che genera una contraddizione. Quindi $f \notin \mathcal{Hom}(S,T)$ 

A questo punto l'algoritmo esegue un backtracking e prova un'altra assegnazione possibile. Ad esempio, $f(\bar{1}) = \bar{0}$.

Caso per $f(\bar{1}) = \bar{0}$. Si ha che:

$h(\bar{2}) = (\bar{1}, \bar{1}) \implies f(\bar{2}) = f(\bar{1}) +_T f(\bar{1}) = \bar{0} + \bar{0} = \bar{0}$
$h(\bar{3}) = (\bar{2}, \bar{1}) \implies f(\bar{3}) = f(\bar{2}) +_T f(\bar{1}) = \bar{0} + \bar{0} = \bar{0}$
$h(\bar{0}) = (\bar{3}, \bar{1}) \implies f(\bar{0}) = f(\bar{3}) +_T f(\bar{1}) = \bar{0} + \bar{0} = \bar{0}$

Quindi l'applicazione $f$ costruita è 

$$f: \bar{a} \in \mathbb{Z}_4 \to \bar{0} \in \mathbb{Z}_3$$

La funzione $f$ soddisfa la definizione di omomorfismo. Come prima, verifichiamo se $f$ preservi l'esistenza dell'elemento neutro ovvero $f(\varepsilon_S) = \varepsilon_T \iff f(\bar{0}) = \bar{0}$ vero. Quindi $f \in \mathcal{Hom}(S,T)$. In particolare si tratta di un omomorfismo banale. 

Proseguiamo con l'ultima assegnazione possibile, ovvero $f(\bar{1}) = \bar{2}$. Similmente a quanto fatto prima si ottiene la seguente applicazione:

$$f: \mathbb{Z}_4 \to \mathbb{Z}_3$$
$$\bar{0} \mapsto \bar{2}$$
$$\bar{1} \mapsto \bar{2}$$
$$\bar{2} \mapsto \bar{1}$$
$$\bar{3} \mapsto \bar{0}$$

Verifico se tale applicazione preserva l'elemento neutro ovvero $f(\varepsilon_S) = \varepsilon_T \iff f(\bar{0}) = \bar{0}$ falso. Quindi $f \notin \mathcal{Hom}(S,T)$.

$$
\therefore \mathcal{Hom}(S,T) = \lbrace f: \bar{a} \in \mathbb{Z}_4 \mapsto \bar{0} \in \mathbb{Z}_3 \rbrace
$$

La seguente Figura mostra l'albero di computazione per l'esempio fornito:

![Backtracking](assets/backtracking.png)

Si noti che grazie alla propagazione dei vincoli, l'algoritmo evita l'esplorazione esaustiva dell'intero spazio delle applicazioni $(|T|^{|S|} = 3^4 = 81)$. Limitando i tentativi alla sola scelta dei generatori $(|T|^{|G|} = 3$ il carico computazionale viene abbattuto, rendendo trattabili anche strutture algebriche di dimensioni superiori."
