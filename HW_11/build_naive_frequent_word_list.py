import string
import argparse
import json
from typing import List

def get_page_titles(page: str) -> List[List[str]]:
    """
    Extracts titles from a JSON file, processes them into keywords, 
    and returns a list of keyword lists.
    """
    titles_list = []
    
    try:
        # Open and load JSON
        with open(page, 'r', encoding='utf-8') as json_data:
            data = json.load(json_data)
        
        # Extract titles from JSON structure
        for post in data.get("data", {}).get("children", []):
            title = post.get("data", {}).get("title", "")
            if title:  # non-empty 
                titles_list.append(title)
    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading the JSON file: {e}")
        return []  
    
    # Process the extracted titles into keywords
    return title_into_keywords(titles_list)


def title_into_keywords(titles_list: List[str]) -> List[List[str]]:
    """
    Process a list of titles into a list of keyword lists.
    """
    processed_titles_list = []
    
    for title in titles_list:
        # Remove punctuation, convert to lowercase
        clean_title = title.translate(str.maketrans('', '', string.punctuation)).lower()
        
        # Split the cleaned title into words
        words = clean_title.split()
        
        # Filter out non-alphabetic words
        processed_title = [word for word in words if word.isalpha()]
        
        # Append the processed title (as list of words)
        processed_titles_list.append(processed_title)
    
    return processed_titles_list


def stopword_file_to_list(sw_file: str) -> List[str]:
    """
    Load stopwords from a file into a list.
    """
    word_list = []
    with open(sw_file, 'r') as stopwords:
        for line in stopwords:
            word_list.append(line.strip())
    return word_list


def build_word_lists(subreddits: List[str], stopwords_file: str, out_json: str):
    """
    Build a word frequency list for each subreddit JSON file, 
    and output a dictionary of word frequency.

    If a stopwords file is provided (not None), exclude those words from the ranking.
    """
    result = {}

    # Load stopwords once
    stopwords = stopword_file_to_list(stopwords_file) if stopwords_file else []

    for page in subreddits:
        # Get processed titles
        titles_keywords = get_page_titles(page)
        
        # Flatten the list of lists into list of words
        all_words = [word for title in titles_keywords for word in title]
        
        # Count word frequencies
        word_count = {}
        for word in all_words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # Filter out stopwords
        filtered_word_count = {word: count for word, count in word_count.items() if word not in stopwords}
        
        # Rank words by frequency
        ranked_words = sorted(filtered_word_count.items(), key=lambda x: x[1], reverse=True)[0:10]

        # Add to result
        result[page] = [[word, count] for word, count in ranked_words]

    # Write result to output JSON file
    try:
        with open(out_json, 'w', encoding='utf-8') as output_file:
            json.dump(result, output_file, indent=4)
        print(f"Output written to {out_json}")
    except Exception as e:
        print(f"Error writing to output file: {e}")


def main():
    parser = argparse.ArgumentParser(description="Determine frequency of title keywords in given list of subreddits")

    parser.add_argument('-o', '--output', required=True, help="Output JSON file name")
    parser.add_argument('-s', '--stopwords', help="A text file of newline-delimited stopwords to exclude from the frequency counting")
    parser.add_argument('-i', '--input', required=True, nargs='+', help="Input JSON files")

    args = parser.parse_args()

    build_word_lists(args.input, args.stopwords, args.output)


if __name__ == "__main__":
    main()
    # Use Case: python3 build_naive_frequent_word_list.py -o word_counts.json -i archery.json baking.json blacksmithing.json fencing.json gameOfThrones.json minecraft.json
    # Use Case: python3 build_naive_frequent_word_list.py -o word_counts.json -s stopwords.txt -i archery.json baking.json blacksmithing.json fencing.json gameOfThrones.json minecraft.json
