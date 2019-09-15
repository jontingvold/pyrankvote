import pyrankvote
from pyrankvote import Candidate, Ballot

# ONE SEAT ELECTION: INSTANT RUNOFF VOTING

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


# 2 SEAT ELECTION

popular_moderate = Candidate("William, popular moderate")
moderate2 = Candidate("John, moderate")
moderate3 = Candidate("Charles, moderate")
far_left = Candidate("Thomas, far-left")

candidates = [popular_moderate, moderate2, moderate3, far_left]

ballots = [
    Ballot(ranked_candidates=[popular_moderate, moderate2, moderate3, far_left]),
    Ballot(ranked_candidates=[popular_moderate, moderate2, moderate3, far_left]),
    Ballot(ranked_candidates=[popular_moderate, moderate3, moderate2, far_left]),
    Ballot(ranked_candidates=[popular_moderate, moderate3, moderate2, far_left]),
    Ballot(ranked_candidates=[moderate2, popular_moderate, moderate3, far_left]),
    Ballot(ranked_candidates=[moderate2, popular_moderate, moderate3, far_left]),

    Ballot(ranked_candidates=[far_left, popular_moderate, moderate2, moderate3]),
    Ballot(ranked_candidates=[far_left, popular_moderate, moderate2, moderate3]),
    Ballot(ranked_candidates=[far_left, moderate2, popular_moderate, moderate3]),
    Ballot(ranked_candidates=[far_left, moderate2, popular_moderate, moderate3]),
]

# INSTANT RUNOFF VOTING
election_result = pyrankvote.single_transferable_vote(candidates, ballots, number_of_seats=2)
# Elects: William, popular moderate, and Thomas, far-left
print(election_result)
"""
ROUND 1
Candidate                    Votes  Status
-------------------------  -------  --------
William, popular moderate        4  Hopeful
Thomas, far-left                 4  Hopeful
John, moderate                   2  Hopeful
Charles, moderate                0  Hopeful

FINAL RESULT
Candidate                     Votes  Status
-------------------------  --------  --------
William, popular moderate  3.33333   Elected
Thomas, far-left           3.33333   Elected
John, moderate             3         Hopeful
Charles, moderate          0.333333  Hopeful
"""

# PREFERENTIAL BLOCK VOTING
election_result = pyrankvote.preferential_block_voting(candidates, ballots, number_of_seats=2)
# Elects: William, popular moderate, and John, moderate
print(election_result)
"""
ROUND 1
Candidate                    Votes  Status
-------------------------  -------  --------
William, popular moderate        8  Hopeful
John, moderate                   6  Hopeful
Thomas, far-left                 4  Hopeful
Charles, moderate                2  Hopeful

ROUND 2
Candidate                    Votes  Status
-------------------------  -------  --------
William, popular moderate        8  Hopeful
John, moderate                   8  Hopeful
Thomas, far-left                 4  Hopeful
Charles, moderate                0  Rejected

FINAL RESULT
Candidate                    Votes  Status
-------------------------  -------  --------
John, moderate                  10  Elected
William, popular moderate       10  Elected
Thomas, far-left                 0  Rejected
Charles, moderate                0  Rejected
"""
