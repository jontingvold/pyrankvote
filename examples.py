import pyrankvote
from pyrankvote import Candidate, Ballot

# ONE SEAT ELECTION: INSTANT RUNOFF VOTING

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
election_result = pyrankvote.instant_runoff_voting(candidates, ballots)

winners = election_result.get_winners()
# Returns: [<Candidate('Al Gore (Democratic)')>]

print(election_result)
# Prints:
"""
ROUND 1
Candidate                      Votes  Status
---------------------------  -------  --------
George W. Bush (Republican)        4  Hopeful
Al Gore (Democratic)               3  Hopeful
Ralph Nader (Green)                2  Hopeful

ROUND 2
Candidate                      Votes  Status
---------------------------  -------  --------
Al Gore (Democratic)               5  Hopeful
George W. Bush (Republican)        4  Hopeful
Ralph Nader (Green)                0  Rejected

FINAL RESULT
Candidate                      Votes  Status
---------------------------  -------  --------
Al Gore (Democratic)               9  Elected
George W. Bush (Republican)        0  Rejected
Ralph Nader (Green)                0  Rejected
"""


# TWO SEAT ELECTION

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

# SINGLE TRANSFERABLE VOTE

election_result = pyrankvote.single_transferable_vote(candidates, ballots, number_of_seats=2)
# Elects: William, popular moderate; and Thomas, far-left

print(election_result)
# Prints:
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
# Elects: William, popular moderate; and John, moderate

print(election_result)
# Prints:
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
