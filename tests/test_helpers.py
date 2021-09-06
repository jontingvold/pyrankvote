import unittest
from votesim import Candidate, Ballot
from votesim import helpers
from votesim.test_helpers import assert_list_almost_equal


class TestCandidateVoteCount(unittest.TestCase):
    def test_simple(self):
        pass


class TestElectionResults(unittest.TestCase):
    def test_simple(self):
        pass


class TestElectionManager(unittest.TestCase):
    def get_candidates_and_ballots(self):
        stay = Candidate("Stay")
        soft = Candidate("Soft Brexit")
        hard = Candidate("Hard Brexit")

        candidates = [stay, soft, hard]

        ballots = [
            Ballot(ranked_candidates=[stay, soft, hard]),
            Ballot(ranked_candidates=[hard, soft, stay]),
            Ballot(ranked_candidates=[soft, stay, hard]),
        ]

        return candidates, ballots

    def get_election_manager(self, candidates, ballots):
        manager = helpers.ElectionManager(
            candidates,
            ballots,
            number_of_votes_pr_voter=1,
            compare_method_if_equal=helpers.CompareMethodIfEqual.MostSecondChoiceVotes,
        )
        return manager

    def test_simple(self):
        candidates, ballots = self.get_candidates_and_ballots()
        stay, soft, hard = candidates
        manager = self.get_election_manager(candidates, ballots)
        candidate_results = manager.get_results()

        ranking_after_initialization = [candidate_result.candidate for candidate_result in manager._candidates_in_race]
        correct_ranking = [soft, stay, hard]

        msg = "Not correct ranking of candidates. Election manager should rank candidates after initialization."
        self.assertListEqual(correct_ranking, ranking_after_initialization, msg)

        self.assertListEqual(manager._elected_candidates, [], "List of elected candidates should be empty after init")
        self.assertListEqual(manager._rejected_candidates, [], "List of elected candidates should be empty after init")

        candidate_votes = [candidate_result.number_of_votes for candidate_result in candidate_results.candidate_results]
        correct_candidate_votes = [1.0, 1.0, 1.0]
        assert_list_almost_equal(self, candidate_votes, correct_candidate_votes, 0.001, "Votes not counted correctly.")

        candidate_status = [candidate_result.status for candidate_result in candidate_results.candidate_results]
        active = helpers.CandidateStatus.Active
        correct_candidate_status = [active, active, active]
        self.assertListEqual(candidate_status, correct_candidate_status, "All candidates should have status Active")

    def test_random_ranking_of_equal_votes(self):
        candidates, ballots = self.get_candidates_and_ballots()
        stay, soft, hard = candidates

        ranked_first = {
            soft: 0,
            hard: 0,
            stay: 0,
        }

        for _ in range(2000):
            manager = helpers.ElectionManager(
                candidates,
                ballots,
                number_of_votes_pr_voter=1,
                compare_method_if_equal=helpers.CompareMethodIfEqual.Random,
            )

            candidate_ranked_first = manager._candidates_in_race[0].candidate
            ranked_first[candidate_ranked_first] += 1

        msg = "Should have almost equal votes %s" % ranked_first
        self.assertGreater(ranked_first[soft], 20, msg)
        self.assertGreater(ranked_first[hard], 20, msg)
        self.assertGreater(ranked_first[stay], 20, msg)

        self.assertLess(ranked_first[soft], 1980, msg)
        self.assertLess(ranked_first[hard], 1980, msg)
        self.assertLess(ranked_first[stay], 1980, msg)

    def test_candidates_have_most_second_votes(self):
        stay = Candidate("Stay")
        soft = Candidate("Soft Brexit")
        hard = Candidate("Hard Brexit")
        extra = Candidate("Extra")

        candidates = [stay, soft, hard, extra]

        ballots = [
            Ballot(ranked_candidates=[stay, soft, hard]),
            Ballot(ranked_candidates=[stay, soft, hard]),
            Ballot(ranked_candidates=[stay, soft]),
            Ballot(ranked_candidates=[extra, hard, stay]),
            Ballot(ranked_candidates=[soft, stay, hard]),
            Ballot(ranked_candidates=[soft, stay, hard]),
            Ballot(ranked_candidates=[soft, stay, hard]),
        ]
        manager = self.get_election_manager(candidates, ballots)

        stay_vc, soft_vc, hard_vc, extra_vc = [
            manager._candidate_vote_counts[stay],
            manager._candidate_vote_counts[soft],
            manager._candidate_vote_counts[hard],
            manager._candidate_vote_counts[extra],
        ]

        is_stay_ranked_first = manager._candidate1_has_most_second_choices(stay_vc, extra_vc, 1)
        self.assertEqual(is_stay_ranked_first, True, "Stay should rank before extra")

        is_hard_ranked_first = manager._candidate1_has_most_second_choices(hard_vc, extra_vc, 1)
        self.assertEqual(
            is_hard_ranked_first, True, "Hard, should rank before extra, because hard has more 2nd alternative votes"
        )

        is_stay_ranked_first = manager._candidate1_has_most_second_choices(stay_vc, soft_vc, 1)
        self.assertEqual(
            is_stay_ranked_first,
            True,
            "Stay should rank before soft, even though they have equal number of votes, and equal number of "
            "second votes, because stay has more 3rd alternative votes.",
        )

    def test_elect_candidate(self):
        candidates, _ = self.get_candidates_and_ballots()
        stay, soft, hard = candidates
        ballots = [
            Ballot(ranked_candidates=[stay, soft, hard]),
            Ballot(ranked_candidates=[hard, soft, stay]),
            Ballot(ranked_candidates=[soft, stay, hard]),
        ]
        manager = self.get_election_manager(candidates, ballots)

        stay_vc, soft_vc, hard_vc = [
            manager._candidate_vote_counts[stay],
            manager._candidate_vote_counts[soft],
            manager._candidate_vote_counts[hard],
        ]

        self.assertListEqual([], manager._elected_candidates)
        self.assertListEqual([], manager._rejected_candidates)
        self.assertEqual(stay_vc.status, helpers.CandidateStatus.Active)
        self.assertEqual(soft_vc.status, helpers.CandidateStatus.Active)
        self.assertEqual(hard_vc.status, helpers.CandidateStatus.Active)

        manager.elect_candidate(stay)

        self.assertListEqual([stay_vc], manager._elected_candidates)
        self.assertNotIn(stay_vc, manager._candidates_in_race)

        self.assertEqual(stay_vc.status, helpers.CandidateStatus.Elected)
        self.assertEqual(soft_vc.status, helpers.CandidateStatus.Active)
        self.assertEqual(hard_vc.status, helpers.CandidateStatus.Active)

        manager.elect_candidate(soft)

        self.assertListEqual(
            [stay_vc, soft_vc],
            manager._elected_candidates,
            "Stay should be before soft first since it is was elected first.",
        )
        self.assertListEqual([hard_vc], manager._candidates_in_race)
        self.assertNotIn(stay_vc, manager._candidates_in_race)

        self.assertEqual(stay_vc.status, helpers.CandidateStatus.Elected)
        self.assertEqual(soft_vc.status, helpers.CandidateStatus.Elected)
        self.assertEqual(hard_vc.status, helpers.CandidateStatus.Active)

    def test_reject_candidate(self):
        candidates, _ = self.get_candidates_and_ballots()
        stay, soft, hard = candidates
        ballots = [
            Ballot(ranked_candidates=[stay, soft, hard]),
            Ballot(ranked_candidates=[hard, soft, stay]),
            Ballot(ranked_candidates=[soft, stay, hard]),
        ]
        manager = self.get_election_manager(candidates, ballots)

        stay_vc, soft_vc, hard_vc = [
            manager._candidate_vote_counts[stay],
            manager._candidate_vote_counts[soft],
            manager._candidate_vote_counts[hard],
        ]

        self.assertListEqual([], manager._elected_candidates)
        self.assertListEqual([], manager._rejected_candidates)
        self.assertEqual(stay_vc.status, helpers.CandidateStatus.Active)
        self.assertEqual(soft_vc.status, helpers.CandidateStatus.Active)
        self.assertEqual(hard_vc.status, helpers.CandidateStatus.Active)

        manager.reject_candidate(stay)

        self.assertListEqual([stay_vc], manager._rejected_candidates)
        self.assertNotIn(stay_vc, manager._candidates_in_race)

        self.assertEqual(stay_vc.status, helpers.CandidateStatus.Rejected)
        self.assertEqual(soft_vc.status, helpers.CandidateStatus.Active)
        self.assertEqual(hard_vc.status, helpers.CandidateStatus.Active)

        manager.reject_candidate(soft)

        self.assertListEqual(
            [stay_vc, soft_vc],
            manager._rejected_candidates,
            "Stay should be before soft first since it is was rejected first.",
        )
        self.assertListEqual([hard_vc], manager._candidates_in_race)
        self.assertNotIn(stay_vc, manager._candidates_in_race)

        self.assertEqual(stay_vc.status, helpers.CandidateStatus.Rejected)
        self.assertEqual(soft_vc.status, helpers.CandidateStatus.Rejected)
        self.assertEqual(hard_vc.status, helpers.CandidateStatus.Active)

    def test_transfere_votes(self):
        candidates, _ = self.get_candidates_and_ballots()
        stay, soft, hard = candidates
        ballots = [
            Ballot(ranked_candidates=[stay, soft, hard]),
            Ballot(ranked_candidates=[stay, soft, hard]),
            Ballot(ranked_candidates=[stay, hard, soft]),
            Ballot(ranked_candidates=[soft, stay, hard]),
        ]
        manager = self.get_election_manager(candidates, ballots)

        stay_vc, soft_vc, hard_vc = [
            manager._candidate_vote_counts[stay],
            manager._candidate_vote_counts[soft],
            manager._candidate_vote_counts[hard],
        ]

        self.assertAlmostEqual(stay_vc.number_of_votes, 3.0)
        self.assertAlmostEqual(soft_vc.number_of_votes, 1.0)
        self.assertAlmostEqual(hard_vc.number_of_votes, 0.0)

        with self.assertRaises(RuntimeError):
            manager.transfer_votes(stay, 0.5)

        manager.elect_candidate(stay)
        manager.transfer_votes(stay, 0.5)
        self.assertAlmostEqual(stay_vc.number_of_votes, 3.0 - 0.5)
        self.assertAlmostEqual(soft_vc.number_of_votes, 1.0 + 2 * 0.5 / 3)
        self.assertAlmostEqual(hard_vc.number_of_votes, 0.0 + 1 * 0.5 / 3)
