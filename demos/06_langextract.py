"""
DEMO 6 — LangExtract (Google): structured extraction with source grounding.

Run:  python demos/06_langextract.py

Talking point: LangExtract pulls STRUCTURED data out of messy text and — unlike a
plain "return JSON" prompt — it grounds every extraction to the exact source
span (char offsets) so results are auditable. Great for docs/compliance.

⚠️ PRE-FLIGHT THIS ONE. LangExtract routes model_id -> provider by name pattern
and defaults to Gemini. Below we force the OpenAI-compatible backend and point
it at OpenRouter. If your version doesn't accept `language_model_params`,
fallback: get a free Gemini key (https://aistudio.google.com/apikey) and use
model_id="gemini-2.0-flash", api_key=<gemini key>.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import langextract as lx
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, assert_key

assert_key()

prompt = (
    "Extract each robot product mentioned, with its battery life and payload "
    "or key spec. Use exact text from the source; do not paraphrase."
)

examples = [
    lx.data.ExampleData(
        text="Acme Falcon: aerial drone, 40-minute flight time, 2 kg payload.",
        extractions=[
            lx.data.Extraction(
                extraction_class="product",
                extraction_text="Acme Falcon",
                attributes={"spec": "40-minute flight time", "payload": "2 kg"},
            )
        ],
    )
]

input_text = open(
    os.path.join(os.path.dirname(__file__), "..", "data", "company_faq.md")
).read()

result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="openai/gpt-4o-mini",              # OpenAI-compatible slug for OpenRouter
    api_key=OPENROUTER_API_KEY,
    fence_output=True,
    use_schema_constraints=False,
    language_model_params={"base_url": OPENROUTER_BASE_URL},
)

print("\n--- Grounded extractions ---")
for e in result.extractions:
    span = e.char_interval
    print(f"[{e.extraction_class}] {e.extraction_text}  attrs={e.attributes}  span={span}")

# Bonus: writes an interactive HTML you can open in a browser live.
lx.io.save_annotated_documents([result], output_name="langextract_demo.jsonl", output_dir=".")
print("\nSaved langextract_demo.jsonl (visualize with lx.visualize).")
