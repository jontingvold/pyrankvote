import math

from pyrankvote import models


def instant_runoff_voting(election):
    """
    Instant runoff voting (IRV) is a singe candidate election method, that elected the candidate that get draw majority
    support (more than 50%).

    IRV is the same as Preferential block voting and Single transferable vote with only one electable candidate.

    Voters rank candidates and are granted one vote. The candidate with fewest votes are removed and this voters votes
    are transfered according to the 2nd preference (or 3rd etc.).

    The method is the almost the same as *exaustive ballout*, where repetative voting rounds where everyone has just
    one vote (no ranking) and where the worst candidate is removed, until there are as many candidates left as positions
    that should be filled. This is the prefered method in Robers rules of order. The only between difference between
    IRV/PBV and exhaustive ballout, is that in exhaustive ballout voters can adjust votes according to partial results.

    For more info see Wikipedia.
    """

    if election.number_of_seats != 1:
        raise SystemError("Instant runoff voting can not be chosen if more can one winner should be elected.")

    return preferential_block_voting(election)


def preferential_block_voting(election):
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

    election.reset_race()
    em = models.ElectionManager(
        election,
        number_of_votes_pr_voter=election.number_of_seats,
        compare_method_if_equal=models.CompareMethodIfEqual.MostSecondChoiceVotes
    )

    # Remove worst candidate until same number of candidates left as electable
    # While it is more candidates left than electable
    while len(election.get_candidates_in_race()) > election.number_of_seats:
        em.update_candidate_ranking()

        last_candidate = em.get_candidate_with_least_votes_in_race()
        em.reject_candidate(last_candidate)
        em.transfer_votes(last_candidate, last_candidate.number_of_votes)

    em.update_candidate_ranking()

    winners = em.ranked_candidates_in_race
    return winners


def single_transferable_vote(election):
    """
    Single transferable vote (STV) is a multiple candidate election method, that elected the candidate that can
    based on proportional representation. Minority groups therefore get representation.

    If only one candidate can be elected, this method is the same as Instant runoff voting.

    Voters rank candidates and are granted as one vote each. If a candidate gets more votes than the threshold for being
    elected, the candidate is proclaimed as winner. This function uses the Droop quota, where

        droop_quota = votes/(seats+1) + 1

    If one candidate get more votes than the threshold the excess votes are transfered to voters that voted for this
    candidate's 2nd (or 3rd, 4th etc) alternative. If no candidate get over the threshold, the candidate with fewest votes
    are removed. Votes for this candidate is then transfered to voters 2nd (or 3rd, 4th etc) alternative.

    For more info see Wikipedia.
    """

    voters = len(election.ballots)
    seats = election.number_of_seats
    votes_needed_to_win = math.ceil(voters/float((seats+1)))  # Drop quota for fractional votes

    election.reset_race()
    em = models.ElectionManager(
        election,
        number_of_votes_pr_voter=1,
        compare_method_if_equal=models.CompareMethodIfEqual.MostSecondChoiceVotes
    )

    # Remove and distribute votes for candidates over quote or worst candidate
    # until same number of candidates left as electable
    while len(em.elected_candidates) < election.number_of_seats \
            or len(election.get_candidates_in_race()) > election.number_of_seats:

        em.update_candidate_ranking()

        winner_candidates = em.get_candidates_with_more_than_x_votes(votes_needed_to_win)
        is_winner_candidates = len(winner_candidates) > 0

        if is_winner_candidates:
            for winner_candidate in winner_candidates:
                # Transfer only excess votes to 2nd choice (or 3rd, 4th etc.)
                excess_votes = winner_candidate.number_of_votes - votes_needed_to_win

                em.elect_candidate(winner_candidate)
                em.transfer_votes(winner_candidate, excess_votes)

        else:
            last_candidate = em.get_candidate_with_least_votes_in_race()
            em.reject_candidate(last_candidate)
            em.transfer_votes(last_candidate, last_candidate.number_of_votes)

    em.update_candidate_ranking()

    winners = em.elected_candidates
    return winners
