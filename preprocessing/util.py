'''
    We are using the fan sourced transcripts using the urls in 
    extras/episode_links.json

'''
import json
import requests
from lxml import html
import os
from os import path
import argparse

allTranscripts = {}

def getEpisodeText(season, index, episodeInfo):
    ep, title, link = episodeInfo[season][index]
    try:
        page = requests.get(link)
        tree = html.fromstring(page.content)
        p_count = tree.find_class('entrytext')[0]
    except:
        raise Exception("Failed for {ep}, {season}".format(ep=ep,season=season))    
    return p_count.text_content(),ep

def getLinksList(filename):
    try:
        with open(filename,"r") as fhandle:
            episodeInfo =  json.load(fhandle)
            fhandle.close()
        for season in episodeInfo:
            #Season is the key
            print(season)
            for idx in range(0,len(episodeInfo[season])):
                transcript,episode = getEpisodeText(season,idx,episodeInfo)
                ep_id = season+"_"+str(episode)+".txt"
                path = os.path.join("raw_corpus",ep_id)
                with open(path,"w",encoding="utf-8") as fh:
                    fh.write(transcript)
                    fh.close()
                print("Downloaded the transcripts into raw_corpus directory")
                allTranscripts[ep_id] = transcript
        with open("corpus.json","w") as corpus_file:
            json.dump(allTranscripts,corpus_file,indent=4)
            corpus_file.close()
    
    except FileNotFoundError:
        print("Could not file {fname}".format(fname=filename))

# Main Function
def main():
    parser = argparse.ArgumentParser(usage="python util.py <INPUTFILE>", description="Download the TBBT corpus")
    parser.add_argument('inputfile', help="inputfile help")
    args = parser.parse_args()
    if not args.inputfile:
        getLinksList("episode_links.json")
    else:
        getLinksList(args.inputfile)
    print("Downloaded the transcripts to raw_corpus directory")

# Entry point
if __name__ == "__main__":
    main()

