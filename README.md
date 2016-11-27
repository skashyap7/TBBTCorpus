# TBBTCorpus
The Big Bang Theory Transcript Corpus

# Downloading Corpus

We used fan-sourced transcripts for The Big Bang Theory as data set for our experiment. The Blog site had transcripts for the 9 season ( 220 scenes ) of The Big Bang Theory, categorized by season and episode. One of the first task was to extract transcripts from these webpages.

### Scripts

We manually constructed a list of links of all URL's. Using this list
content was scraped from the web and only relevant text was extracted
and dumped into text format under corpus/raw_corpus directory.

You can run util.py to reproduce this corpus. By default it uses the file
episode_links.json for list the links.

    python util.py episode_links.json 

Requires lxml and requests python module

You can run preprocessing.py to perform preprocessing on the data.This script requires
corpus.json

    python preprocessing.py

The previous step of util.py creates a corpus.json which is JSON representation of season
/episode categorized transcript

# Processing Corpus

A single episode transcript is of the form

    [Scene]
    SpeakerA : ***Some Text***
    SpeakerB : ***Some Text***
    SpeakerC : ***Some Text***
    ...
    ...
    ...
    [Scene]
    SpeakerA : ***Some Text***
    SpeakerB : ***Some Text***
    SpeakerC : ***Some Text***
    ...
    ...
    ...

### Challenges with processing 
- We treat every Scene as distinct unit to be processed. Theoretically, a scene change
occurs even when new characters enter or exit. However, for our corpus, there were only
13 turns that had enters and 18 that had exits of the total 1028000 turns and hence we 
decided ignore splitting the scene when a character enters or exits. 

    There were instances when they made sense for e.g
    > Penny (as Sheldon enters): Shh! Act normal.
    
    While instances when they had no relevance for e.g.
    > Leonard (entering on the phone): I’m really very busy. Is there any way that we can put this off 

- Another challenge were instances where extra attributes being mentioned along with
speaker information. This extra information needed to removed to capture the speaker
name. We could have used Named Entity Recognition for this, but we used the naive approach
to parse for brackets and ignore any content within the brackets.This has worked fine for us.

    for e.g.
    > Speaker: Penny( Sitting quitely): 

    resulted in capturing speaker as Penny

- As not all speakers had enough dialogues, to identify the character, we needed to define
the subset of characters to be considered as classification label. We wrote additional script
to analyze the # of dialogues by each character. We chose a threshold of 4 to decide the main
classification labels. We included an extra label for all other characters clubbed together as
"Others". Hence each dialogue can be classified to be spoken by one of the five characters in 
our case ["Leonard","Sheldon","Penny", "Howard","Others"]


>
    | Character     | Dialogues   |
    |---------------|------------:|
    |Sheldon        |    164415   |
    |Leonard        |     94143   |
    |Penny          |     73147   |
    |Howard         |     62951   |
    |Raj            |     50924   |
    |Amy            |     32641   |

For each scene we capture
* Scene Description
* Season_Episode
* List of Turns (Turn Object)
* List of Participants ( Names of Characters present in the turn)

For each turn (Turn Object) we capture
* Speaker
* Recipients
* List of words(after removing stop words) in the turn (utterance)
* POS tag for each word 
* Topic associated with the turn (Topic extracted using LDA model)
* ACT Tag 

We save list of scenes per episode in a JSON format, where each
episode in a season has a key of season_episode. Additionally, it also
generated a JSON file for the unique words over the entire corpus with 
key as the lemmatized word and value as occurence frequency.This can be
useful for topic extraction.

We use nltk toolkit to remove stop words and 

Please see [corpus reader tool](http://www.google.com), [ train and classify methods](http://www.google.com) &
[evaluation methods](http://www.google.com) for more information on the next steps
