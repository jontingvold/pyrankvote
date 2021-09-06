import votesim
from votesim import Candidate, Ballot

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
    Ballot(ranked_candidates=[gore, nader]),
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

election_result = votesim.single_transferable_vote(candidates, ballots, number_of_seats=2)
# Elects: William, popular moderate; and Thomas, far-left

print(election_result)
# Prints:
"""
FINAL RESULT
Candidate                    Votes  Status
-------------------------  -------  --------
William, popular moderate        4  Elected
Thomas, far-left                 4  Elected
John, moderate                   2  Rejected
Charles, moderate                0  Rejected
"""

# PREFERENTIAL BLOCK VOTING

election_result = votesim.preferential_block_voting(candidates, ballots, number_of_seats=2)
# Elects: William, popular moderate; and John, moderate

print(election_result)
# Prints:
"""
FINAL RESULT
Candidate                    Votes  Status
-------------------------  -------  --------
William, popular moderate        8  Elected
John, moderate                   6  Elected
Thomas, far-left                 4  Rejected
Charles, moderate                2  Rejected
"""

#   COMMENT
#
#   As you can see PBV produces moderate candidates all agree on.
#   While STV produces representative candidates that better reflect the different voting groups.
