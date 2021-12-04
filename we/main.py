"""
The goal was to find some pairs for white elephant gifts, with some constraints:
one person can not do a gift for its spouse.

So this is a brute force way of finding a result.
"""
import json
import logging
import pprint
import sys
from random import randrange
from typing import Tuple, List, Optional, Dict, Set, io


def find_pairs(people: Dict[str, Set[str]]) -> Optional[List[Tuple[str, str]]]:
    already_drawn = set()
    pairs = []

    for person, forbidden_matches in people.items():
        logging.debug("looking a pair for %s", person)
        match = find_match(
            list(people.keys()),
            # a person can not match itself, nor anyone already drawn, nor any of the initial constraints
            forbidden_matches.union(already_drawn, {person})
        )
        if not match:
            logging.warning(
                "unable to find a match for %s, already drawn %s, people %s, constraint %s",
                person,
                already_drawn,
                people,
                forbidden_matches
            )
            return None

        already_drawn.add(match)
        pairs.append((person, match))

    return pairs


def find_match(people: List[str],
               forbidden_matches: Set[str]) -> Optional[str]:
    number_of_people = len(people)
    match_index = randrange(number_of_people)

    # we will get an index, and if this person is not a match, as it might
    # been in the forbidden match
    for idx in range(number_of_people):
        possible_match = people[(match_index + idx) % number_of_people]
        if possible_match not in forbidden_matches:
            return possible_match
        else:
            logging.debug("the match %s is forbidden, so let's try to loop", possible_match)

    return None


def draw(people: Dict[str, Set[str]]):
    try_count = 0
    while try_count < MAX_TRY:
        logging.debug("== Attempt no %d", try_count)
        result = find_pairs(people)
        if result:
            logging.info(u"🎉 One result has been found:\n%s", pprint.pformat(result))
            return

        logging.debug("unable to find a result")
        try_count += 1

    logging.info(u"too many tries without any result found 😞")


MAX_TRY = 10


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s : "
           "%(lineno)d - %(message)s"
)


def print_usage(prog_name: str):
    print(f'''An input file containing the people needs to be specified.

usage: python {prog_name} <file>

example of a valid file:
{{
    "Augustin": ["Anna"],
    "Anna": ["Augustin"],
    "Sam": [],
    "Elo": ["Arnaud"],
    "Arnaud": ["Elo"]
}}
''')


def parse(file: io.TextIO) -> Dict[str, Set[str]]:
    raw_people = json.load(file)
    return {
        person: set(forbidden_list)
        for person, forbidden_list in raw_people.items()
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage(sys.argv[0])
        sys.exit(-1)

    with open(sys.argv[1]) as _file:
        _people = parse(_file)

    draw(_people)
