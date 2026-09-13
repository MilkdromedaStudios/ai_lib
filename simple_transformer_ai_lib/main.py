# Delegate module to ai_lib.main but provide a simple CLI that prints only the raw model output
from ai_lib import main as _main
import sys


def main():
    # Support: python -m simple_transformer_ai_lib.main [--model MODEL] <prompt parts...>
    argv = sys.argv[1:]
    model = None

    if not argv:
        print('No prompt provided. Usage: python -m simple_transformer_ai_lib.main [--model MODEL] "your prompt"')
        sys.exit(1)

    # Simple flag parsing for --model
    if "--model" in argv:
        idx = argv.index("--model")
        if idx + 1 < len(argv):
            model = argv[idx + 1]
            # remove flag and value
            del argv[idx:idx + 2]
        else:
            print('Usage error: --model requires an argument')
            sys.exit(1)

    prompt = " ".join(argv).strip()
    if not prompt:
        print('No prompt provided. Usage: python -m simple_transformer_ai_lib.main [--model MODEL] "your prompt"')
        sys.exit(1)

    # Empty model string means use default
    if isinstance(model, str) and model.strip() == "":
        model = None

    # Delegate to underlying AI instance; print only raw generated text
    output = _main.ai.generate(prompt, model=model)
    print(output)


if __name__ == "__main__":
    main()
