import pandas as pd

paths = [
    ["YouTube", "Meta", "Conversion"],
    ["TV", "YouTube", "Conversion"],
    ["Meta", "Conversion"]
]

def markov_attribution(paths):
    transitions = {}
    for path in paths:
        for i in range(len(path)-1):
            pair = (path[i], path[i+1])
            transitions[pair] = transitions.get(pair, 0) + 1

    df = pd.DataFrame(
        [(k[0], k[1], v) for k,v in transitions.items()],
        columns=["from", "to", "count"]
    )

    contribution = df.groupby("from")["count"].sum()
    total = contribution.sum()

    return (contribution / total).to_dict()
