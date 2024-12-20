# Annotation Analysis of University Subreddit Taxonomy

After comparing my annotations with those of my two "hired" annotators, I am pleased to report that there were very few disagreements and no complete 3-way disagreements. Each post's category was either unanimously agreed upon or classified with a 2/3 majority. I attribute this consistency to my thorough taxonomy, which included realistic edge cases that encouraged at least one annotator to classify posts in line with my own choices. Here is a breakdown of the disagreements we encountered:

---

### Concordia Subreddit

**Post**: t2_n7zhe - "Any degenerate daytraders at Concordia?"  
**Categories**: 2 say *social_and_events*, 1 says *career_help*.  
**Analysis**: The boundary between viewing day trading as a social or career-oriented activity made classification tricky. Given the casual tone, the post is better suited to *social_and_events*, treating it more as a hobby rather than a serious career pursuit.

**Post**: t2_16w28ypbfv - "How do I get student care ID?"  
**Categories**: 2 say *personal_help*, 1 says *campus_tips*.  
**Analysis**: A student care ID is both a personal and campus-related matter. However, given that it directly affects personal health, *personal_help* is more appropriate.

---

### McGill Subreddit

**Post**: t2_xz8mtr60d - "Is this a fake email?"  
**Categories**: 1 says *career_help*, 2 say *personal_help*.  
**Analysis**: While emails often relate to productivity, the user seems to seek reassurance, not career guidance. This qualifies it as *personal_help* rather than *career_help*.

**Post**: t2_1c5hl1qaff - "Where to look for a roommate for next year?"  
**Categories**: 2 say *personal_help*, 1 says *campus_tips*.  
**Analysis**: Although roommates live on campus, finding one is not strictly a campus-specific concern and may involve external resources. Since sharing a living space is a personal matter, *personal_help* is the better fit.

**Post**: t2_fyryp6vxn - "WHEN DO THEY TURN ON THE HEAT???"  
**Categories**: 2 say *campus_tips*, 1 says *personal_help*.  
**Analysis**: While personal comfort may vary, the question pertains to campus infrastructure. Therefore, it falls under *campus_tips* as it relates to campus facilities and operation.

---

### Observations

Interestingly, neither dataset contained *academic_clubs* posts. However, in previous scans through the full JSON data, I encountered a few posts related to academic clubs, suggesting that club-related content might simply be underrepresented in this random sample.

### Visual Analysis

After plotting the frequency of both McGill and Concordia subreddit posts by category, a strong similarity emerges in students’ primary topics of discussion. The bar plots across all seven categories are closely aligned, suggesting similar interests and priorities within each university's subreddit.