"""
Author: Harshdip Girde
"""



import requests 
import json     
import time     
import os       
from datetime import datetime  



TOP_STORIES = https://hacker-news.firebaseio.com/v0/topstories.json
ITEM = https://hacker-news.firebaseio.com/v0/item/{id}.json




headers = {"User-Agent": "TrendPulse/1.0"}





CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

MAX_PER_CATEGORY = 25 




def assign_category(title):
    title_lower = title.lower()  

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower: 
                return category

    return None



def main():
    try:
        response = requests.get(TOP_STORIES, headers=headers) 
        story_ids = response.json()[:500] 
    except Exception as e:
        print("Failed to fetch top stories:", e)
        return

    collected_data = []  
    category_count = {cat: 0 for cat in CATEGORIES} 
    seen_ids = set() 

    print("Collecting stories and categorizing...")


  

    for story_id in story_ids:

       
        if all(count >= MAX_PER_CATEGORY for count in category_count.values()):
            break

        try:
            res = requests.get(ITEM.format(story_id), headers=headers)
            story = res.json()

            if not story or "title" not in story:  
                continue

            assigned = assign_category(story["title"])  
            if assigned and category_count[assigned] < MAX_PER_CATEGORY:

                if story_id not in seen_ids:  

                    data = {
                        "post_id": story.get("id"),
                        "title": story.get("title"),
                        "category": assigned,
                        "score": story.get("score", 0),
                        "num_comments": story.get("descendants", 0),
                        "author": story.get("by"),
                        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    collected_data.append(data) 
                    category_count[assigned] += 1 
                    seen_ids.add(story_id) 

        except Exception as e:
            print(f"Failed to fetch story {story_id}: {e}")

        time.sleep(0.2)




    if not os.path.exists("data"):
        os.makedirs("data")


   

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print(f"\nCollected {len(collected_data)} stories. Saved to {filename}")




if __name__ == "__main__":
    main()
