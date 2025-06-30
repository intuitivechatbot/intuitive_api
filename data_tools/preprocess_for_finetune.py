import json

with open('qa_style_new.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

qa_pairs = []
for theme in data["themes"]:
    for qa in theme["qa"]:
        prompt = f"[{theme['theme']}] {qa['question']}"
        qa_pairs.append({
            "prompt": prompt,
            "response": qa["answer"]
        })

with open('qa_dataset.jsonl', 'w', encoding='utf-8') as f:
    for qa in qa_pairs:
        f.write(json.dumps(qa, ensure_ascii=False) + "\n")

print(f"Created {len(qa_pairs)} Q&A pairs for fine-tuning.")