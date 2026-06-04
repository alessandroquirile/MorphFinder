# Theory: MorphFinder

MorphFinder is a library designed for the discovery and classification of homomorphisms between finite algebraic
structures, including magmas, semigroups, monoids, groups, abelian groups, rings, commutative rings, unital rings, and
fields.

## Theoretical Background

Given two algebraic structures $(S,*)$ and $(T,\square)$, we aim to determine the set of homomorphisms from $S$ to $T$,
defined as:

$$
\mathcal{Hom}(S,T) := \lbrace f: S \to T\ \text{s.t.}\ \forall a,b \in S\ f(a*b) = f(a)\ \square\ f(b) \rbrace
$$

It is readily observed that $|\mathcal{Hom}(S,T)| \le |Map(S,T)| = |T|^{|S|}$, where $Map(S,T)$ denotes the set of all
mappings from $S$ to $T$.

An exhaustive algorithm searching for all possible homomorphisms from $S$ to $T$ would have an exponential time
complexity of $O(|T|^{|S|})$. However, by identifying a system of generators $G$ for $S$, we can reduce the search space
from $O(|T|^{|S|})$ to $O(|T|^{|G|})$, where $|G| \ll |S|$.

## How to determine a generating system $G$ for $S$?

There are several strategies for determining a generating system $G$ for $S$:

- Brute-Force Algorithm: Determines the minimal generating system $G$ of an algebraic structure $S$ by enumerating
  all subsets of $S$ in increasing order of cardinality. It returns the first subset $G \subseteq S$ such
  that $\langle G \rangle = S$—that is, the closure of $G$ under the structure's operations and constants coincides
  with $S$ itself. This approach guarantees finding a set of globally minimal cardinality.

- Greedy Algorithm: Constructs a generating set $G$ by iteratively adding the element that maximizes the growth of
  the closure $\langle G \rangle$ until the entire structure $S$ is covered. Redundant elements are subsequently removed
  to ensure $G$ is minimal in terms of inclusion, though this does not guarantee global minimum cardinality.

## How to determine $\mathcal{Hom}(S,T)$?

It is important to note that the generating system $G$ is generally not closed under the operation; that is, it is
likely that $\exists a,b \in G$ such that $a * b \notin G$ but in $S \setminus G$ instead.

Since $G$ generates $S$, any homomorphism $f \in \mathcal{Hom}(S,T)$ is uniquely determined by its
restriction $f|_G : G \to T$. Consequently, we need only enumerate the $|T|^{|G|}$ mappings of the
form $\varphi: G \to T$, extend each to $f: S \to T$ using the genealogy function $h$ (defined below), and verify
whether $f \in \mathcal{Hom}(S,T)$.

### Genealogy Function

The algorithm constructs a function $h: S \setminus G \to S \times S$ that associates each element $x \in S \setminus G$
with a pair $(a, b) \in S \times S$ such that $a * b = x$, effectively tracing the "genealogy" of each non-generating
element.

For example, consider the monoids $S = (\mathbb{Z}_4, +, \overline{0})$ and $T = (\mathbb{Z}_3, +, \overline{0})$.
With $G_S = \lbrace \overline{1} \rbrace$, we
have $h(\overline{0}) = (\overline{3}, \overline{1})$, $h(\overline{2}) = (\overline{1}, \overline{1})$,
and $h(\overline{3}) = (\overline{2}, \overline{1})$. Note that $h(\overline{1})$ need not be computed
since $\overline{1} \in G$.

The following figure illustrates the genealogy map $h$:

![Genealogy Map](assets/history.png)

### Backtracking and Constraint Propagation

To construct $\mathcal{Hom}(S,T)$, the algorithm systematically assigns a value in $T$ to each generator in $G$. The
function $h$ then acts as a "recipe" to derive images for the remaining elements of $S$ without further branching:
if $h(x) = (a, b)$, then $f(x) := f(a)\ \square\ f(b)$. Once a candidate $f$ is constructed, we verify that it satisfies
the homomorphism definition over $S \times S$ and preserves intrinsic properties (such as identity or zero elements). If
a contradiction arises, the candidate is discarded. If the check succeeds, $f$ is a valid homomorphism.

Applying this to our previous example, the algorithm assigns $b \in \mathbb{Z}_3$ to $g \in G$:

If $f(\overline{1}) = \overline{1}$:
$h(\overline{2}) = (\overline{1}, \overline{1}) \implies f(\overline{2}) = \overline{1} + \overline{1} = \overline{2}$
$h(\overline{3}) = (\overline{2}, \overline{1}) \implies f(\overline{3}) = \overline{2} + \overline{1} = \overline{0}$
$h(\overline{0}) = (\overline{3}, \overline{1}) \implies f(\overline{0}) = \overline{0} + \overline{1} = \overline{1}$

The mapping $f$ preserves the operation, but as the structures are monoids, $f$ must also preserve the identity
element $f(\varepsilon_S) = \varepsilon_T$. Since $f(\overline{0}) = \overline{1} \ne \overline{0}$, this assignment
leads to a contradiction, so $f \notin \mathcal{Hom}(S,T)$.

The algorithm then backtracks to test another assignment, e.g., $f(\overline{1}) = \overline{0}$:
$h(\overline{2}) = (\overline{1}, \overline{1}) \implies f(\overline{2}) = \overline{0} + \overline{0} = \overline{0}$
$h(\overline{3}) = (\overline{2}, \overline{1}) \implies f(\overline{3}) = \overline{0} + \overline{0} = \overline{0}$
$h(\overline{0}) = (\overline{3}, \overline{1}) \implies f(\overline{0}) = \overline{0} + \overline{0} = \overline{0}$

Here $f(\overline{a}) = \overline{0}$ satisfies the homomorphism definition and identity
preservation ($f(\overline{0}) = \overline{0}$), confirming $f \in \mathcal{Hom}(S,T)$ as the trivial homomorphism.

Testing the final assignment, $f(\overline{1}) = \overline{2}$:
$f(\overline{0}) = f(\overline{3}) + f(\overline{1}) = f(\overline{2}) + \overline{1} + \overline{1} = \overline{1} + \overline{1} + \overline{2} = \overline{1} \ne \overline{0}$,
leading to another contradiction.

$$
\therefore \mathcal{Hom}(S,T) = \lbrace f: \overline{a} \in \mathbb{Z}_4 \mapsto \overline{0} \in \mathbb{Z}_3 \rbrace
$$

![Backtracking](assets/backtracking.png)

Constraint propagation significantly reduces the search space compared to the $3^4 = 81$ brute-force combinations,
making this approach highly efficient.

## Classifying Homomorphisms

Once $\mathcal{Hom}(S,T)$ is identified, MorphFinder classifies each $f \in \mathcal{Hom}(S,T)$ based on its categorical
properties.

### First Isomorphism Theorem

MorphFinder utilizes the First Isomorphism Theorem, which states that for structures like groups and rings:

$$
S/\ker(f) \cong \mathrm{Im}(f)
$$

Where:

- $\ker(f) := \lbrace s \in S : f(s) = 0_T \rbrace$ is the kernel.
- $\mathrm{Im}(f) := \lbrace f(s) \in T : s \in S \rbrace$ is the image.
- $S/\ker(f)$ is the quotient structure.

The relation $|\mathrm{Im}(f)| = |S| / |\ker(f)|$ holds for groups. For more general structures (like magmas), where a
kernel might not be uniquely defined by an identity, MorphFinder uses the congruence relation $\sim_f$
where $a \sim_f b \iff f(a) = f(b)$. Here, $|\mathrm{Im}(f)|$ corresponds to the number of distinct equivalence classes
in $S/{\sim_f}$.

### Classification Criteria

MorphFinder categorizes homomorphisms based on image, kernel, and set properties:

| Property               | Symbol                       | Condition                                                                                                           | 
|------------------------|------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Trivial                | $f(S) = \lbrace 0_T \rbrace$ | $f$ maps all elements of $S$ to the identity (or zero) of $T$.                                                      |
| Monomorphism/Embedding | $f: S \hookrightarrow T$     | $f$ is injective: all $\sim_f$ classes are trivial; equivalently, $\ker(f) = \lbrace 0_S \rbrace$ for groups/rings. |
| Epimorphism            | $f: S \twoheadrightarrow T$  | $f$ is surjective: $\mathrm{Im}(f) = T$.                                                                            |
| Isomorphism            | $f: S \cong T$               | $f$ is bijective (injective and surjective).                                                                        |
| Endomorphism           | $f: S \to S$                 | $S = T$.                                                                                                            |
| Automorphism           | $f: S \cong S$               | Isomorphism with $S = T$.                                                                                           |

Beyond standard injectivity/surjectivity, MorphFinder identifies mappings of a structure to itself (endomorphism). A
bijective endomorphism that preserves all relational structure is an automorphism, representing a structural
symmetry.

For example, $f: \overline{a} \in \mathbb{Z}_6 \mapsto \overline{2a} \in \mathbb{Z}_4$:

- $\ker(f) = \lbrace \overline{0}, \overline{2}, \overline{4} \rbrace \ne \lbrace \overline{0} \rbrace \implies$ not
  injective.
- $\mathrm{Im}(f) = \lbrace \overline{0}, \overline{2} \rbrace \ne \mathbb{Z}_4 \implies$ not surjective.
  Thus, $f$ is neither a monomorphism nor an epimorphism.

For $f: \overline{a} \in \mathbb{Z}_3 \mapsto \overline{2a} \in \mathbb{Z}_3$:

- $\ker(f) = \lbrace \overline{0} \rbrace \implies$ injective.
- $\mathrm{Im}(f) = \mathbb{Z}_3 \implies$ surjective.
  This $f$ is an isomorphism, endomorphism, and automorphism, representing a non-trivial symmetry of $\mathbb{Z}_3$.
