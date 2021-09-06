"""
Multiple seat ranking methods

Implemented methods:
 - Single transferable vote
 - Preferential block voting
"""

from typing import List
from votesim.helpers import CompareMethodIfEqual, ElectionManager, ElectionResults
from votesim.models import Candidate, Ballot
import math


def preferential_block_voting(
    candidates: List[Candidate],
    ballots: List[Ballot],
    number_of_seats: int,
    compare_method_if_equal=CompareMethodIfEqual.MostSecondChoiceVotes,
    pick_random_if_blank=False,
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

    rounding_error = 1e-6

    manager = ElectionManager(
        candidates,
        ballots,
        number_of_votes_pr_voter=number_of_seats,
        compare_method_if_equal=compare_method_if_equal,
        pick_random_if_blank=pick_random_if_blank,
    )
    election_results = ElectionResults()

    # Remove worst candidate until same number of candidates left as electable
    # While it is more candidates left than electable
    while True:
        majority_limit = math.ceil(manager.get_number_of_non_exhausted_ballots() / 2.0)

        seats_left = number_of_seats - manager.get_number_of_elected_candidates()
        candidates_in_race = manager.get_candidates_in_race()
        candidates_in_race_votes: List[float] = [
            manager.get_number_of_votes(candidate) for candidate in candidates_in_race
        ]

        votes_remaining = sum(candidates_in_race_votes)
        last_votes = 0.0
        candidates_to_elect = []
        candidates_to_reject = []

        for i, candidate in enumerate(candidates_in_race):
            votes_for_candidate = candidates_in_race_votes[i]
            is_last_candidate = i == len(candidates_in_race) - 1

            # Elect candidates with a majority
            if (votes_for_candidate - rounding_error) >= majority_limit:
                candidates_to_elect.append(candidate)

            # Reject candidates that even with redistribution can't change the results
            elif i >= seats_left and (votes_remaining - rounding_error) <= last_votes:
                candidates_to_reject.append(candidate)

            elif is_last_candidate:
                # Should be catched by if statement above
                raise RuntimeError("Illigal state")

            last_votes = votes_for_candidate
            votes_remaining -= votes_for_candidate

        for candidate in candidates_to_elect:
            manager.elect_candidate(candidate)

        for candidate in candidates_to_reject[::-1]:
            manager.reject_candidate(candidate)

        # If same number of seats left as there are candidates, elect all candidates
        seats_left = number_of_seats - manager.get_number_of_elected_candidates()
        if manager.get_number_of_candidates_in_race() <= seats_left:
            for candidate in manager.get_candidates_in_race():
                candidates_to_elect.append(candidate)
                manager.elect_candidate(candidate)

        # If no seats left, reject the rest of the candidates
        seats_left = number_of_seats - manager.get_number_of_elected_candidates()
        if seats_left == 0:
            for candidate in manager.get_candidates_in_race()[::-1]:
                candidates_to_reject.append(candidate)
                manager.reject_candidate(candidate)

        # Register round result
        election_results.register_round_results(manager.get_results())

        # If all seats filled
        if manager.get_number_of_candidates_in_race() == 0:
            break

        else:
            # For voters who voted on rejected candidates,
            # transfer votes to 2nd choice (or 3rd, 4th etc.)
            for candidate in candidates_to_reject:
                number_of_votes = manager.get_number_of_votes(candidate)
                manager.transfer_votes(candidate, number_of_votes)

            # New round
            continue

    return election_results


def single_transferable_vote(
    candidates: List[Candidate],
    ballots: List[Ballot],
    number_of_seats: int,
    compare_method_if_equal=CompareMethodIfEqual.MostSecondChoiceVotes,
    pick_random_if_blank=False,
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

    rounding_error = 1e-6

    manager = ElectionManager(
        candidates,
        ballots,
        number_of_votes_pr_voter=1,
        compare_method_if_equal=compare_method_if_equal,
        pick_random_if_blank=pick_random_if_blank,
    )
    election_results = ElectionResults()

    voters, seats = manager.get_number_of_non_exhausted_ballots(), number_of_seats
    votes_needed_to_win: float = voters / float((seats + 1))  # Drop quota

    # Remove worst candidate until same number of candidates left as electable
    # While it is more candidates left than electable
    while True:
        seats_left = number_of_seats - manager.get_number_of_elected_candidates()
        candidates_in_race = manager.get_candidates_in_race()
        candidates_in_race_votes: List[float] = [
            manager.get_number_of_votes(candidate) for candidate in candidates_in_race
        ]

        votes_remaining = sum(candidates_in_race_votes)
        last_votes = 0.0
        candidates_to_elect = []
        candidates_to_reject = []

        for i, candidate in enumerate(candidates_in_race):
            votes_for_candidate = candidates_in_race_votes[i]
            is_last_candidate = i == len(candidates_in_race) - 1

            # Elect candidates with more votes than Drop quota
            if (votes_for_candidate - rounding_error) >= votes_needed_to_win:
                candidates_to_elect.append(candidate)

            # Reject candidates that even with redistribution can't change the results
            elif i >= seats_left and (votes_remaining - rounding_error) <= last_votes:
                if len(candidates_to_elect) > 0:
                    # Don't reject candidates if there are elected candidates that have not yet
                    # redistributed their votes
                    break
                else:
                    candidates_to_reject.append(candidate)

            elif is_last_candidate:
                # Should be catched by if statement above
                raise RuntimeError("Illigal state")

            last_votes = votes_for_candidate
            votes_remaining -= votes_for_candidate

        for candidate in candidates_to_elect:
            manager.elect_candidate(candidate)

        for candidate in candidates_to_reject[::-1]:
            manager.reject_candidate(candidate)

        # If same number of seats left as there are candidates, elect all candidates
        seats_left = number_of_seats - manager.get_number_of_elected_candidates()
        if manager.get_number_of_candidates_in_race() <= seats_left:
            for candidate in manager.get_candidates_in_race():
                candidates_to_elect.append(candidate)
                manager.elect_candidate(candidate)

        # If no seats left, reject the rest of the candidates
        seats_left = number_of_seats - manager.get_number_of_elected_candidates()
        if seats_left == 0:
            for candidate in manager.get_candidates_in_race()[::-1]:
                candidates_to_reject.append(candidate)
                manager.reject_candidate(candidate)

        # Register round result
        election_results.register_round_results(manager.get_results())

        # If all seats filled
        if manager.get_number_of_candidates_in_race() == 0:
            break

        else:
            # For voters who votes for elected candidates,
            # transfer excess votes to 2nd choice (or 3rd, 4th etc.)
            for candidate in candidates_to_elect:
                votes_for_candidate = manager.get_number_of_votes(candidate)
                excess_votes: float = votes_for_candidate - votes_needed_to_win
                manager.transfer_votes(candidate, excess_votes)

            # For votes who votes on rejected candidates,
            # transfer all votes to 2nd choice (or 3rd, 4th etc.)
            for candidate in candidates_to_reject:
                votes_for_candidate = manager.get_number_of_votes(candidate)
                manager.transfer_votes(candidate, votes_for_candidate)

            # New round
            continue

    return election_results
