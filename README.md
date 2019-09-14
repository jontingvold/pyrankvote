

PyRankVote —A Ranked Choice Voting System for Python
==========
[![PyPI version](https://badge.fury.io/py/pyrankvote.svg)](https://badge.fury.io/py/pyrankvote)  [![Coverage Status](https://coveralls.io/repos/github/jontingvold/pyrankvote/badge.svg?branch=master)](https://coveralls.io/github/jontingvold/pyrankvote?branch=master)  [![CircleCI](https://circleci.com/gh/jontingvold/pyrankvote/tree/master.svg?style=svg)](https://circleci.com/gh/jontingvold/pyrankvote/tree/master)

PyRankVote is a python library for different ranked-choice voting systems (sometimes called preferential voting systems) created by Jon Tingvold in June 2019.

The following ranking methods are implemented for electing one person/alternative (e.g. electing the chairman to a board):

- Instant-runoff voting (IRV)

The following ranking methods are implemented for electing multiple people/alternatives (e.g. electing board members):

- Single transferable vote (STV)
- Preferential block voting (PBV)

## Different ranking methods

**Instant runoff voting (IRV)** is a single candidate election method that elects the candidate that can obtain majority support (more than 50%).

Voters rank candidates and are granted one vote. The candidate with fewest votes is removed and this candidate's votes are transferred according to the 2nd preference (or 3rd etc.).

**Preferential block voting (PBV)** is a multiple candidate election method that elects candidates that
can obtain majority support (more than 50%). PBV tend to elect uncontroversial candidates that agree with each other. Minority group often lose their representation.

Voters rank candidates and are granted as many votes as there are people that should be elected. The candidate with
fewest votes are removed and this candidate's votes are transferred according to the 2nd preference (or 3rd etc.).

**Single transferable vote (STV)** is a multiple candidate election method that elects candidates based on proportional representation. Minority groups get representation. STV is therefore the preferred ranked-choice voting method for parliament elections. 

Voters rank candidates and are granted as one vote each. If a candidate gets more votes than the threshold for being
elected, the candidate is proclaimed as winner. This function uses the Droop quota, where

```python
droop_quota = votes/(seats+1) + 1
```

If one candidate gets more votes than the threshold the excess votes are transferred to voters that voted for this
candidate's 2nd (or 3rd, 4th, etc) alternative. If no candidate gets over the threshold, the candidate with fewest votes
is removed. Votes for this candidate is then transferred to voters 2nd (or 3rd, 4th, etc) alternative.

Preferential block voting and Single transferable vote are the same as Instant-runoff voting when only one candidate is elected.

Instant-runoff voting and Preferential block voting are basically the same as **exhaustive ballot**, the preferred method in Robers rules of order. The only difference is that in exhaustive ballot voters can adjust their preferences between each round (elimination or election of one candidate).

For more info see [pyrankvote/single_seat_ranking_methods.py](pyrankvote/single_seat_ranking_methods.py), [pyrankvote/multiple_seat_ranking_methods.py](pyrankvote/multiple_seat_ranking_methods.py) and Wikipedia.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install (or upgrade) pyrankvote.

```bash
pip install pyrankvote
```

## Usage

```python
import pyrankvote
from pyrankvote import Candidate, Ballot

trump = Candidate("Donald Trump")
hillary = Candidate("Hillary Clinton")
johnson = Candidate("Gary Johnson")

candidates = [trump, hillary, johnson]

ballots = [
    Ballot(ranked_candidates=[trump, johnson, hillary]),
    Ballot(ranked_candidates=[trump, johnson, hillary]),
    Ballot(ranked_candidates=[trump, johnson]),
    Ballot(ranked_candidates=[trump, johnson]),
    Ballot(ranked_candidates=[johnson, hillary, trump]),
    Ballot(ranked_candidates=[johnson, hillary]),
    Ballot(ranked_candidates=[hillary, johnson, trump]),
    Ballot(ranked_candidates=[hillary, johnson]),
    Ballot(ranked_candidates=[hillary, johnson])
]

# You can use your own Candidate and Ballot objects as long as they implement the same properties and methods
election_result = pyrankvote.instant_runoff_voting(candidates, ballots)

winners = election_result.get_winners()

print(election_result)

"""
ROUND 1
Candidate          Votes  Status
---------------  -------  --------
Donald Trump           4  Hopeful
Hillary Clinton        3  Hopeful
Gary Johnson           2  Hopeful

ROUND 2
Candidate          Votes  Status
---------------  -------  --------
Hillary Clinton        5  Hopeful
Donald Trump           4  Hopeful
Gary Johnson           0  Rejected

FINAL RESULT
Candidate          Votes  Status
---------------  -------  --------
Hillary Clinton        9  Elected
Donald Trump           0  Rejected
Gary Johnson           0  Rejected
"""
```

More examples in [examples.py](./examples.py)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](LICENSE.txt)