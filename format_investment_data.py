import json
import random

# Input and output paths
input_path = "../data/raw_articles.jsonl"
output_path = "../data/instruction_dataset.jsonl"

# Instruction templates (add more if needed)
instruction_templates = [
    "Summarize the main investment strategy in the article.",
    "List the key points or takeaways from the investment article.",
    "Explain the financial principles used in this article.",
    "What kind of investor is this strategy most suitable for?",
    "What are the potential risks mentioned in this article?"
]

def format_example(article_text, target_response=None):
    """Format an article into an instruction-style prompt"""
    instruction = random.choice(instruction_templates)
    formatted = {
        "text": f"### Prompt:\n{instruction}\n\n### Article:\n{article_text.strip()}\n\n### Response:\n{target_response or ''}"
    }
    return formatted

def load_articles(jsonl_path):
    """Load articles from JSONL. Expects each line to have an 'article' or 'text' field."""
    with open(jsonl_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def save_formatted_dataset(data, jsonl_path):
    """Save list of dicts to a JSONL file"""
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def main():
    raw_data = load_articles(input_path)
    
    # Replace "article" with your actual field name if different
    formatted_data = [format_example(item["article"]) for item in raw_data if item.get("article")]

    save_formatted_dataset(formatted_data, output_path)
    print(f"Formatted {len(formatted_data)} examples and saved to {output_path}")

if __name__ == "__main__":
    main()
