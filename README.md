

PyRankVote - A Ranked Choice Voting System for Python
=====================================================

PyRankVote is a python library for different ranked-choice voting systems (sometimes called preferential voting systems) created by Jon Tingvold in June 2019. 

The following ranking methods are implemented for electing one person/alternative (e.g. electing the chairman to a board):

- Instant-runoff voting (IRV)

The following ranking methods are implemented for electing multiple people/alternatives (e.g. electing board members):

- Single transferable vote (STV)
- Preferential block voting (PBV)

## Different ranking methods

**Instant runoff voting (IRV)** is a singe candidate election method, that elected the candidate that get draw majority support (more than 50%).

Voters rank candidates and are granted one vote. The candidate with fewest votes are removed and this candidates votes are transfered according to the 2nd preference (or 3rd etc.).

**Preferential block voting (PBV)** is a multiple candidate election method, that electes candidates that
can obtain majority support (more than 50%). Minority groups therefore lose their representation.

Voters rank candidates and are granted as many votes as there are people that should be elected. The candidate with
fewest votes are removed and this candidates votes are transfered according to the 2nd preference (or 3rd etc.).

**Single transferable vote (STV)** is a multiple candidate election method, that elects candidates based on proportional representation. Minority groups therefore get representation.

Voters rank candidates and are granted as one vote each. If a candidate gets more votes than the threshold for being
elected, the candidate is proclaimed as winner. This function uses the Droop quota, where

    droop_quota = votes/(seats+1) + 1

If one candidate get more votes than the threshold the excess votes are transfered to voters that voted for this
candidate's 2nd (or 3rd, 4th etc) alternative. If no candidate get over the threshold, the candidate with fewest votes
are removed. Votes for this candidate is then transfered to voters 2nd (or 3rd, 4th etc) alternative.

Preferential block voting and Single transferable vote is the same as Instant-runoff voting when only one candidate is elected.

Instant-runoff voting and Preferential block voting is basicly the same as **exaustive ballout**, the prefered method in Robers rules of order. The only difference is that in exaustive ballout voters can adjust their preferences between each round (elimination or election of one candidate).

For more info see [pyrankvote/ranking_methods.py](pyrankvote/ranking_methods.py) and Wikipedia.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install (or upgrade) pyrankvote.

```bash
pip install git+https://github.com/jontingvold/pyrankvote.git
```

## Usage

```python
import pyrankvote
from pyrankvote.models import Candidate, Ballot

per = Candidate("Per")
paal = Candidate("Pål")
askeladden = Candidate("Askeladden")

candidates = [per, paal, askeladden]

ballots = [
    Ballot(ranked_candidates=[askeladden, per]),
    Ballot(ranked_candidates=[per, paal]),
    Ballot(ranked_candidates=[per, paal]),
    Ballot(ranked_candidates=[paal, per]),
    Ballot(ranked_candidates=[paal, per, askeladden])
]

election_result = pyrankvote.multiple_seat_ranking_methods.single_transferable_vote(candidates, ballots, number_of_seats=2)

winners = election_result.get_winners()

print(election_result)

"""
ROUND 1
Candidate      Votes  Status
-----------  -------  --------
Per                2  Hopeful
Pål                2  Hopeful
Askeladden         1  Hopeful


ROUND 2
Candidate      Votes  Status
-----------  -------  --------
Per                3  Hopeful
Pål                2  Hopeful
Askeladden         0  Rejected


FINAL RESULT
Candidate      Votes  Status
-----------  -------  --------
Per                3  Elected
Pål                2  Elected
Askeladden         0  Rejected
"""

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
