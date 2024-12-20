import matplotlib.pyplot as plt
import pandas as pd

# Data for the two datasets with categories
data_concordia = [
    "courses_and_grades", "personal_help", "courses_and_grades", "social_and_events", "courses_and_grades",
    "exams_and_projects", "personal_help", "exams_and_projects", "courses_and_grades", "social_and_events",
    "exams_and_projects", "social_and_events", "campus_tips", "courses_and_grades", "career_help",
    "courses_and_grades", "courses_and_grades", "courses_and_grades", "personal_help", "campus_tips"
]

data_mcgill = [
    "exams_and_projects", "courses_and_grades", "courses_and_grades", "social_and_events", "personal_help",
    "exams_and_projects", "courses_and_grades", "personal_help", "exams_and_projects", "courses_and_grades",
    "courses_and_grades", "courses_and_grades", "social_and_events", "campus_tips", "courses_and_grades",
    "courses_and_grades", "courses_and_grades", "career_help", "personal_help", "career_help"
]

# Count frequencies of each category in each dataset
categories = [
    "exams_and_projects", "courses_and_grades", "academic_clubs", 
    "social_and_events", "personal_help", "career_help", "campus_tips"
]

concordia_counts = {category: data_concordia.count(category) for category in categories}
mcgill_counts = {category: data_mcgill.count(category) for category in categories}

# Create DataFrame for easy plotting
df = pd.DataFrame({
    'Concordia': concordia_counts,
    'McGill': mcgill_counts
})

# Plotting
df.plot(kind='bar', figsize=(10, 6))
plt.title("Frequency of Categories in University Subreddits (Concordia vs McGill)")
plt.xlabel("Categories")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.legend(title="Dataset")
plt.tight_layout()
plt.show()
