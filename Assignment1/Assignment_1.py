import csv
import json
import sys
import os


sys.path.append(os.path.abspath(".."))

from llm import ask


def classify_claim(claim_text):
    prompt = f"""
You are an insurance claim classification assistant.

Analyze the following claim description and return ONLY valid JSON.

Claim:
{claim_text}

Required JSON format:
{{
  "claim_type": "Motor | Property | Liability",
  "tone": "Calm | Frustrated | Urgent",
  "legal_action": "Yes | No"
}}
"""

    response = ask(
        [
            {
                "role": "system",
                "content": "you are an insurance classification assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    content = response.choices[0].message.content.strip()
    content = content.replace("```json","")
    content = content.replace("```","")
    content = content.strip()

    print("\nRaw Response:")
    print(content)

    return json.loads(content)

# --------------------------------------------------
# Read claims from CSV
# --------------------------------------------------
claims = []

with open("claims.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        claims.append({
            "claim_id": row["claim_id"],
            "description": row["description"]
        })

# --------------------------------------------------
# Process claims
# --------------------------------------------------
results = []

for claim in claims:
    classification = classify_claim(claim["description"])

    results.append({
        "claim_id": claim["claim_id"],
        "description": claim["description"],
        "claim_type": classification["claim_type"],
        "tone": classification["tone"],
        "legal_action": classification["legal_action"]
    })

# --------------------------------------------------
# Save output
# --------------------------------------------------
with open("classified_claims.json", "w", encoding="utf-8") as outfile:
    json.dump(results, outfile, indent=4)

print("Classification completed.")
print("Results saved to classified_claims.json")