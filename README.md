

votesim —A Ranked Choice Voting System for Python
==========
[![PyPI version](https://badge.fury.io/py/votesim.svg)](https://badge.fury.io/py/votesim) ![Test status](https://github.com/jontingvold/votesim/workflows/CI/badge.svg?branch=master)  [![Coverage Status](https://coveralls.io/repos/github/jontingvold/votesim/badge.svg?branch=master)](https://coveralls.io/github/jontingvold/votesim?branch=master)

votesim is a python library for election voting. It was forked from [PyRankVote](https://github.com/jontingvold/pyrankvote).

The following ranking methods are implemented for electing one person/alternative (e.g. electing the chairman to a board):

- Instant-runoff voting (IRV)—often known as the alternative vote

The following ranking methods are implemented for electing multiple people/alternatives (e.g. electing board members):

- Single transferable vote (STV)—generally preferred
- Preferential block voting (PBV)

## Different ranking methods

**Instant runoff voting (IRV)** is a single candidate election method that elects the candidate that can obtain majority support (more than 50%).

Voters rank candidates and are granted one vote. The candidate with fewest votes is removed and this candidate's votes are transferred according to the voters 2nd preference (or 3rd etc).

**Preferential block voting (PBV)** is a multiple candidate election method that elects candidates that
can obtain majority support (more than 50%). PBV tends to elect uncontroversial candidates that agree with each other. Minority group often lose their representation.

Voters rank candidates and are granted as many votes as there are people that should be elected. The candidate with
fewest votes are removed and this candidate's votes are transferred according to the voters 2nd preference (or 3rd etc).

**Single transferable vote (STV)** is a multiple candidate election method that elects candidates based on proportional representation. Minority (and extreme) groups get representation if they have enough votes to elect a candidate. STV is therefore the preferred ranked-choice voting method for parliament elections and most multiple seat elections, but it's more complex than  PBV, so it explained last.

Voters rank candidates and are granted as one vote each. If a candidate gets more votes than the threshold for being
elected, the candidate is proclaimed as winner. This function uses the Droop quota, where

```python
droop_quota = votes/(seats+1) + 1
```

If one candidate gets more votes than the threshold the excess votes are transferred to voters that voted for this
candidate's 2nd (or 3rd, 4th, etc) alternative. If no candidate gets over the threshold, the candidate with fewest votes
is removed. Votes for this candidate is then transferred to voters 2nd (or 3rd, 4th, etc) alternative.

Preferential block voting and Single transferable vote are the same as Instant-runoff voting when only one candidate is elected.

Instant-runoff voting and Preferential block voting are basically the same as **exhaustive ballot**, the preferred method in Rober's rules of order. The only difference is that in exhaustive ballot voters can adjust their preferences between each round (elimination or election of one candidate).

For more info:

- [votesim/single_seat_ranking_methods.py](votesim/single_seat_ranking_methods.py) and  [votesim/multiple_seat_ranking_methods.py](votesim/multiple_seat_ranking_methods.py)
- Wikipedia: [IRV](https://en.wikipedia.org/wiki/Instant-runoff_voting), [STV](https://en.wikipedia.org/wiki/Single_transferable_vote), [PBV](https://en.wikipedia.org/wiki/Preferential_block_voting), [exhaustive ballot](https://en.wikipedia.org/wiki/Exhaustive_ballot)
- CGP Gray's YouTube videos: [IRV](https://www.youtube.com/watch?v=3Y3jE3B8HsE), [STV1](https://www.youtube.com/watch?v=l8XOZJkozfI&t=2s), [STV2](https://www.youtube.com/watch?v=Ac9070OIMUg), [STV3](https://www.youtube.com/watch?v=wRc630BSTIg)

## Installation

With pip package manager:

```bash
pip install votesim
```

## Usage

```python
import votesim
from votesim import Candidate, Ballot

bush = Candidate("George W. Bush (Republican)")
gore = Candidate("Al Gore (Democratic)")
nader = Candidate("Ralph Nader (Green)")

candidates = [bush, gore, nader]

# Bush have most first choice votes, but because Ralph Nader-voters want
# Al Gore if Nader is not elected, the elected candidate is Al Gore
ballots = [
    Ballot(ranked_candidates=[bush, nader, gore]),
    Ballot(ranked_candidates=[bush, nader, gore]),
    Ballot(ranked_candidates=[bush, nader]),
    Ballot(ranked_candidates=[bush, nader]),
    Ballot(ranked_candidates=[nader, gore, bush]),
    Ballot(ranked_candidates=[nader, gore]),
    Ballot(ranked_candidates=[gore, nader, bush]),
    Ballot(ranked_candidates=[gore, nader]),
    Ballot(ranked_candidates=[gore, nader])
]

# You can use your own Candidate and Ballot objects as long as they implement the same properties and methods
election_result = votesim.instant_runoff_voting(candidates, ballots)

winners = election_result.get_winners()
# Returns: [<Candidate('Al Gore (Democratic)')>]

print(election_result)
# Prints:
"""
ROUND 1
Candidate                      Votes  Status
---------------------------  -------  --------
George W. Bush (Republican)        4  Active
Al Gore (Democratic)               3  Active
Ralph Nader (Green)                2  Rejected

FINAL RESULT
Candidate                      Votes  Status
---------------------------  -------  --------
Al Gore (Democratic)               5  Elected
George W. Bush (Republican)        4  Rejected
Ralph Nader (Green)                0  Rejected
"""
```

More examples in [examples.py](./examples.py)

## License
[MIT](LICENSE.txt)
