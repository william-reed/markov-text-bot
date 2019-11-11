from random import randrange
from dataclasses import dataclass
from typing import List, Dict, Optional

MAX_GROUP_SIZE = 2


@dataclass
class Group:
    text: str
    nextToken: Optional[str]


def parse_tokens(text: str) -> List[str]:
    split = text.split(' ')
    start_tokens.append(split[0])
    return split


def parse_groups(tokens: List[str]) -> None:
    start = 0
    groups: List[Group] = []

    for end in range(1, len(tokens) + 1):
        groups.append(
            Group(
                " ".join([t for t in tokens[start:end]]),
                tokens[end] if (end < len(tokens)) else None
            )
        )

        # increment
        if end >= MAX_GROUP_SIZE:
            start += 1

    for g in groups:
        new_entry = g.nextToken if g.nextToken is not None else None
        if g.text not in connections:
            connections[g.text] = [new_entry]
        else:
            connections[g.text].append(new_entry)


def sanitize(raw: str) -> str:
    return raw.lower().replace("\n", "").replace('"', "")


file = open("pics-10k.txt", "r")
lines = file.readlines()
lines = [sanitize(s) for s in lines]

connections: Dict[str, List[str]] = {}
start_tokens: List[str] = []
for i in lines:
    parse_groups(parse_tokens(i))

# print(connections)
# print(start_tokens)

for i in range(0, 1000):
    next_token = start_tokens[randrange(0, len(start_tokens))]
    buff = []
    while next_token is not None:
        buff.append(next_token)
        prev_group = buff[-MAX_GROUP_SIZE:]
        next_connections = connections[" ".join(prev_group)]
        next_token = next_connections[randrange(0, len(next_connections))]

    print(" ".join(buff))
