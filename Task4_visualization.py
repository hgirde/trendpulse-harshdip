"""
Author:Harshdip Girde
"""



import pandas as pd     
import matplotlib.pyplot as plt 
import os                




file_path = "data/trends_analysed.csv"

try:
    df = pd.read_csv(file_path)
    print("Data loaded successfully")
except Exception as e:
    print("Error loading file:", e)
    exit()



if not os.path.exists("outputs"):
    os.makedirs("outputs") 



def shorten_title(title):
    return title[:50] + "..." if len(title) > 50 else title  # bada title short




top10 = df.sort_values(by="score", ascending=False).head(10) 
titles = [shorten_title(t) for t in top10["title"]]

plt.figure()
plt.barh(titles, top10["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis() 

plt.savefig("outputs/chart1_top_stories.png") 
plt.close()




category_counts = df["category"].value_counts()

plt.figure()
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.savefig("outputs/chart2_categories.png")
plt.close()




popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure()
plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.savefig("outputs/chart3_scatter.png")
plt.close()




fig, axes = plt.subplots(1, 3, figsize=(18, 5)) 


axes[0].barh(titles, top10["score"])
axes[0].set_title("Top 10 Stories")
axes[0].set_xlabel("Score")
axes[0].invert_yaxis()



axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")



axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].legend()


plt.suptitle("TrendPulse Dashboard")

plt.savefig("outputs/dashboard.png")  
plt.close()
