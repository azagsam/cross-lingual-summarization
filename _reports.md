Problem: it is not evident from gigafida which sentences of each article form a first paragraph/summary.

# HOW THE SUMMARIES WERE GENERATED
1. Get 25 random summaries/paragraphs from sta.si 
2. Split sentences into characters. Analyse and determine the average length of a summary.
3. Run a heuristic algorithm which predicts summary and body of each article according to the average length

# RESULTS
3/25 generated summaries contain additional redundant sentence (too long)
2/25 generated summaries don't contain all relevant sentences (too short)
20/25 generated summaries contain all relevant sentences
