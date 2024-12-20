import argparse
import random
import json

def get_sample_idxs(n: int, num_posts: int) -> list:
    '''
    Return a list of n unique random indices in range 0 to total_posts,
    representing the sample posts we will take from our McGill or Concordia
    full JSON files.
    '''
    return random.sample(range(num_posts), n)

def get_tsv_list(posts, sample_idxs: list[int]) -> list[str]:
    '''
    Use the sample indices to obtain the author and title from those indices within the posts data
    '''
    return [f"{posts[i]['data']['author_fullname']}\t{posts[i]['data']['title']}\t\n" for i in sample_idxs] # List comprehension

def to_tsv(input: str, output: str, n: int):
    '''
    The worker / pipeline function that carries out the extraction procedure
    from an input JSON to an output TSV
    '''
    try:
        with open(input, 'r') as json_raw:
            data = json.load(json_raw)
    except FileNotFoundError:
        print(f"Error: The input file '{input}' was not found.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON from the input file.")
        return


    posts = data['data']['children'] # Accessing the part of the full dataset which lists each post
    num_posts = data['data']['dist'] # Meta data provided at the top of the JSON, saves us computation time, no need for len(posts)

    if num_posts == 0:
        print("No posts available in the input JSON.") # Error handling
        return # This edge case should not produce an empty list, even though n=0 would.

    if n == -1 or n > num_posts: # n wasn't provided or it's too big
        idxs = range(0,num_posts) # Return all the posts
    else:
        idxs = get_sample_idxs(n, num_posts) # Sampling a subset of posts, should work with 0 too and just return an empty list

    tsv_data = get_tsv_list(posts, idxs)

    with open(output, 'w') as tsv_out:
        tsv_out.writelines(tsv_data) # Write our TSV list into the correct output file

    print(f"Wrote the data from {len(idxs)} posts to {output}")

def main():
    '''
    The top executive function that handles parameters and initiates function calls.
    '''
    parser = argparse.ArgumentParser(description="Outputs given number of randomly selected reddit posts from given reddit API JSON to a given filepath")
    
    parser.add_argument("-o", "--output", required=True, help="The output file to save the reddit API JSON data")
    parser.add_argument("-i", "--input", required=True, help="The input JSON from the reddit API") # Has 100 entries as max specified by Reddit API
    parser.add_argument("-n", "--number", default=-1, type=int, help="The (positive) number of randomly selected posts to be saved in the output file, defaults to all posts.")
    # Note, by setting the default of an unspecified --number to be -1, we can look for this -1 later to know n was not provided
    # Since -1 is an invalid input for an argument that is expected to be a natural number in value.

    args = parser.parse_args()

    to_tsv(args.input, args.output, args.number)


if __name__ == "__main__":
    '''
    Use case:

    python3 extract_to_tsv.py -o annotated_concordia.tsv -i concordia.json -n 50
    python3 extract_to_tsv.py -o annotated_mcgill.tsv -i mcgill.json -n 50 
    '''
    main() # Good practice