# Homework 11

## Task 5 - Analysis

1) What is the impact of including a stop word list?

A stop word list was an effective means of ignoring filler words in both the naive and TF-IDF methods of frequency analysis.  Words that are commonly used many times but have no strong relation to a given topic (the, and, but, I ...) are not useful to calculate and do not indicate any underlying trends.  They are a waste of computational power, and ignoring them provides much more relevant and subject-focused terminology, aiding in a more thorough analysis.  Note though, stopwords tended to appear less in the TF-IDF method, even without guarding against stopwords.  Perhaps this is because stopwords are common in the english language and appear uniformly in most documents / subreddits.

2) What differences do you observe with TF-IDF?

TF-IDF certainly differed from a simple frequency rank ordering.  Especially because I chose subreddits of similar subjects (related vaguely to a medieval or fantasy theme).  This meant that certain topics that are common amongst medieval life, swordfighting, royalty, and artisanal cooking, would lead to higher penalties for words like "sword", since despite this word being topically unique, the fact that a nunber of these subreddits share this common theme, would make the inverse document frequency quite low, even if the term frequency was high.  For TF-IDF, this lead to the top 10 words being more diverse and unique-to-the-subreddit with respect to the other subreddits, than a frequency analysis which had a number of common words.  "Minecraft" is very frequent to appear in the Minecraft subreddit, and very unlikely to appear in every other.  Same for "Ned" in Game of Thrones, as opposed to Baking or Archery. Conversely "blade" is much higher ranked in fencing's term frequency list, but it drops sharply to near 10th place in the TF-IDF, as blacksmithing also mentions "blade".

3) Which method produces the best list?

TF-IDF with stopwords excluded yields the most informative and analytical JSON dataset--the best list.  It ranks highest the terms with a balance of frequency and uniqueness, and it excludes filler words that dilute the more noteworthy by hiding them in the rankings (Ex. "him" taking a place in the top 10 words under archery is a lot less useful to the topic of archery than "deflect").  Moreover, absolute frequency is not as good at exposing contrasts between the subreddits even if it shows trends with respect to each individual page.  Hence both excluding stopwords and using Term Frequency * Inverse Document Frequency are preferred and produce the best list.