"""PyHound: Hunt down retrieval problems in RAG/LLM systems."""

__version__ = "0.1.0"
__author__ = "Georgi Mammen Mullassery"
__email__ = "mullassery@gmail.com"
__license__ = "MIT"

from pyhound.hound import Hound
from pyhound.diagnosis import Diagnosis
from pyhound.comparison import ModelComparison
from pyhound.scorer import QualityScorer

__all__ = [
    "Hound",
    "Diagnosis",
    "ModelComparison",
    "QualityScorer",
]
