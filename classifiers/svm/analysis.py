import json

corpus = {}
with open("final.json","r") as fh:
    corpus = json.load(fh)

act_tags = []
topics = []

for season_episode in corpus:
    season,episode = season_episode.split("_")
    for scene in corpus[season_episode]:
        for turn in scene["Turns"]:
            print(turn["Speaker"])
            if turn["Act_Tag"][0] not in act_tags:
                act_tags.append(turn["Act_Tag"][0])
            if turn["Topics"]:
                for t in turn["Topics"]:
                    if t not in topics:
                        topics.append(t)

with open("info.json","w") as fh:
    json.dump(act_tags,fh)
with open("info1.json","w") as fh:
    json.dump(topics,fh)