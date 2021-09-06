"""
Single seat ranking methods

Instant runoff voting is the only implemented ranking method so far.
"""

from typing import List
from votesim.helpers import CompareMethodIfEqual, ElectionResults
from votesim.models import Candidate, Ballot
from votesim import multiple_seat_ranking_methods


def instant_runoff_voting(
    candidates: List[Candidate],
    ballots: List[Ballot],
    compare_method_if_equal=CompareMethodIfEqual.MostSecondChoiceVotes,
    pick_random_if_blank=False,
) -> ElectionResults:
    """
    Instant runoff voting (IRV), often known as the alternative vote, is a singe candidate election method,
    that elected the candidate that get draw majority support (more than 50%).

    IRV is the same as Preferential block voting and Single transferable vote with only one electable candidate.

    Voters rank candidates and are granted one vote. The candidate with fewest votes are removed and this voters votes
    are transfered according to the 2nd preference (or 3rd etc.).

    The method is the almost the same as *exaustive ballout*, where repetative voting rounds where everyone has just
    one vote (no ranking) and where the worst candidate is removed, until there are as many candidates left as positions
    that should be filled. This is the prefered method in Robers rules of order. The only between difference between
    IRV/PBV and exhaustive ballout, is that in exhaustive ballout voters can adjust votes according to partial results.

    For more info see Wikipedia.
    """

    return multiple_seat_ranking_methods.preferential_block_voting(
        candidates,
        ballots,
        number_of_seats=1,
        compare_method_if_equal=compare_method_if_equal,
        pick_random_if_blank=pick_random_if_blank,
    )
