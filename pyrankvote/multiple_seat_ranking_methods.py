"""
Multiple seat ranking methods

Implemented methods:
 - Single transferable vote
 - Preferential block voting
"""

from typing import List
from pyrankvote.helpers import CompareMethodIfEqual, ElectionManager, ElectionResults
from pyrankvote.models import Candidate, Ballot


def preferential_block_voting(candidates: List[Candidate], ballots: List[Ballot], number_of_seats: int,
                              compare_method_if_equal=CompareMethodIfEqual.MostSecondChoiceVotes
                              ) -> ElectionResults:
    """
    Preferential block voting (PBV) is a multiple candidate election method, that elected the candidate that can
    draw majority support (more than 50%). Minority groups therefore lose their representation.

    If only one candidate can be elected, this method is the same as Instant runoff voting.

    Voters rank candidates and are granted as many votes as there are people that should be elected. The candidate with
    fewest votes are removed and this voters votes are transfered according to the 2nd preference (or 3rd etc.).

    The method is the same as *exaustive ballout*, where repetative voting rounds where everyone has just one vote (no ranking) and
    where the worst candidate is removed, until there are as many candidates left as positions that should be filled.
    This is the prefered method in Robers rules of order. The only between difference between IRV/PBV and exhaustive ballout,
    is that in exhaustive ballout voters can adjust votes according to partial results.

    For more info see Wikipedia.
    """

    manager = ElectionManager(
        candidates,
        ballots,
        number_of_votes_pr_voter=number_of_seats,
        compare_method_if_equal=compare_method_if_equal
    )
    election_results = ElectionResults()

    # Remove worst candidate until same number of candidates left as electable
    # While it is more candidates left than electable
    while manager.get_number_of_candidates_in_race() > number_of_seats:
        # Register partial result
        election_results.register_round_results(manager.get_results())

        last_candidate = manager.get_candidate_with_least_votes_in_race()
        manager.reject_candidate(last_candidate)

        number_of_votes: float = manager.get_number_of_votes(last_candidate)
        manager.transfer_votes(last_candidate, number_of_votes)

    # The last candidates standing are winners
    for candidate in manager.get_candidates_in_race():
        manager.elect_candidate(candidate)

    # Register final result
    election_results.register_round_results(manager.get_results())

    return election_results


def single_transferable_vote(candidates: List[Candidate], ballots: List[Ballot], number_of_seats: int,
                             compare_method_if_equal=CompareMethodIfEqual.MostSecondChoiceVotes
                             ) -> ElectionResults:
    """
    Single transferable vote (STV) is a multiple candidate election method, that elected the candidate that can
    based on proportional representation. Minority groups therefore get representation.

    If only one candidate can be elected, this method is the same as Instant runoff voting.

    Voters rank candidates and are granted as one vote each. If a candidate gets more votes than the threshold for being
    elected, the candidate is proclaimed as winner. This function uses the Droop quota, where

        droop_quota = votes/(seats+1)

    If one candidate get more votes than the threshold the excess votes are transfered to voters that voted for this
    candidate's 2nd (or 3rd, 4th etc) alternative. If no candidate get over the threshold, the candidate with fewest votes
    are removed. Votes for this candidate is then transfered to voters 2nd (or 3rd, 4th etc) alternative.

    For more info see Wikipedia.
    """

    voters = len(ballots)
    seats = number_of_seats
    drop_quota: int = voters/float((seats+1))
    votes_needed_to_win = drop_quota

    manager = ElectionManager(
        candidates,
        ballots,
        number_of_votes_pr_voter=1,
        compare_method_if_equal=compare_method_if_equal
    )
    election_results = ElectionResults()

    # Elect candidates with more votes than quota and redistribute excess votes
    # and remove worst candidate and redistribute votes
    # until all seats filled
    while manager.get_number_of_elected_candidates() < number_of_seats:

        # Register partial result
        election_results.register_round_results(manager.get_results())

        number_of_seats_left = number_of_seats - manager.get_number_of_elected_candidates()
        if manager.get_number_of_candidates_in_race() == number_of_seats_left:
            # Elect all candidates left in race
            for candidate in manager.get_candidates_in_race():
                manager.elect_candidate(candidate)
            break

        winner_candidates = manager.get_candidates_with_more_than_x_votes(votes_needed_to_win)

        if len(winner_candidates) > 0:
            for winner_candidate in winner_candidates:
                # Transfer only excess votes to 2nd choice (or 3rd, 4th etc.)
                number_of_votes: float = manager.get_number_of_votes(winner_candidate)
                excess_votes: float = number_of_votes - votes_needed_to_win

                manager.elect_candidate(winner_candidate)
                manager.transfer_votes(winner_candidate, excess_votes)

        else:
            last_candidate = manager.get_candidate_with_least_votes_in_race()
            manager.reject_candidate(last_candidate)

            number_of_votes: float = manager.get_number_of_votes(last_candidate)
            manager.transfer_votes(last_candidate, number_of_votes)

    # Register final result
    election_results.register_round_results(manager.get_results())

    return election_results
