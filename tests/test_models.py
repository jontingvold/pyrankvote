import unittest
import votesim


class TestCandidate(unittest.TestCase):
    def test_equal(self):
        """Test that two candidates with the same name is considered equal."""

        candidate1 = votesim.Candidate("Per")
        candidate2 = votesim.Candidate("Per")
        candidate3 = votesim.Candidate("Aase")

        self.assertEqual(candidate1, candidate2, "These candidates should be equal/the same candidate.")
        self.assertNotEqual(candidate1, candidate3, "These candidates should NOT be equal/the same candidate.")


class TestBallot(unittest.TestCase):
    def test_create_object(self):
        """Test that voting with two equal candidates raises DuplicateCandidateError"""

        candidate1 = votesim.Candidate("Per")
        candidate2 = votesim.Candidate("Maria")
        candidate3 = votesim.Candidate("Aase")

        ranked_candidates=(candidate1, candidate2, candidate3)

        ballot = votesim.Ballot(ranked_candidates)
        self.assertTupleEqual(ranked_candidates, ballot.ranked_candidates)

    def test_raise_duplicate_candidate_error(self):
        """Test that voting with two equal candidates raises DuplicateCandidateError"""

        candidate1 = votesim.Candidate("Per")
        candidate2 = votesim.Candidate("Per")
        candidate3 = votesim.Candidate("Aase")

        def tester(_):
            votesim.Ballot(ranked_candidates=[candidate1, candidate2, candidate3])

        msg = "Candidate 1 and 2 is equal and should raise duplicate candidate error"
        self.assertRaises(votesim.models.DuplicateCandidatesError, tester, msg)

        # TEST THE OPPOSITE
        candidate1 = votesim.Candidate("Per")
        candidate2 = votesim.Candidate("Maria")
        candidate3 = votesim.Candidate("Aase")

        # This should NOT raise an error
        votesim.Ballot(ranked_candidates=[candidate1, candidate2, candidate3])

    def test_new_candidate_objects(self):
        """Test that if one of the candidate that are voted for are not a cadidate, that a TypeError is raised"""

        class NewCandidate:
            def __init__(self, name):
                self.name = "New "+name
            def __hash__(self):
                return hash(self.name)

        candidate1 = NewCandidate("Per")
        candidate2 = NewCandidate("Aase")

        # This should NOT raise an error
        votesim.Ballot(ranked_candidates=[candidate1, candidate2])

    def test_raise_error_if_not_all_obj_are_candidate_objects(self):
        """Test that if one of the candidate that are voted for are not a cadidate, that a TypeError is raised"""

        candidate1 = votesim.Candidate("Per")
        candidate2 = "Aase"

        def tester(_):
            votesim.Ballot(ranked_candidates=[candidate1, candidate2])

        msg = "Candidate 2 is a string, not a Candidate, and should raise a TypeError"
        self.assertRaises(TypeError, tester, msg)

        # TEST THE OPPOSITE
        candidate1 = votesim.Candidate("Per")
        candidate2 = votesim.Candidate("Aase")

        # This should NOT raise an error
        votesim.Ballot(ranked_candidates=[candidate1, candidate2])
