"""Similarity tools for fuzzy matching short strings.

This package provides Levenshtein distance and Jaro-Winkler similarity.
"""

from .core import levenshtein, jaro_winkler

__all__ = ["levenshtein", "jaro_winkler"]
