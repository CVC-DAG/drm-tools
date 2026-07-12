"""Ready-to-run dataset loaders for tutorial examples.

This package contains small dataset loaders for common graph domains:

- Karate Club (NetworkX classic)
- Bibliographic references (OpenAlex API)
- Movies (movie domain, loaded into Neo4jGraph)
- Game of Thrones (character domain, loaded into Neo4jGraph)
"""

from .networkx_karate import load_karate_club
from .networkx_bibliografia import load_bibliografia_openalex
from .neo4j_movies import load_movies_sample
from .neo4j_got import load_got_characters
from .load_ric_o_naf import load_ric_o_naf
from .cli import main

__all__ = [
    "load_karate_club",
    "load_bibliografia_openalex",
    "load_movies_sample",
    "load_got_characters",
    "load_ric_o_naf",
    "main",
]

