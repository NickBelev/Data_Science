**Task 2**:

0) We first run `scp -i ~/. ssh/key3_COMP_370 ~/Downloads/clean_dialog.csv nbelev@3.96.148.51:~/downloads` to move our locally downloaded dialog data file to the AWS VM.  We then ssh into the VM, and move our download into `~/comp370/hw3/data` on the VM, in line with standards for data science projects.

1) Upon `cd ~/comp370/hw3/data` and `ls -lh`, we are returned:
`-rw-rw-r-- 1 nbelev nbelev 4.7M Sep 15 23:50 clean_dialog.csv`, telling us that the size of the dataset is 4.7 megabytes--not extremely large by data science standards.

2) The data is structured as lines of comma-separated values where the meaning of each of the values in the ordered line corresponds to the corresponding value in the header line, revealed with `head clean_dialog.csv` as `"title","writer","pony","dialog"`.

3) To cleverly count the number of episodes in this dataset, we first notice that the first column of data represents the title of each episode, so we want to count the number of unique titles.

    To do this we can start with the awk command: `awk -F',' '{print $1}' clean_dialog.csv` which allows us to look at only the first column for the whole CSV, just to be safe, we sort this alphabetically with `sort`, then we remove duplicates with `uniq` on this sorted column, lastly we count the number of lines with `wc -l` on the duplicate-removed set of titles.  This combines into the piped-together chain of commands as follows: `awk -F',' '{print $1}' clean_dialog.csv | sort | uniq | wc -l` which yields `197`, the total number of unique episodes, assuming our lookup is not buggy.

4) Upon observing the dialogue itself, which is the 4th value of each line of data in the CSV, we see that the ponies often refer to eachother by name, so if we're analyzing the frequency of ponies talking by looking up a name, we ought to be careful not to overcount a pony's dialogue, just because another mentions them by name in their own line of dialogue.

**Task 3**:

Twilight Sparkle: `csvtool col 3 clean_dialog.csv | grep "Twilight Sparkle" | wc -l`; produces `4831` lines of dialogue; looks for an entry / value in the third columm that contains the name Twilight Sparkle, which is likely foolproof, as even if multiple characters talk, it still catches the character in question's mention.  This same strategy should work for the other characters too.

Rarity: `csvtool col 3 clean_dialog.csv | grep "Rarity" | wc -l`; produces `2722` lines of dialogue.

Pinkie Pie: `csvtool col 3 clean_dialog.csv | grep "Pinkie Pie" | wc -l`; produces `2922` lines of dialogue.

Rainbow Dash: `csvtool col 3 clean_dialog.csv | grep "Rainbow Dash" | wc -l`; produces `3154` lines of dialogue.

Fluttershy: `csvtool col 3 clean_dialog.csv | grep "Fluttershy" | wc -l`; produces `2149` lines of dialogue.

Total lines of dialogue is given by `wc -l clean_dialog.csv`, minus 1 for the header line, so `36860` - 1 = `36859`

Using this, we calculate Total Percentages are as follows:

Twilight Sparkle: `4831` / 36859 * 100% = `13.107%`

Rarity: `2722` / 36859 * 100% = `7.385%`

Pinkie Pie: `2922` / 36859 * 100% = `7.928%`

Rainbow Dash: `3154` / 36859 * 100% = `8.557%`

Fluttershy: `2149` / 36859 * 100% = `5.830%`

Using all this annotation, we can combine the pony names, with their total grep'd lines, and their dialogue frequency (found by dividing total character lines by total lines of the dataset) into our analysis CSV.