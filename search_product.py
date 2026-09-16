import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

def search_product(query, max_results=5):
    """Search Google Shopping for a given item description."""
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": os.environ.get("SERPAPI_KEY"),
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    shopping_results = results.get("shopping_results", [])

    simplified = []
    for item in shopping_results[:max_results]:
        simplified.append({
            "title": item.get("title"),
            "price": item.get("price"),
            "link": item.get("link"),
            "source": item.get("source"),
        })

    return simplified

if __name__ == "__main__":
    test_query = "white thigh high socks with blue stripes"
    results = search_product(test_query)

    print(f"Results for: '{test_query}'\n")
    if not results:
        print("⚠️ No products found for this search. Try a broader or different query.")
    else:
        for i, item in enumerate(results, 1):
            print(f"{i}. {item['title']}")
            print(f"   Price: {item['price']}")
            print(f"   Source: {item['source']}")
            print(f"   Link: {item['link']}\n")