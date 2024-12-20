import csv
import json
import argparse
from collections import defaultdict

def build_interaction_network(input_file):

    interaction_network = defaultdict(lambda: defaultdict(int)) # {"speaker": {"listener": interactions, ...}, ... }
    speaker = None
    prev_episode = None

    # Words to skip when determining listener
    skip_words = {"others", "ponies", "and", "all"}

    with open(input_file, 'r', encoding='utf-8') as csvfile:
        dialogue = csv.reader(csvfile)

        for line in dialogue:

            # REDUNDANT, we check listener validity before making them a speaker
            # # Skip if current speaker name indicates group or not singular
            # invalid_speaker = False

            # if speaker:
            #     for word in speaker.split(" "):
            #         if word in skip_words: # Is the character name valid
            #             invalid_speaker = True
            #             break # out of this inner loop 

            # if invalid_speaker: # Go to next line and try again
            #     speaker = None
            #     continue # Current speaker wasn't a valid character so go to next line

            episode, listener = line[0].lower(), line[2].lower() # Info from line

            if prev_episode and prev_episode != episode: # If this line and the next line aren't the same episode
                speaker = None
                prev_episode = episode # Only change prev episode if it's the first line or if the current episode is different than the last one
                continue # Skip: last line character of episode i is not talking to first line character in episode i + 1

            if speaker == listener:
                continue # but don't change speaker because it must be valid if this char was assigned to speaker from previous loop and maybe the next line is another character
                # ex:
                # A: "bla"
                # A: "bla"
                # B: "bla" A->B is an speaker-listener interaction

            # Skip if current row has a character name indicating group or not singular listener/speaker
            invalid_listener = False

            for word in listener.split(" "):
                if word in skip_words: # Is the character name valid
                    invalid_listener = True
                    break # out of this inner loop 

            if invalid_listener: # Same principle as with speaker.  Also discount if character has 2 subsequent dialogue lines 
                speaker = None
                continue # Current speaker wasn't speaking to a valid single character, go to next line iteration

            # If we get here and have a current speaker, then the interaction is valid
            if speaker:
                interaction_network[speaker][listener] += 1 # speaker speaks to character (listener)
            speaker = listener # Might assign current speaker as invalid but will be pruned at start of next iteration

    return interaction_network

def clean_up_network(interactions_dict, output_file):
    # speakers and all their speaks
    speaks_counts = {}

    # calculate total lines spoken by given speaker
    for speaker, listener_dict in interactions_dict.items():
        times_spoken = sum(listener_dict.values())  # add up all interactions for this speaker
        speaks_counts[speaker] = times_spoken

    # Sort via total lines spoken most to least, lambda [1] cuz value is an int to sort by
    top_speakers = [speaker for speaker, _ in sorted(speaks_counts.items(), key=lambda x: x[1], reverse=True)[:101]]

    filtered_interactions_dict = {} # new dict with only those characters

    for speaker in top_speakers:
        filtered_interactions_dict[speaker] = interactions_dict[speaker]

    # Save the filtered interaction network to a JSON file
    with open(output_file, 'w', encoding='utf-8') as network_json:
        json.dump(filtered_interactions_dict, network_json, indent=4)

    print(f"Filtered interaction network saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build an interaction network of My Little Pony Character from their dialogue CSV file.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input dialogue CSV file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output JSON Interaction Network.")

    args = parser.parse_args()

    unfiltered_network = build_interaction_network(args.input)
    clean_up_network(unfiltered_network, args.output)

# python3 build_interaction_network.py -i clean_dialog.csv -o interactions.json