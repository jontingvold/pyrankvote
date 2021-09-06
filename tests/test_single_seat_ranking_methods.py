import unittest
import votesim
from votesim import Candidate, Ballot


class TestInstantRunoffVoting(unittest.TestCase):
    def test_simple_case(self):
        per = Candidate("Per")
        paal = Candidate("Pål")
        askeladden = Candidate("Askeladden")

        candidates = [per, paal, askeladden]

        ballots = [
            Ballot(ranked_candidates=[askeladden, per]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[paal, per]),
            Ballot(ranked_candidates=[paal, per, askeladden])
        ]

        election_result = votesim.instant_runoff_voting(
            candidates, ballots
        )
        winners = election_result.get_winners()

        
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

        election_result = votesim.instant_runoff_voting(
            candidates, ballots
        )
        winners = election_result.get_winners()

        self.assertEqual(1, len(winners), "Function should return a list with one item")

        winner = winners[0]
        self.assertEqual(stay, winner, "Winner should be Soft")

    def test_simple_case2(self):

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

        election_result = votesim.instant_runoff_voting(
            candidates, ballots
        )
        winners = election_result.get_winners()

        self.assertEqual(1, len(winners), "Function should return a list with one item")
        self.assertListEqual([per], winners, "Winners should be Per")

    def test_case3(self):
        trump = Candidate("Donald Trump")
        hillary = Candidate("Hillary Clinton")
        mary = Candidate("Uniting Mary")

        candidates = [trump, hillary, mary]

        ballots = [
            Ballot(ranked_candidates=[trump, mary, hillary]),
            Ballot(ranked_candidates=[trump, mary, hillary]),
            Ballot(ranked_candidates=[hillary, mary, trump]),
            Ballot(ranked_candidates=[hillary, mary, trump]),
            Ballot(ranked_candidates=[hillary, mary])
        ]

        # You can use your own Candidate and Ballot objects as long as they implement the same properties and methods
        election_result = votesim.instant_runoff_voting(candidates, ballots)

        winners = election_result.get_winners()

        self.assertEqual(1, len(winners), "Function should return a list with one item")
        self.assertListEqual([hillary], winners, "Winners should be Per")

    def test_equal_number_of_votes(self):
        trump = Candidate("Donald Trump")
        hillary = Candidate("Hillary Clinton")
        mary = Candidate("Uniting Mary")

        candidates = [trump, hillary, mary]

        ballots = [
            Ballot(ranked_candidates=[trump, mary, hillary]),
            Ballot(ranked_candidates=[trump, mary, hillary]),
            Ballot(ranked_candidates=[mary, trump, hillary]),
            Ballot(ranked_candidates=[hillary, trump, mary]),
            Ballot(ranked_candidates=[hillary, mary, trump])
        ]

        # You can use your own Candidate and Ballot objects as long as they implement the same properties and methods
        election_result = votesim.instant_runoff_voting(candidates, ballots)
        ranking_first_round = election_result.rounds[0].candidate_results
        blank_votes = election_result.rounds[0].number_of_blank_votes

        self.assertEqual(3, len(ranking_first_round), "Function should return a list with one item")
        self.assertListEqual([trump, hillary, mary], [candidate_result.candidate for candidate_result in ranking_first_round], "Winners should be Per")
        self.assertEqual(0.0, blank_votes, "Should be zero blank votes as all ballots have ranked all candidates")
