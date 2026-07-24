import os
from pathlib import Path

from google import genai

ROOT_DIR = Path(__file__).resolve().parent.parent
PROMPT_FILE = ROOT_DIR / "prompts" / "notebook-doc-prompt.txt"
NOTEBOOK_DIR = ROOT_DIR / "notebook"
OUTPUT_DIR = ROOT_DIR / "doc"


def load_prompt() -> str:
    return PROMPT_FILE.read_text(encoding="utf-8")


def find_notebook_files() -> list[Path]:
    return [
        path for path in NOTEBOOK_DIR.rglob("*")
        if path.is_file() and not path.name.startswith(".")
    ]


def create_client() -> genai.Client:
    api_key = os.environ.get("GENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GENAI_API_KEY is not set. Define it as a GitHub secret and pass it to the workflow."
        )
    return genai.Client(api_key=api_key)


def generate_documentation(client: genai.Client, prompt_text: str, source_path: Path) -> str:
    source_content = source_path.read_text(encoding="utf-8")
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        temperature=0.2,
        contents=[
            prompt_text,
            f"### Source file: {source_path.name}\n\n{source_content}",
        ],
    )
    return response.text


def write_output(output_text: str, target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(output_text, encoding="utf-8")


def main() -> None:
    prompt_text = load_prompt()
    notebook_files = find_notebook_files()
    if not notebook_files:
        print(f"No notebook files found in {NOTEBOOK_DIR}")
        return

    client = create_client()
    print(f"Generating documentation for {len(notebook_files)} notebook file(s)")

    for source_path in notebook_files:
        target_path = OUTPUT_DIR / f"{source_path.stem}.md"
        print(f"- Processing {source_path.relative_to(ROOT_DIR)} -> {target_path.relative_to(ROOT_DIR)}")
        markdown_output = generate_documentation(client, prompt_text, source_path)
        write_output(markdown_output, target_path)

    print("Documentation generation complete.")


if __name__ == "__main__":
    main()
