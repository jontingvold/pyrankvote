import unittest
import pyrankvote
from pyrankvote.models import Candidate, Ballot


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

        election_result = pyrankvote.single_seat_ranking_methods.instant_runoff_voting(
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

        election_result = pyrankvote.single_seat_ranking_methods.instant_runoff_voting(
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

        election_result = pyrankvote.single_seat_ranking_methods.instant_runoff_voting(
            candidates, ballots
        )
        winners = election_result.get_winners()

        self.assertEqual(1, len(winners), "Function should return a list with one item")
        self.assertListEqual([per], winners, "Winners should be Per")
