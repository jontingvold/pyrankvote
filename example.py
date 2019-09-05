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
