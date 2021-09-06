"""
Helper classes used by multiple_seat_ranking_methods.py

"""
from votesim.models import Candidate, Ballot

import random
import functools
from typing import Dict, List, NamedTuple
from tabulate import tabulate


CONSIDERED_EQUAL_MARGIN = 0.001


def almost_equal(value1: float, value2: float) -> bool:
    return abs(value1 - value2) < CONSIDERED_EQUAL_MARGIN


class CandidateStatus:
    Elected = "Elected"
    Active = "Active"
    Rejected = "Rejected"


class CandidateResult(NamedTuple):
    candidate: Candidate
    number_of_votes: float
    status: CandidateStatus


class RoundResult:
    candidate_results: List[CandidateResult]
    number_of_blank_votes: float

    def __init__(self, candidate_results, number_of_blank_votes):
        self.candidate_results = candidate_results
        self.number_of_blank_votes = number_of_blank_votes

    def __repr__(self):
        representation_string = "<RoundResult>"
        return representation_string

    def __str__(self):
        if almost_equal(self.number_of_blank_votes, 0.0):
            results_with_blank_votes = self.candidate_results
        else:
            blank_votes_as_candidate_results = [("Blank votes", self.number_of_blank_votes, CandidateStatus.Rejected)]
            results_with_blank_votes = self.candidate_results + blank_votes_as_candidate_results

        all_integers = all([float(candidateResult[1]).is_integer() for candidateResult in results_with_blank_votes])
        if all_integers:
            float_format = ".0f"
        else:
            float_format = ".2f"

        pretty_print_string = tabulate(
            results_with_blank_votes, headers=["Candidate", "Votes", "Status"], floatfmt=float_format
        )

        return pretty_print_string


class CandidateVoteCount:
    def __init__(self, candidate: Candidate):
        self.candidate = candidate
        self.status = CandidateStatus.Active

        self.number_of_votes = 0.0
        self.votes: List[Ballot] = []

    @property
    def is_in_race(self) -> bool:
        return self.status == CandidateStatus.Active

    def as_candidate_result(self) -> CandidateResult:
        return CandidateResult(self.candidate, self.number_of_votes, self.status)

    def __repr__(self) -> str:
        return "<CandidateVoteCount(candidate='%s, votes=%.2f')>" % (self.candidate.name, self.number_of_votes)


class CompareMethodIfEqual:
    Random = "Random"
    MostSecondChoiceVotes = "MostSecondChoiceVotes"


class NoCandidatesLeftInRaceError(RuntimeError):
    pass


class ElectionManager:
    """
    ElectionManager is a abstract class that take care of managing the counting of votes.
    It implements common functionality among the ranking methods.

    ElectionManager is initialized by giving it the list of candidates and ballots,
    and configure settings like number of votes each person has (used in preferential block voting)
    and what to do if two voters have the same number of votes. It can then ether choose to
    rank candidates based on the voters who has most second choice votes (and if equal third
    choice votes, fourth etc.) or just choose randomly.

    After initialization ranking methods can get the ranked candidates list, elect or reject a candidate,
    or distribute a part of the number of votes of one candidate to the second choices to the voters that voted
    for this candidate. The last method is used, among other things, by Single Transferable Votes to distribute
    excess votes if a candidate gets more votes than necessary. That way even if many people voted for this
    candidate, the votes are still useful.

    transfer_votes(..) and other methods that effects the proper ranking of candidates, re-sorts
    the ranking of candidates, so _candidates_in_race should always be properly sorted.
    """

    def __init__(
        self,
        candidates: List[Candidate],
        ballots: List[Ballot],
        number_of_votes_pr_voter=1,
        compare_method_if_equal=CompareMethodIfEqual.MostSecondChoiceVotes,
        pick_random_if_blank=False,
    ):

        self._ballots = ballots
        self._candidate_vote_counts: Dict[Candidate:CandidateVoteCount] = {
            candidate: CandidateVoteCount(candidate) for candidate in candidates
        }

        self._candidates_in_race: List[CandidateVoteCount] = list(self._candidate_vote_counts.values())
        self._elected_candidates: List[CandidateVoteCount] = []  # Sorted asc by election round
        self._rejected_candidates: List[CandidateVoteCount] = []  # Sorted desc by election round
        self._exhausted_ballots: List[Ballot] = []  # Blank and exhausted ballots (all alternatives used up)
        self._number_of_blank_votes = 0.0

        self._number_of_candidates = len(candidates)
        self._number_of_votes_pr_voter = number_of_votes_pr_voter
        self._compare_method_if_equal = compare_method_if_equal
        self._pick_random_if_blank = pick_random_if_blank

        # Distribute votes to the most preferred candidates (before any candidates are elected or rejected)
        for ballot in ballots:
            # If one vote per voter -> Voters vote goes to the first candidate on the ranked list
            # If more than one vote per voter -> Voters votes goes to the x first candidates on the ranked list
            candidates_that_should_be_voted_on = ballot.ranked_candidates[0:number_of_votes_pr_voter]

            number_of_blank_votes = number_of_votes_pr_voter - len(ballot.ranked_candidates)
            if number_of_blank_votes > 0:
                if self._pick_random_if_blank:
                    candidates_that_should_be_voted_on = list(candidates_that_should_be_voted_on)
                    for _ in range(number_of_blank_votes):
                        new_candidate_choice = random.choice(candidates)
                        candidates_that_should_be_voted_on.append(new_candidate_choice)
                else:
                    self._exhausted_ballots.append(ballot)
                    self._number_of_blank_votes += number_of_blank_votes

            for candidate in candidates_that_should_be_voted_on:
                candidate_vc = self._candidate_vote_counts[candidate]
                candidate_vc.number_of_votes += 1
                candidate_vc.votes.append(ballot)

        # After votes are distributed -> sort candidates
        # This is also done each time transfer_votes(...) is called
        self._sort_candidates_in_race()

    def __repr__(self) -> str:
        candidate_name_and_votes_str = ", ".join(
            [
                "%s: %.2f" % (candidate_vc.name, candidate_vc.number_of_votes)
                for candidate_vc in self.get_candidates_in_race()
            ]
        )
        return "<ElectionManager(%s)>" % (candidate_name_and_votes_str)

    # METHODS WITH SIDE-EFFECTS

    def elect_candidate(self, candidate: Candidate):
        if candidate not in self._candidate_vote_counts:
            raise RuntimeError("Candidate not found in electionManager")

        candidate_cv = self._candidate_vote_counts[candidate]

        candidate_cv.status = CandidateStatus.Elected
        self._elected_candidates.append(candidate_cv)
        self._candidates_in_race.remove(candidate_cv)

    def reject_candidate(self, candidate: Candidate):
        if candidate not in self._candidate_vote_counts:
            raise RuntimeError("Candidate not found in electionManager")

        candidate_cv = self._candidate_vote_counts[candidate]

        candidate_cv.status = CandidateStatus.Rejected
        self._rejected_candidates.append(candidate_cv)
        self._candidates_in_race.remove(candidate_cv)

    def transfer_votes(self, candidate: Candidate, number_of_trans_votes: float):
        if candidate not in self._candidate_vote_counts:
            raise RuntimeError("Candidate not found in electionManager")
        if round(number_of_trans_votes, 4) == 0.000:
            # Do nothing
            return

        candidate_cv = self._candidate_vote_counts[candidate]
        if candidate_cv.status == CandidateStatus.Active:
            raise RuntimeError(
                "ElectionManager can not transfer votes from a candidate "
                "that is still in the race (candidateStatus == Active)"
            )

        voters = len(candidate_cv.votes)  # Voters/ballots, not votes!
        votes_pr_voter = number_of_trans_votes / float(voters)  # This is a fractional number between 0 and 1

        for ballot in candidate_cv.votes:
            new_candidate_choice = self._get_ballot_candidate_nr_x_in_race_or_none(
                ballot, self._number_of_votes_pr_voter - 1
            )
            # Is none if blank or exhausted ballot

            if new_candidate_choice is None and self._pick_random_if_blank:
                # Chose a candidate at random
                candidates_in_race = self.get_candidates_in_race()
                if len(candidates_in_race) > 0:
                    new_candidate_choice = random.choice(candidates_in_race)

            if new_candidate_choice:
                new_candidate_cv = self._candidate_vote_counts[new_candidate_choice]
                new_candidate_cv.number_of_votes += votes_pr_voter
                new_candidate_cv.votes.append(ballot)

            # Still "Blank ballot"
            else:
                self._exhausted_ballots.append(ballot)
                self._number_of_blank_votes += votes_pr_voter

        candidate_cv.number_of_votes -= number_of_trans_votes
        candidate_cv.votes = []

        self._sort_candidates_in_race()

    # METHODS WITHOUT SIDE-EFFECTS

    def get_number_of_non_exhausted_votes(self):
        """Returns number of votes excluding blank and exhausted ballots"""
        return len(self._ballots) * self._number_of_votes_pr_voter - self._number_of_blank_votes

    def get_number_of_non_exhausted_ballots(self):
        """Returns number of ballots excluding blank and exhausted ballots"""
        return len(self._ballots) - len(self._exhausted_ballots)

    def get_number_of_candidates_in_race(self) -> int:
        return len(self._candidates_in_race)

    def get_number_of_elected_candidates(self) -> int:
        number_of_elected_candidates = len(self._elected_candidates)
        return number_of_elected_candidates

    def get_number_of_votes(self, candidate: Candidate) -> float:
        if candidate not in self._candidate_vote_counts:
            raise RuntimeError("Candidate not found in electionManager")

        return self._candidate_vote_counts[candidate].number_of_votes

    def get_candidates_in_race(self) -> List[Candidate]:
        candidates = [candidate_vc.candidate for candidate_vc in self._candidates_in_race if candidate_vc.is_in_race]
        return candidates

    def get_candidate_with_least_votes_in_race(self) -> Candidate:
        if len(self._candidates_in_race) == 0:
            raise NoCandidatesLeftInRaceError("No candidates left in race")

        candidate_with_least_votes = self._candidates_in_race[-1].candidate
        return candidate_with_least_votes

    def get_candidates_with_more_than_x_votes(self, x: int) -> List[Candidate]:
        candidates = [
            candidate_vc.candidate
            for candidate_vc in self._candidates_in_race
            if round(candidate_vc.number_of_votes, 4) > round(x, 4)
        ]
        return candidates

    def get_results(self) -> RoundResult:
        candidates_vc: List[CandidateVoteCount] = []
        candidates_vc.extend(self._elected_candidates)
        candidates_vc.extend(self._candidates_in_race)
        candidates_vc.extend(self._rejected_candidates[::-1])

        candidate_results = [candidate_vc.as_candidate_result() for candidate_vc in candidates_vc]

        round_result = RoundResult(candidate_results, self._number_of_blank_votes)
        return round_result

    # INTERNAL METHODS
    def _get_ballot_candidate_nr_x_in_race_or_none(self, ballot: Ballot, x: int) -> Candidate:
        ranked_candidates_in_race = [
            candidate for candidate in ballot.ranked_candidates if self._candidate_vote_counts[candidate].is_in_race
        ]

        if len(ranked_candidates_in_race) > x:
            candidate = ranked_candidates_in_race[x]
            return candidate
        else:
            return None

    def _sort_candidates_in_race(self):
        sorted_candidates_in_race = sorted(
            self._candidates_in_race, key=functools.cmp_to_key(self._cmp_candidate_vote_counts)
        )
        self._candidates_in_race = sorted_candidates_in_race

    def _cmp_candidate_vote_counts(self, candidate1_vc: CandidateVoteCount, candidate2_vc: CandidateVoteCount) -> int:
        c1_votes: float = candidate1_vc.number_of_votes
        c2_votes: float = candidate2_vc.number_of_votes

        if not almost_equal(c1_votes, c2_votes):
            if c1_votes > c2_votes:
                return -1
            else:
                return 1

        # If equal number of votes
        else:
            if self._compare_method_if_equal == CompareMethodIfEqual.MostSecondChoiceVotes:
                # Choose candidate with most second choices (or third, forth and so on) (default)
                if self._candidate1_has_most_second_choices(candidate1_vc, candidate2_vc, x=1):
                    return -1
                else:
                    return 1

            if self._compare_method_if_equal == CompareMethodIfEqual.Random:
                # Choose randomly
                return random.choice([1, -1])

            else:
                raise SystemError("Compare method unknown/not implemented.")

    def _candidate1_has_most_second_choices(
        self, candidate1_vc: CandidateVoteCount, candidate2_vc: CandidateVoteCount, x: int
    ) -> bool:
        if x >= self._number_of_candidates:
            return random.choice([True, False])

        votes_candidate1: int = 0
        votes_candidate2: int = 0

        for ballot in self._ballots:
            candidate = self._get_ballot_candidate_nr_x_in_race_or_none(ballot, x)

            if candidate == candidate1_vc.candidate:
                votes_candidate1 += 1
            elif candidate == candidate2_vc.candidate:
                votes_candidate2 += 1
            elif candidate is None:
                pass  # Zero votes

        if votes_candidate1 == votes_candidate2:
            return self._candidate1_has_most_second_choices(candidate1_vc, candidate2_vc, x + 1)
        else:
            return votes_candidate1 > votes_candidate2


class ElectionResults:
    """
    ElectionResults store the result of all rounds in the election:

     - the ranking of candidates
     - how many votes they got
     - their election status (elected, active, rejected)

    ElectionResults.get_winners() makes it trivial to receive the elected candidates.

    ElectedResults can be printed:

    > elected_results = votesim.single_transferable_vote(candidates, ballots)
    > print(elected_results)
    """

    def __init__(self):
        self.rounds: List[RoundResult] = []

    def register_round_results(self, round_: RoundResult):
        self.rounds.append(round_)

    def get_winners(self) -> List[Candidate]:
        last_round = self.rounds[-1]
        winner_candidates = [
            candidate_result.candidate
            for candidate_result in last_round.candidate_results
            if candidate_result.status == CandidateStatus.Elected
        ]
        return winner_candidates

    def __repr__(self) -> str:
        return "<ElectionResults(%i rounds)>" % len(self.rounds)

    def __str__(self) -> str:
        lines = []
        for i, round_ in enumerate(self.rounds):

            # Print round nr header
            if i == len(self.rounds) - 1:
                lines.append("FINAL RESULT")
            else:
                round_nr = i + 1
                lines.append("ROUND %i" % round_nr)

            # Print table
            lines.append(round_.__str__())

            # Print an extra blank line
            lines.append("")

        string = "\n".join(lines)
        return string
