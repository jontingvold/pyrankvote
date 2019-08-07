import unittest
from pyrankvote import models


class TestCandidate(unittest.TestCase):
    def test_equal(self):
        """Test that two candidates with the same name is considered equal."""

        candidate1 = models.Candidate("Per")
        candidate2 = models.Candidate("Per")
        candidate3 = models.Candidate("Aase")

        self.assertEqual(candidate1, candidate2, "These candidates should be equal/the same candidate.")
        self.assertEqual(candidate1, candidate3, "These candidates should NOT be equal/the same candidate.")


class TestBallot(unittest.TestCase):
    def test_create_object(self):
        """Test that voting with two equal candidates raises DuplicateCandidateError"""

        candidate1 = models.Candidate("Per")
        candidate2 = models.Candidate("Maria")
        candidate3 = models.Candidate("Aase")

        ranked_candidates=(candidate1, candidate2, candidate3)

        ballot = models.Ballot(ranked_candidates)
        self.assertTupleEqual(ranked_candidates, ballot.ranked_candidates)

    def test_raise_duplicate_candidate_error(self):
        """Test that voting with two equal candidates raises DuplicateCandidateError"""

        candidate1 = models.Candidate("Per")
        candidate2 = models.Candidate("Per")
        candidate3 = models.Candidate("Aase")

        def tester(_):
            models.Ballot(ranked_candidates=[candidate1, candidate2, candidate3])

        msg = "Candidate 1 and 2 is equal and should raise duplicate candidate error"
        self.assertRaises(models.DuplicateCandidatesError, tester, msg)

        # TEST THE OPPOSITE
        candidate1 = models.Candidate("Per")
        candidate2 = models.Candidate("Maria")
        candidate3 = models.Candidate("Aase")

        # This should NOT raise an error
        models.Ballot(ranked_candidates=[candidate1, candidate2, candidate3])

    def test_raise_error_if_not_all_obj_are_candidate_objects(self):
        """Test that if one of the candidate that are voted for are not a cadidate, that a TypeError is raised"""

        candidate1 = models.Candidate("Per")
        candidate2 = "Aase"

        def tester(_):
            models.Ballot(ranked_candidates=[candidate1, candidate2])

        msg = "Candidate 2 is a string, not a Candidate, and should raise a TypeError"
        self.assertRaises(TypeError, tester, msg)

        # TEST THE OPPOSITE
        candidate1 = models.Candidate("Per")
        candidate2 = models.Candidate("Aase")

        # This should NOT raise an error
        models.Ballot(ranked_candidates=[candidate1, candidate2])
