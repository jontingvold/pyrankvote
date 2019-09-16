"""
Models that are used by multiple_seat_ranking_methods.py

You can create and use your own Candidate and Ballot models as long as they implement the same properties and methods.
"""


class Candidate:
    """A candidate in the election."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Candidate('%s')>" % self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if other is None:
            return False

        return self.name == other.name


class DuplicateCandidatesError(RuntimeError): pass


class Ballot:
    """
    A ballot (vote) where the voter has ranked all, or just some, of the candidates.

    If a voter lists one candidate multiple times, a DuplicateCandidatesError is thrown.
    """

    def __init__(self, ranked_candidates):
        ranked_candidates = tuple(ranked_candidates)

        if Ballot._is_duplicates(ranked_candidates):
            raise DuplicateCandidatesError

        if not Ballot._is_all_candidate_objects(ranked_candidates):
            raise TypeError("Not all objects in ranked candidate list are of class Candidate or implement the same properties and methods")

        self.ranked_candidates = ranked_candidates

    def __repr__(self):
        candidate_name = ", ".join([candidate.name for candidate in self.ranked_candidates])
        return "<Ballot(%s)>" % (candidate_name)

    @staticmethod
    def _is_duplicates(ranked_candidates):
        return len(set(ranked_candidates)) is not len(ranked_candidates)

    @staticmethod
    def _is_all_candidate_objects(objects):
        for obj in objects:
            if not Ballot._is_candidate_object(obj):
                return False

        # If all objects are Candidate-objects
        return True

    @staticmethod
    def _is_candidate_object(obj):
        if obj.__class__ is Candidate:
            return True

        is_candidate_like = all([
            hasattr(obj, 'name'),
            hasattr(obj, '__hash__'),
            hasattr(obj, '__eq__')
        ])

        return is_candidate_like
