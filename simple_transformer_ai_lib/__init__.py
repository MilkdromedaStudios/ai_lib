"""Compatibility shim for simple_transformer_ai_lib.

Provides a simple `ai` object with methods:
 - ai.listmodels(limit=20)
 - ai.promt(model="", prompt="")  # intentionally keeping user's preferred name
 - ai.prompt(model="", prompt="")  # corrected alias

This delegates to the ai_lib.main implementation and returns plain text answers.
"""
from typing import Any
import ai_lib.main as _core


class SimpleAI:
    def listmodels(self, limit: int = 20) -> list[str]:
        """Return a list of available model IDs."""
        return _core.list_models(limit)

    def promt(self, *args: Any, **kwargs: Any) -> str:
        """Generate text.

        Accepts calls in either form:
          promt(prompt_text)
          promt(model_id, prompt_text)
          promt(model="gpt2", prompt="Hello")

        An empty string for model (model="") is treated as no model provided and will use the
        underlying AI instance default model.
        """
        model = None
        prompt_text = None

        # kwargs take precedence
        if "model" in kwargs:
            model = kwargs.get("model")
        if "prompt" in kwargs:
            prompt_text = kwargs.get("prompt")

        # positional args
        if len(args) == 1 and prompt_text is None:
            prompt_text = args[0]
        elif len(args) >= 2:
            model = args[0]
            prompt_text = args[1]

        if prompt_text is None:
            raise TypeError("promt() requires a prompt. Usage: promt(prompt) or promt(model, prompt) or promt(model=..., prompt=...)")

        # Treat empty-string model as no model specified
        if isinstance(model, str) and model.strip() == "":
            model = None

        # Delegate to underlying ai instance; ensure only the generated text is returned
        return _core.ai.generate(str(prompt_text), model=model)

    # provide a correctly spelled alias
    def prompt(self, *args: Any, **kwargs: Any) -> str:
        return self.promt(*args, **kwargs)


# Export a module-level instance
ai = SimpleAI()

__all__ = ["ai", "SimpleAI"]
