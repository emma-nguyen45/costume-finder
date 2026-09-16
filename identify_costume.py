import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def identify_costume_items(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    ext = image_path.split(".")[-1].lower()
    mime_type = f"image/{'jpeg' if ext == 'jpg' else ext}"

    prompt = (
        "Identify the character in this image and list the distinct "
        "costume items needed to dress as them. Respond with ONLY valid "
        "JSON, no other text, no markdown formatting, in this exact format:\n"
        '{"character": "name", "items": [{"category": "e.g. jacket", '
        '"description": "detailed description for shopping search"}]}'
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            prompt,
        ],
    )

    return response.text

if __name__ == "__main__":
    result = identify_costume_items("test_character.jpg")
    print(result)

    cleaned = result.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    try:
        parsed = json.loads(cleaned)
        print("\n✅ Successfully parsed JSON:")
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError as e:
        print(f"\n❌ Failed to parse JSON: {e}")
        print(f"Raw output was: {result}")