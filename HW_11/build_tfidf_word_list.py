import string
import argparse
import json
import math
from typing import List, Dict


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


def build_word_freq_lists(subreddits: List[str], stopwords_file: str) -> Dict[str, Dict[str, int]]:
    """
    Build a word frequency list for each subreddit JSON file.

    Args:
        subreddits (List[str]): List of subreddit JSON filenames.
        stopwords_file (str): Path to a file containing stopwords.

    Returns:
        dict: A dictionary of word frequencies for each subreddit.
    """
    result = {}

    # Load stopwords once
    stopwords = stopword_file_to_list(stopwords_file) if stopwords_file else []

    for page in subreddits:
        # Get processed titles
        titles_keywords = get_page_titles(page)
        
        # Flatten the list of lists into a list of words
        all_words = [word for title in titles_keywords for word in title if word not in stopwords]
        
        # Count word frequencies
        word_count = {}
        for word in all_words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # Add word counts to the result for this subreddit
        result[page] = word_count
    
    return result  # A dictionary to facilitate TF-IDF calculation


def build_tfidf_lists(freq_lists: Dict[str, Dict[str, int]], subreddits: List[str], out_json: str):
    """
    Calculate TF-IDF scores for words in subreddit JSON files and save the output to a file.

    Args:
        freq_lists (dict): A dictionary of word frequencies for each subreddit.
        subreddits (List[str]): List of subreddit JSON filenames.
        out_json (str): Path to the output JSON file.
    """
    num_documents = len(subreddits)
    result = {}

    # Iterate over each subreddit
    for subreddit in subreddits:
        tfidf_scores = {}

        # Get word frequencies for the current subreddit
        word_frequencies = freq_lists[subreddit]
        total_words = sum(word_frequencies.values())  # Total words in this subreddit
        
        # Calculate TF-IDF for each word
        for word, tf in word_frequencies.items():
            # Count how many documents (subreddits) contain this word
            doc_count = sum(1 for page in subreddits 
                            if word in freq_lists[page])
            
            # Calculate IDF
            idf = math.log(num_documents / doc_count)
            
            # Compute TF-IDF
            tfidf_scores[word] = tf * idf
        
        # Get the top 10 words by TF-IDF scores
        top_tfidf = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[0:10]
        result[subreddit] = [[word, score] for word, score in top_tfidf]

    # Save the result to the output JSON file
    try:
        with open(out_json, 'w', encoding='utf-8') as output_file:
            json.dump(result, output_file, indent=4)
        print(f"TF-IDF scores written to {out_json}")
    except Exception as e:
        print(f"Error writing to output file: {e}")


def main():
    parser = argparse.ArgumentParser(description="Determine TF-IDF scores of title keywords in given list of subreddits.")

    parser.add_argument('-o', '--output', required=True, help="Output JSON file name")
    parser.add_argument('-s', '--stopwords', help="A text file of newline-delimited stopwords to exclude from the frequency counting")
    parser.add_argument('-i', '--input', required=True, nargs='+', help="Input JSON files")

    args = parser.parse_args()

    # Build word frequency lists
    freq_lists = build_word_freq_lists(args.input, args.stopwords)

    # Build TF-IDF lists and write to output file
    build_tfidf_lists(freq_lists, args.input, args.output)


if __name__ == "__main__":
    main()
    # Use case: python3 build_tfidf_word_list.py -o word_scores.json -i archery.json baking.json blacksmithing.json fencing.json gameOfThrones.json minecraft.json
    # Use case: python3 build_tfidf_word_list.py -o word_scores.json -s stopwords.txt -i archery.json baking.json blacksmithing.json fencing.json gameOfThrones.json minecraft.json
