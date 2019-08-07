

PyRankVote - A Ranked Choice Voting System for Python
=====================================================

PyRankVote is a python library for different ranked-choice voting systems (sometimes called preferential voting systems) created by Jon Tingvold. 

The following ranking methods are implemented for electing one person/alternative (e.g. electing the chairman to a board):

- Instant-runoff voting (IRV)

The following ranking methods are implemented for electing multiple people/alternatives (e.g. electing board members):

- Single transferable vote (STV)
- Preferential block voting (PBV)

You can read about the different ranking methods in [pyrankvote/ranking_methods.py](pyrankvote/ranking_methods.py).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install (or upgrade) pyrankvote.

```bash
pip install git+https://github.com/jontingvold/pyrankvote.git
```

## Usage

```python
import pyrankvote

election = pyrankvote.Election(number_of_seats=2)
election.add_candidate("Per")
election.add_candidate("Pål")
election.add_candidate("Askeladden")

per, paal, askeladden = election.get_candidates()
election.register_ballot(ranked_candidates=[askeladden, per])
election.register_ballot(ranked_candidates=[per, paal])
election.register_ballot(ranked_candidates=[per, paal])
election.register_ballot(ranked_candidates=[paal, per])
election.register_ballot(ranked_candidates=[paal, per, askeladden])

winners = pyrankvote.ranking_methods.single_transferable_vote(election)

print(winners)  # [Candidate(name='Per'), Candidate(name='Pål')]
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)