from __future__ import annotations

import re
from typing import Dict, List, Optional

from langchain.output_parsers import RegexParser

class MY_RegexParser(RegexParser):
    """自定义RegexParser"""

    @property
    def lc_serializable(self) -> bool:
        return True

    regex: str
    output_keys: List[str]
    default_output_key: Optional[str] = None

    @property
    def _type(self) -> str:
        """Return the type key."""
        return "regex_parser"

    def parse(self, text: str) -> Dict[str, str]:
        """Parse the output of an LLM call."""
        match = re.search(self.regex, text, re.DOTALL)
        if match:
            answer = match.group(1).strip()
            score = match.group(2).strip() if match.group(2) else "0"
            return {"answer": answer, "score": score}
        else:
            return {
                "answer": text,
                "score": "10"
            }