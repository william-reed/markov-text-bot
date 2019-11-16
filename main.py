from random import randrange
from dataclasses import dataclass
from typing import List, Dict, Optional

# the number of tokens to use when looking backwards
GROUP_SIZE          = 2
# minimum number of tokens to use in output
MIN_OUTPUT_LENGTH   = 15
# number of phrases to generate and output
NUM_TO_GEN          = 100_000


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
        if end >= GROUP_SIZE:
            start += 1

    for g in groups:
        new_entry = g.nextToken if g.nextToken is not None else None
        if g.text not in connections:
            connections[g.text] = [new_entry]
        else:
            connections[g.text].append(new_entry)


def sanitize(raw: str) -> str:
    return raw.lower().replace("\n", "").replace('"', "")


file = open("messages.txt", "r")
lines = file.readlines()
lines = set([sanitize(s) for s in lines])

connections: Dict[str, List[str]] = {}
start_tokens: List[str] = []
for i in lines:
    parse_groups(parse_tokens(i))


output: Set[str] = set()
while len(output) < NUM_TO_GEN:
    next_token = start_tokens[randrange(0, len(start_tokens))]
    buff = []
    while next_token is not None:
        buff.append(next_token)
        prev_group = buff[-GROUP_SIZE:]
        next_connections = connections[" ".join(prev_group)]
        next_token = next_connections[randrange(0, len(next_connections))]

    if len(buff) > MIN_OUTPUT_LENGTH:
        generated = " ".join(buff)
        if generated not in lines and generated not in output:
            output.add(generated)
            print(generated)
