# MorphFinder

MorphFinder è una libreria per explorare omomorfismi tra strutture algebriche finite.

Le strutture algebriche attualmente implementate sono magmi, semigruppi, monoidi, gruppi, gruppi abeliani, anelli, anelli commutativi, anelli unitari, campi.

# Background teorico
Date due strutture algebriche $(S,*)$ e $(T,\square)$, si vuole determinare l'insieme degli omomorfismi da S a T ovvero

$$
\mathcal{Hom}(S,T) := \left \{ f: S \to T\;\  \text{s.t.}\;\  \forall a,b \in S\;\ f(a*b) = f(a)\ \square\ f(b)  \right\}
$$

Si nota facilmente che $|\mathcal{Hom}(S,T)| \le |Map(S,T)| = |T|^{|S|}$, dove $Map(S,T)$ rappresenta l'insieme delle applicazioni da $S$ a $T$.

Un algoritmo che ricerca esaustivamente tutti i possibili omomorfismi da $S$ a $T$ impiegherebbe tempo esponenziale, ovvero $O(|T|^{|S|})$. Il che significa che, ad esempio, se $|S| = 100$ e $T = 500$, allora l'algoritmo richiederebbe $500^{100}$ passi.

Se riuscissimo a trovare un sistema di generatori $G$ per $S$, allora passeremmo da $O(|T|^{|S|})$ a $O(|T|^{|G|})$, con $|G| \ll |S|$. Ad esempio,se $|S| = 100$, $|G| = 1$ e $T = 500$, allora l'algoritmo richiederebbe $500^{1}$ passi.

Si vuole quindi determinare

$$
\mathcal{Hom}(G,T) := \left \{ f: S \to T\;\  \text{s.t.}\;\  \forall g_1,g_2 \in G\;\ f(g_1*g_2) = f(g_1)\ \square\ f(g_2)  \right\}
$$



## Come determino un sistema di generatori $G$ per $S$?

Per determinare un sistema di generatori $G$ per $S$ ho diverse strategie:

- Algoritmo a forza bruta: determina il sistema minimale di generatori $G$ di una struttura algebrica $S$ enumerando tutti i sottoinsiemi di $S$ in ordine di cardinalità crescente e restituendo il primo sottoinsieme $G \subseteq S$ tale che $\langle G \rangle = S$, cioè tale che la chiusura di G rispetto alle operazioni (e costanti) della struttura coincida con l’intera struttura $S$.

- Algoritmo greedy: costruisce un insieme di generatori $G$ che aggiunge iterativamente l’elemento che massimizza l’incremento della chiusura $\langle G \rangle$ fino a coprire tutta la struttura $S$, e successivamente rimuove gli elementi ridondanti ottenendo un insieme $G$ tale che $\langle G \rangle = S$ e nessun suo sottoinsieme proprio genera ancora $S$, senza però garantire che $G$ sia di cardinalità minima globale.

## Come determino $\mathcal{Hom}(S,T)$?

Ci sono alcune considerazioni importanti da fare: innanzitutto non è detto che il sistema di generatori $G$ sia chiuso rispetto all'operazione, ovvero non è detto che $\forall a,b \in G\;\ a*b \in G$. Anzi, essendo $|G| \ll |S|$ è molto probabile che $a*b \in S \setminus G$.

Per convincerci di questo consideriamo le seguenti strutture algebriche $S = (\mathbb{Z}_4, +)$ e $T = (\mathbb{Z}_3, +)$, dove $+$ denota l'usuale operazione binaria di somma. Determinato $G_S = \{ 1 \}$, si nota facilmente che  $\exists g_1, g_2 \in G\;\ \text{s.t.}\;\ g_1+g_2 \notin G$, ad esempio $\bar{1}+\bar{1} = \bar{2}$.

Dato che $G$ non è chiuso, in generale, rispetto all'operazione $*$, l'algoritmo sfrutta questa proprietà come un vantaggio per modellare il problema come un Constraint Satisfaction Problem (CSP) e propagare i vincoli.

Il motore CSP, infatti, opera in tre fasi:
1. Tracciamento della genealogia: durante il calcolo della chiusura $\langle G \rangle$ di $S$, l'algoritmo memorizza la "ricetta algebrica" di ogni elemento di $S$. Ad esempio memorizza che $\bar{2} = f(\bar{1}, \bar{1})$. 
2. Backtracking: il motore CSP tenta di un'immagine in $T$ solo agli elementi del sistema di generatori $G$. Nell'esempio, ipotizziamo un tentativo $f(\bar{1}) = a \in T$
3. Propagazione dei vincoli: sfruttando la definizione di omomorfismo di cui sopra, il valore di $f(\bar{2})$ viene individuato rapidamente accedendo alla genealogia: $f(\bar{2}) = f(\bar{1} + \bar{1}) = a + a$. Se questo calcolo genera una contraddizione con le relazioni interne della struttura, il ramo di ricerca viene scartato e viene eseguito un backtracking, riducendo drasticamente lo spazio di ricerca
4. Verifica finale: per ogni coppia $(a,b) \in \S \times S$ si controlla che l'uguaglianza $f(a*b) = f(a)\ \square\ f(b)$ sia preservata nel codominio $T$. Se il controllo ha successo, la funzione trovata è un omomorfismo valido da $S$ a $T$.