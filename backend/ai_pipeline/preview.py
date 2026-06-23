import json
import os

filename = input("Enter output JSON filename: ")
with open(os.path.join("output", filename), "r") as f:
    data = json.load(f)

for page in data["pages"]:
    print(f"\n{'='*60}")
    print(f"PAGE {page['page_number']}")
    print(f"{'='*60}")
    print(page["extracted_content"])
    print(f"\nDiagrams found: {len(page['diagrams'])}")
    for d in page["diagrams"]:
        print(f"  - {d['description']} → {d['image_path']}")
    print(f"Confidence Score: {page['confidence_score']}")

print(f"\nOverall Confidence: {data['overall_confidence']}%")