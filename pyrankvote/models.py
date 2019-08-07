import random
import functools


class CandidateStatus:
    Elected = "Elected"
    Hopeful = "Hopeful"
    Rejected = "Rejected"


class Candidate:
    def __init__(self, name):
        self.name = name
        self.status = CandidateStatus.Hopeful
        self.number_of_votes = 0
        self.votes = []  # type: Ballots

    @property
    def is_in_race(self):
        return self.status == CandidateStatus.Hopeful

    def reset_race(self):
        self.status = CandidateStatus.Hopeful
        self.number_of_votes = 0
        self.votes = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Candidate(name='%s')" % self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == self.name


class DuplicateCandidatesError(ValueError):
    pass


class Ballot:
    def __init__(self, ranked_candidates):
        ranked_candidates = tuple(ranked_candidates)

        if Ballot._is_duplicates(ranked_candidates):
            raise DuplicateCandidatesError

        if not Ballot._is_all_candidate_objects(ranked_candidates):
            raise TypeError("Not all objects in ranked candidate list are of class Candidate")

        self.ranked_candidates = ranked_candidates

    #def is_blank_vote(self):
    #    return len(self.get_ranked_candidates_in_race) == 0

    def get_ranked_candidates(self):
        return self.ranked_candidates

    def get_ranked_candidates_in_race(self):
        return tuple(candidate for candidate in self.ranked_candidates if candidate.is_in_race)

    def get_first_x_candidates_in_race(self, x):
        ranked_candidates_in_race = self.get_ranked_candidates_in_race()

        if len(ranked_candidates_in_race) > x:
            return ranked_candidates_in_race[:x]
        else:
            return ranked_candidates_in_race

    def get_candidate_nr_x_in_race_or_none(self, x):
        ranked_candidates_in_race = self.get_ranked_candidates_in_race()

        if len(ranked_candidates_in_race) > x:
            return ranked_candidates_in_race[x]
        else:
            return None

    @staticmethod
    def _is_duplicates(ranked_candidates):
        return len(set(ranked_candidates)) is not len(ranked_candidates)

    @staticmethod
    def _is_all_candidate_objects(ranked_candidates):
        for obj in ranked_candidates:
            if obj.__class__ is not Candidate:
                return False

        # If all objects are Candidate-objects
        return True


class Election:
    def __init__(self, number_of_seats=1):
        self.number_of_seats = number_of_seats
        self.candidates = []
        self.ballots = []

    def add_candidate(self, name):
        self.candidates.append(Candidate(name))

    def register_ballot(self, ranked_candidates):
        self.ballots.append(Ballot(ranked_candidates))

    def get_candidates(self):
        return self.candidates

    def get_candidates_in_race(self):
        return tuple([candidate for candidate in self.candidates if candidate.is_in_race])

    def reset_race(self):
        for candidate in self.candidates:
            candidate.reset_race()


class CompareMethodIfEqual:
    Random = "Random"
    MostSecondChoiceVotes = "MostSecondChoiceVotes"


class ElectionManager:
    def __init__(self, election, number_of_votes_pr_voter=1, compare_method_if_equal=CompareMethodIfEqual.MostSecondChoiceVotes):
        self.election = election
        self.number_of_votes_pr_voter = number_of_votes_pr_voter
        self.compare_method_if_equal = compare_method_if_equal

        self.elected_candidates = []    # Sorted asc by election round
        self.ranked_candidates_in_race = None
        self.rejected_candidates = []   # Sorted desc by election round
        self.results_by_round = []

        for ballot in self.election.ballots:
            candidates = ballot.get_first_x_candidates_in_race(x=number_of_votes_pr_voter)
            for candidate in candidates:
                candidate.number_of_votes += 1
                candidate.votes.append(ballot)

    def update_candidate_ranking(self):
        candidates = self.election.get_candidates_in_race()
        self.ranked_candidates_in_race = sorted(candidates, key=functools.cmp_to_key(self._candidate1_has_more_votes))

        self._store_result()

    def get_candidate_with_most_votes_in_race(self):
        return self.ranked_candidates_in_race[0]

    def get_candidate_with_least_votes_in_race(self):
        return self.ranked_candidates_in_race[-1]

    def get_candidates_with_more_than_x_votes(self, x):
        return [candidate for candidate in self.ranked_candidates_in_race
                if round(candidate.number_of_votes, 4) > round(x, 4)]

    def transfer_votes(self, candidate, number_of_trans_votes):
        if round(number_of_trans_votes, 4) == 0:
            return

        voters = len(candidate.votes)  # Voters/ballots, not votes!
        votes_pr_voter = number_of_trans_votes/float(voters)  # This is a fractional number between 0 and 1

        for ballot in candidate.votes:
            new_candidate_choice = ballot.get_candidate_nr_x_in_race_or_none(self.number_of_votes_pr_voter - 1)

            if new_candidate_choice is None:
                # Chose a candidate at random
                candidates_in_race = self.election.get_candidates_in_race()
                if len(candidates_in_race) == 0:
                    # If no candidates left in race, do nothing
                    return
                else:
                    new_candidate_choice = random.choice(candidates_in_race)

            new_candidate_choice.number_of_votes += votes_pr_voter
            new_candidate_choice.votes.append(ballot)

        candidate.number_of_votes -= number_of_trans_votes
        candidate.votes = []

    def elect_candidate(self, candidate):
        self.elected_candidates.append(candidate)
        candidate.status = CandidateStatus.Elected

    def reject_candidate(self, candidate):
        self.rejected_candidates.append(candidate)
        candidate.status = CandidateStatus.Rejected

    @staticmethod
    def result_as_string(result):
        s = ""
        for c in result:
            s += "%s, %.02f votes (%s)" % (c["candidate"].name, c["votes"], c["status"])
        return s

    # Private methods
    def _store_result(self):
        self.results_by_round.append(self._get_result())

    def _get_result(self):
        ranked_candidates = self._get_ranked_candidates()
        result = [{"candidate": candidate, "votes": candidate.number_of_votes, "status": candidate.status}
                   for candidate in ranked_candidates]
        return result

    def _get_ranked_candidates(self):
        ranked_candidates = []
        ranked_candidates.extend(self.elected_candidates)
        ranked_candidates.extend(self.ranked_candidates_in_race)
        ranked_candidates.extend(reversed(self.rejected_candidates))
        return ranked_candidates

    def _candidate1_has_more_votes(self, candidate1, candidate2):
        c1_votes = round(candidate1.number_of_votes, 4)
        c2_votes = round(candidate2.number_of_votes, 4)

        if c1_votes != c2_votes:
            return c1_votes > c2_votes
        else:
            # If equal number of votes:
            return self._compare_if_equal_number_of_votes(candidate1, candidate2)

    def _compare_if_equal_number_of_votes(self, candidate1, candidate2):
        if self.compare_method_if_equal == CompareMethodIfEqual.Random:
            return self._compare_random()
        elif self.compare_method_if_equal == CompareMethodIfEqual.MostSecondChoiceVotes:
            return self._candidate1_has_most_second_choices(candidate1, candidate2, x=1)
        else:
            raise SystemError("Compare method unknown/not implemented.")

    def _compare_random(self):
        return random.choice([True, False])

    def _candidate1_has_most_second_choices(self, candidate1, candidate2, x):
        if x >= len(self.election.get_candidates()):
            return self._compare_random()

        votes_candidate1 = 0
        votes_candidate2 = 0

        for ballot in self.election.ballots:
            candidate = ballot.get_candidate_nr_x_in_race_or_none(x)

            if candidate == candidate1:
                votes_candidate1 += 1
            if candidate == candidate2:
                votes_candidate2 += 1
            if candidate is None:
                pass  # Zero votes

        if votes_candidate1 != votes_candidate2:
            return votes_candidate1 > votes_candidate2
        else:
            # If still same number of votes, look at 3rd choice votes (or 4th choice votes etc.)
            return self._candidate1_has_most_second_choices(candidate1, candidate2, x+1)

    def __str__(self):
        return ElectionManager.result_as_string(self.get_result())
