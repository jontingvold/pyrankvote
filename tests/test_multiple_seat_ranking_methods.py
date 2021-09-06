import unittest
from votesim.test_helpers import assert_list_almost_equal

import votesim
from votesim import Candidate, Ballot
from votesim.helpers import CandidateStatus


class TestPreferentialBlockVoting(unittest.TestCase):
    def test_simple_pbv(self):

        stay = Candidate("Stay")
        soft = Candidate("Soft Brexit")
        hard = Candidate("Hard Brexit")

        candidates = [stay, soft, hard]

        ballots = [
            Ballot(ranked_candidates=[soft, stay]),
            Ballot(ranked_candidates=[stay, soft]),
            Ballot(ranked_candidates=[stay, soft]),
            Ballot(ranked_candidates=[hard, soft]),
            Ballot(ranked_candidates=[hard, stay, soft]),
        ]

        election_result = votesim.preferential_block_voting(
            candidates, ballots, number_of_seats=1
        )
        winners = election_result.get_winners()

        self.assertEqual(1, len(winners), "Function should return a list with one item")

        winner = winners[0]
        self.assertEqual(stay, winner, "Winner should be Soft")

    def test_simple_pbv2(self):

        per = Candidate("Per")
        paal = Candidate("Pål")
        askeladden = Candidate("Askeladden")

        candidates = [per, paal, askeladden]

        ballots = [
            Ballot(ranked_candidates=[askeladden, per]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[paal, per]),
            Ballot(ranked_candidates=[paal, per, askeladden]),
        ]

        election_result = votesim.preferential_block_voting(
            candidates, ballots, number_of_seats=1
        )
        winners = election_result.get_winners()

        self.assertEqual(1, len(winners), "Function should return a list with one item")
        self.assertListEqual([per], winners, "Winners should be Per")

    def test_simple_pbv(self):

        per = Candidate("Per")
        paal = Candidate("Pål")
        askeladden = Candidate("Askeladden")

        candidates = [per, paal, askeladden]

        ballots = [
            Ballot(ranked_candidates=[askeladden, per]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[paal, per]),
            Ballot(ranked_candidates=[paal, per, askeladden]),
        ]

        election_result = votesim.preferential_block_voting(
            candidates, ballots, number_of_seats=2
        )
        winners = election_result.get_winners()

        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertIn(per, winners, "Per should be one of the winners")
        self.assertIn(paal, winners, "Pål should be one of the winners")

    def test_pbv_with_second_selection_if_equal(self):

        stay = Candidate("Stay")
        soft = Candidate("Soft Brexit")
        hard = Candidate("Hard Brexit")

        candidates = [stay, soft, hard]

        ballots = [
            Ballot(ranked_candidates=[stay, soft, hard]),
            Ballot(ranked_candidates=[hard, soft, stay]),
            Ballot(ranked_candidates=[soft, stay, hard]),
        ]

        election_result = votesim.preferential_block_voting(
            candidates, ballots, number_of_seats=1
        )

        winners = election_result.get_winners()
        self.assertEqual(1, len(winners), "Function should return a list with one item")

        winner = winners[0]
        self.assertEqual(soft, winner, "Winner should be soft")

    def test_simple_pbv_with_second_selection_if_equal(self):

        stay = Candidate("Stay")
        soft = Candidate("Soft Brexit")
        hard = Candidate("Hard Brexit")

        candidates = [stay, soft, hard]

        ballots = [
            Ballot(ranked_candidates=[stay, soft, hard]),
            Ballot(ranked_candidates=[hard, soft, stay]),
            Ballot(ranked_candidates=[soft, stay, hard]),
        ]

        election_result = votesim.preferential_block_voting(
            candidates, ballots, number_of_seats=2
        )
        winners = election_result.get_winners()

        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertIn(soft, winners, "Soft should be one of the winners")
        self.assertIn(stay, winners, "Stay should be one of the winners")

    def test_example(self):
        popular_moderate = Candidate("William, popular moderate")
        moderate2 = Candidate("John, moderate")
        moderate3 = Candidate("Charles, moderate")
        far_left = Candidate("Thomas, far-left")

        candidates = [popular_moderate, moderate2, moderate3, far_left]

        ballots = [
            Ballot(ranked_candidates=[popular_moderate, moderate2, moderate3, far_left]),
            Ballot(ranked_candidates=[popular_moderate, moderate2, moderate3, far_left]),
            Ballot(ranked_candidates=[popular_moderate, moderate3, moderate2, far_left]),
            Ballot(ranked_candidates=[popular_moderate, moderate3, moderate2, far_left]),
            Ballot(ranked_candidates=[moderate2, popular_moderate, moderate3, far_left]),
            Ballot(ranked_candidates=[moderate2, popular_moderate, moderate3, far_left]),

            Ballot(ranked_candidates=[far_left, popular_moderate, moderate2, moderate3]),
            Ballot(ranked_candidates=[far_left, popular_moderate, moderate2, moderate3]),
            Ballot(ranked_candidates=[far_left, moderate2, popular_moderate, moderate3]),
            Ballot(ranked_candidates=[far_left, moderate2, popular_moderate, moderate3]),
        ]

        election_result = votesim.preferential_block_voting(candidates, ballots, number_of_seats=2)

        round_nr = 0
        candidates_results_in_round = election_result.rounds[round_nr].candidate_results

        ranking_in_round = [candidate_result.candidate for candidate_result in candidates_results_in_round]
        correct_ranking_in_round = [popular_moderate, moderate2, far_left, moderate3]
        self.assertEqual(4, len(ranking_in_round), "All four candidates should be in the result list")
        self.assertListEqual(correct_ranking_in_round, ranking_in_round)

        votes_in_round = [candidate_result.number_of_votes for candidate_result in candidates_results_in_round]
        correct_votes_in_round = [8, 6, 4, 2]
        assert_list_almost_equal(self, correct_votes_in_round, votes_in_round)

        status_in_round = [candidate_result.status for candidate_result in candidates_results_in_round]
        correct_status_in_round = [CandidateStatus.Elected, CandidateStatus.Elected, CandidateStatus.Rejected, CandidateStatus.Rejected]
        self.assertListEqual(correct_status_in_round, status_in_round)

        winners = election_result.get_winners()
        self.assertEqual(2, len(winners), "Function should return a list with two items")

        self.assertIn(popular_moderate, winners, "William should be a winner")
        self.assertIn(moderate2, winners, "John should be a winner")


class TestSingleTransferableVote(unittest.TestCase):
    def test_simple_stv(self):

        stay = Candidate("Stay")
        soft = Candidate("Soft Brexit")
        hard = Candidate("Hard Brexit")

        candidates = [stay, soft, hard]

        ballots = [
            Ballot(ranked_candidates=[soft, stay]),
            Ballot(ranked_candidates=[stay, soft]),
            Ballot(ranked_candidates=[stay, soft]),
            Ballot(ranked_candidates=[hard, soft]),
            Ballot(ranked_candidates=[hard, stay, soft]),
        ]

        election_result = votesim.single_transferable_vote(
            candidates, ballots, number_of_seats=1
        )
        winners = election_result.get_winners()

        self.assertEqual(1, len(winners), "Function should return a list with one item")

        winner = winners[0]
        self.assertEqual(stay, winner, "Winner should be Soft")

    def test_simple_stv2(self):

        per = Candidate("Per")
        paal = Candidate("Pål")
        askeladden = Candidate("Askeladden")

        candidates = [per, paal, askeladden]

        ballots = [
            Ballot(ranked_candidates=[askeladden, per]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[paal, per]),
            Ballot(ranked_candidates=[paal, per, askeladden]),
        ]

        election_result = votesim.single_transferable_vote(
            candidates, ballots, number_of_seats=1
        )
        winners = election_result.get_winners()

        self.assertEqual(1, len(winners), "Function should return a list with one item")
        self.assertListEqual([per], winners, "Winners should be Per")

    def test_case1_simple(self):

        per = Candidate("Per")
        paal = Candidate("Pål")
        askeladden = Candidate("Askeladden")

        candidates = [per, paal, askeladden]

        ballots = [
            Ballot(ranked_candidates=[askeladden, per]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[paal, per]),
            Ballot(ranked_candidates=[paal, per, askeladden]),
        ]

        election_result = votesim.single_transferable_vote(
            candidates, ballots, number_of_seats=2
        )
        winners = election_result.get_winners()

        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertListEqual([per, paal], winners, "Winners should be Per and Pål")

    def test_case2(self):

        per = Candidate("Per")
        paal = Candidate("Pål")
        maria = Candidate("Maria")
        ingrid = Candidate("Ingrid")

        candidates = [per, paal, maria, ingrid]


        # Quote = 3.33 with 10 votes and 2 seat
        ballots = [
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[maria, ingrid]),
            Ballot(ranked_candidates=[ingrid, maria]),
            Ballot(ranked_candidates=[ingrid, maria]),
        ]

        # 1. round: Per: 7, Ingrid: 2, Maria: 1, Pål: 0
        #       --> Per is elected and 3.67 votes are transferred to Pål
        # Final round: Per: 3.33, Pål: 3.67, Ingrid: 2, Maria: 1
        #       --> Paal is elected. Since all seats filled, Ingrid and Maria are rejected.

        election_result = votesim.single_transferable_vote(
            candidates, ballots, number_of_seats=2
        )
        winners = election_result.get_winners()

        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertListEqual([per, paal], winners, "Winners should be Per and Pål")

        round = 0
        votes_round = [candidate_vc.number_of_votes for candidate_vc in election_result.rounds[round].candidate_results]
        assert_list_almost_equal(self, votes_round, [7, 2, 1, 0], 0.02)

        round = 1
        votes_round = [candidate_vc.number_of_votes for candidate_vc in election_result.rounds[round].candidate_results]
        assert_list_almost_equal(self, votes_round, [3.33, 3.67, 2, 1], 0.02)


    def test_case3(self):

        per = Candidate("Per")
        paal = Candidate("Pål")
        maria = Candidate("Maria")
        ingrid = Candidate("Ingrid")

        candidates = [per, paal, maria, ingrid]

        # Quote = 4.67 with 11 votes and 2 seat
        ballots = [
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[maria, ingrid]),
            Ballot(ranked_candidates=[ingrid, maria]),
            Ballot(ranked_candidates=[ingrid, maria]),
        ]

        # 1. round: Per: 7, Ingrid: 2, Maria: 1, Pål: 0
        #       --> Per is elected and 3.33 votes are transfered to Pål
        # 2. round: Pål: 3.33, Ingrid: 2, Maria: 1
        #       --> Maria is excluded and her one vote is transfered to Ingrid
        # 3. round: Pål: 3.33, Ingrid: 3
        #       --> Pål is elected

        election_result = votesim.single_transferable_vote(
            candidates, ballots, number_of_seats=2
        )
        winners = election_result.get_winners()

        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertListEqual([per, paal], winners, "Winners should be Per and Pål")

    def test_example(self):
        popular_moderate = Candidate("William, popular moderate")
        moderate2 = Candidate("John, moderate")
        moderate3 = Candidate("Charles, moderate")
        far_left = Candidate("Thomas, far-left")

        candidates = [popular_moderate, moderate2, moderate3, far_left]

        ballots = [
            Ballot(ranked_candidates=[popular_moderate, moderate2, moderate3, far_left]),
            Ballot(ranked_candidates=[popular_moderate, moderate2, moderate3, far_left]),
            Ballot(ranked_candidates=[popular_moderate, moderate3, moderate2, far_left]),
            Ballot(ranked_candidates=[popular_moderate, moderate3, moderate2, far_left]),
            Ballot(ranked_candidates=[moderate2, popular_moderate, moderate3, far_left]),
            Ballot(ranked_candidates=[moderate2, popular_moderate, moderate3, far_left]),

            Ballot(ranked_candidates=[far_left, popular_moderate, moderate2, moderate3]),
            Ballot(ranked_candidates=[far_left, popular_moderate, moderate2, moderate3]),
            Ballot(ranked_candidates=[far_left, moderate2, popular_moderate, moderate3]),
            Ballot(ranked_candidates=[far_left, moderate2, popular_moderate, moderate3]),
        ]

        election_result = votesim.single_transferable_vote(candidates, ballots, number_of_seats=2)

        round_nr = 0
        candidates_results_in_round = election_result.rounds[round_nr].candidate_results
        ranking_in_round = [candidate_result.candidate for candidate_result in candidates_results_in_round]
        votes_in_round = [candidate_result.number_of_votes for candidate_result in candidates_results_in_round]
        self.assertEqual(4, len(ranking_in_round), "All four candidates should be list.")
        self.assertListEqual([popular_moderate, far_left, moderate2, moderate3], ranking_in_round)
        assert_list_almost_equal(self, [4, 4, 2, 0], votes_in_round)

        self.assertEqual(1, len(election_result.rounds), "Should be only one round")

        winners = election_result.get_winners()
        self.assertEqual(2, len(winners), "Should be two winners")

        self.assertIn(popular_moderate, winners, "William should be a winner")
        self.assertIn(far_left, winners, "John should be a winner")
