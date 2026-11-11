# similarity_tools

Levenshtein edit distance and Jaro-Winkler similarity for short strings, with no third-party dependencies.

```python
from similarity_tools import levenshtein, jaro_winkler

distance = levenshtein("kitten", "sitting")  # 3
score = jaro_winkler("MARTHA", "MARHTA")     # 0.9611111111111111
```

## Why this exists

Fuzzy matching short strings is a common need, but pulling in a full fuzzy-matching library for two well-known algorithms is often overkill. This package provides just the two metrics, implemented with the standard library only, so it can be vendored or dropped into a constrained environment without dependency management.

The trade-off is deliberate: the functions are pure and case-sensitive. No normalisation (lowercasing, trimming, Unicode folding) is performed. That keeps behaviour predictable and puts the policy decision in the caller's hands.

## Edge cases

- Both functions treat the empty string as a valid input. `levenshtein("", "abc")` is 3; `jaro_winkler("", "abc")` is 0.0.
- Jaro-Winkler is symmetric: `jaro_winkler(a, b) == jaro_winkler(b, a)`.
- The Jaro-Winkler prefix boost is capped at 4 characters and uses the standard weight of 0.1.
- Case matters: `levenshtein("a", "A")` is 1, and `jaro_winkler("a", "A")` is 0.0.
