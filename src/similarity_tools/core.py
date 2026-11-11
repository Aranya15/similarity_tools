"""Core similarity functions.

All functions operate on strings and are case-sensitive. No preprocessing
(e.g., lowercasing, trimming) is performed; callers should normalise if needed.

WHY: Keeping the functions pure and predictable makes them easier to compose and
test. Case folding is a policy decision that varies by application.
"""


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between two strings.

    The distance is the minimum number of single-character edits
    (insertions, deletions, substitutions) required to change *a* into *b*.

    This implementation uses a rolling array to keep memory usage O(min(len(a), len(b))).
    """
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    # Ensure a is the shorter string to minimise memory.
    if len(a) > len(b):
        a, b = b, a

    previous = list(range(len(a) + 1))
    for i, ch_b in enumerate(b, 1):
        current = [i]
        for j, ch_a in enumerate(a, 1):
            insert = previous[j] + 1
            delete = current[j - 1] + 1
            substitute = previous[j - 1] + (ch_a != ch_b)
            current.append(min(insert, delete, substitute))
        previous = current
    return previous[-1]


def jaro_winkler(a: str, b: str, prefix_weight: float = 0.1) -> float:
    """Return the Jaro-Winkler similarity between two strings.

    The result is a float between 0.0 (no similarity) and 1.0 (identical).

    *prefix_weight* controls how much the common prefix boosts the score.
    The standard value is 0.1, and the prefix length is capped at 4 characters.
    """
    if a == b:
        return 1.0
    if not a or not b:
        return 0.0

    len_a = len(a)
    len_b = len(b)
    max_dist = max(len_a, len_b) // 2 - 1
    if max_dist < 0:
        max_dist = 0

    # Matching window: characters are considered matching if they are within
    # max_dist positions of each other.
    a_matches = [False] * len_a
    b_matches = [False] * len_b
    matches = 0

    for i in range(len_a):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, len_b)
        for j in range(start, end):
            if b_matches[j] or a[i] != b[j]:
                continue
            a_matches[i] = True
            b_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    # Count transpositions: matched characters that are out of order.
    transpositions = 0
    k = 0
    for i in range(len_a):
        if not a_matches[i]:
            continue
        while not b_matches[k]:
            k += 1
        if a[i] != b[k]:
            transpositions += 1
        k += 1
    transpositions //= 2

    jaro = (matches / len_a + matches / len_b + (matches - transpositions) / matches) / 3.0

    # Winkler modification: boost for common prefix up to 4 characters.
    prefix_len = 0
    for ca, cb in zip(a, b):
        if ca != cb or prefix_len >= 4:
            break
        prefix_len += 1

    return jaro + prefix_len * prefix_weight * (1.0 - jaro)
