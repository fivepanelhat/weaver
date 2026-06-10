"""Local LLM wrapper with Ollama support and a deterministic fallback."""


try:
    from langchain_community.llms import Ollama
except Exception:
    Ollama = None


class LocalSovereignLLM:
    def __init__(self, model: str = "mosaicml/mpt-7b-instruct"):
        self.model = model
        if Ollama is not None:
            try:
                self.client = Ollama(model=self.model)
            except Exception:
                self.client = None
        else:
            self.client = None

    def invoke(self, prompt: str) -> str:
        """Invoke the local LLM. Falls back to a deterministic response when client missing."""
        if self.client is not None:
            try:
                return self.client(prompt)
            except Exception:
                pass

        # deterministic fallback: return ESCALATE if 'anger' or 'safety' in
        # prompt
        lower = prompt.lower()
        if "anger" in lower or "safety" in lower or "escalate" in lower:
            return "ESCALATE"
        return "Scaffolded LLM Response based on local data."
