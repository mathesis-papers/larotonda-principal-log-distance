# Trace-coupled counterexamples to Larotonda's principal-log distance conjecture: beyond the Antezana-Larotonda-Varela theorem

Haobo Ma (ChronoAI Pte Ltd, Singapore), then Wenlin Zhang (National University of Singapore; ChronoAI Pte Ltd, Singapore).

The note refutes the conjecture after Proposition 4.3 in Section 4.1, p. 7 of Gabriel Larotonda's *Short curves in homogeneous spaces of the unitary group for unitarily invariant norms*, [arXiv:2610.31535v1](https://arxiv.org/abs/2610.31535v1).

## Contents and mathematical coverage

- `note.tex` and `note.pdf`: complete written proofs for the positive-definite trace-coupled quadratic family, its two-dimensional counterexample and the smaller-radius consequences. For c>0, scalar eigenangles above pi(1+c)/(1+nc) admit a shorter logarithm. In each dimension n>=2 every radius r>pi/n admits a counterexample for a suitable c>0. The c=0 positive case is the cited theorem of Antezana, Larotonda and Varela (2011/2014).
- `verify.py` and `checks.json`: exact rational finite checks. Angles are in units of pi, squared norms in units of pi squared. No floating-point approximations are used.
- `metadata.json`: authorship, license, problem identity and fixed-version scientific sources.

The pinned [Lean source](https://github.com/the-omega-institute/trureturing/blob/a89e0fb9ba0f9002502ec8125455c2c2a9281443/D5/S3/QuadraticForms/LarotondaPrincipalLogDistanceRefutation.lean), declaration `D5.S3.QuadraticForms.LarotondaPrincipalLogDistanceRefutation.result`, states the negation of the universal principal-log assertion and uses the dimension-two, trace-coefficient-four counterexample. The parameter-family classification and smaller-radius consequences have written proofs in the note. The finite checks support their explicit coefficients, not the all-parameter norm and curve arguments.

The source's pi/2 passage is a conditional input to a possible extension, not a separately asserted theorem. The U(3) example shows that this input fails. Segment convexity, the stated quotient theorems, uniqueness in quotients and the infinite-dimensional extension are outside the result's coverage. No exact global-distance formula is asserted.

## Rebuild

Use Tectonic 0.17.0:

```sh
tectonic note.tex
python3 verify.py > checks-rebuilt.json
cmp checks.json checks-rebuilt.json
```

Alternatively, use a standard LaTeX installation with AMS packages, geometry, booktabs, lmodern and hyperref:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is embedded in `note.tex`; BibTeX is not needed. `verify.py` uses only Python's standard library (Python 3.10 or later).

## License

Copyright 2026 Haobo Ma and Wenlin Zhang. Creative Commons Attribution 4.0 International, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (`cc-by-4.0`).
