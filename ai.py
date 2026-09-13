"""Very small demo that prints only raw outputs.

Usage: python ai.py

This script reads a prompt from stdin, asks a helper model for the best model name,
then prints that model name and the model's raw answer on separate lines (no labels).
"""

import os
import dotenv

# Load API key from environment or .env and set before importing the library so
# transformers/huggingface_hub can use it when downloading models.
dotenv.load_dotenv()
_token = os.getenv("HUGGINGFACE_HUB_TOKEN") or os.getenv("HF_TOKEN")
if _token:
    os.environ["HUGGINGFACE_HUB_TOKEN"] = _token

from simple_transformer_ai_lib import ai

# Read prompt from the user
prompt = input("Enter your prompt: ")

# Prepare a list of model ids for the chooser prompt (core may return dicts with metadata)
models_info = ai.listmodels(10)
model_ids = [m["id"] if isinstance(m, dict) and "id" in m else str(m) for m in models_info]
chooser_prompt = (
    f"For this prompt: {prompt} which AI out of these {', '.join(model_ids)} "
    "is the best to answer it? Please reply with only the model id, no explanations, no extra text."
)
chosen = ai.promt(model="gpt2", prompt=chooser_prompt)
# Print only raw chosen model id
print(chosen)
# Ask the chosen model for the answer and print only the raw response
response = ai.promt(model=chosen, prompt=prompt)
print(response)
