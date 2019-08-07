import unittest
import pyrankvote


class TestInstantRunoffVoting(unittest.TestCase):
    def test_simple_case(self):

        election = pyrankvote.Election(number_of_seats=1)
        election.add_candidate("Stay")
        election.add_candidate("Soft Brexit")
        election.add_candidate("Hard Brexit")

        stay, soft, hard = election.get_candidates()
        election.register_ballot(ranked_candidates=[soft, stay])
        election.register_ballot(ranked_candidates=[stay, soft])
        election.register_ballot(ranked_candidates=[stay, soft])
        election.register_ballot(ranked_candidates=[hard, soft])
        election.register_ballot(ranked_candidates=[hard, stay, soft])

        winners = pyrankvote.voting_methods.instant_runoff_voting(election)
        self.assertEqual(1, len(winners), "Function should return a list with one item")

        winner = winners[0]
        self.assertEqual(stay, winner, "Winner should be Soft")

    def test_simple_case2(self):

        election = pyrankvote.Election(number_of_seats=1)
        election.add_candidate("Per")
        election.add_candidate("Pål")
        election.add_candidate("Askeladden")

        per, paal, askeladden = election.get_candidates()
        election.register_ballot(ranked_candidates=[askeladden, per])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[paal, per])
        election.register_ballot(ranked_candidates=[paal, per, askeladden])

        winners = pyrankvote.voting_methods.instant_runoff_voting(election)
        self.assertEqual(1, len(winners), "Function should return a list with one item")
        self.assertListEqual([per], winners, "Winners should be Per")


class TestPreferentialBlockVoting(unittest.TestCase):
    def test_simple_irv(self):

        election = pyrankvote.Election(number_of_seats=1)
        election.add_candidate("Stay")
        election.add_candidate("Soft Brexit")
        election.add_candidate("Hard Brexit")

        stay, soft, hard = election.get_candidates()
        election.register_ballot(ranked_candidates=[soft, stay])
        election.register_ballot(ranked_candidates=[stay, soft])
        election.register_ballot(ranked_candidates=[stay, soft])
        election.register_ballot(ranked_candidates=[hard, soft])
        election.register_ballot(ranked_candidates=[hard, stay, soft])

        winners = pyrankvote.voting_methods.preferential_block_voting(election)
        self.assertEqual(1, len(winners), "Function should return a list with one item")

        winner = winners[0]
        self.assertEqual(stay, winner, "Winner should be Soft")

    def test_simple_irv2(self):

        election = pyrankvote.Election(number_of_seats=1)
        election.add_candidate("Per")
        election.add_candidate("Pål")
        election.add_candidate("Askeladden")

        per, paal, askeladden = election.get_candidates()
        election.register_ballot(ranked_candidates=[askeladden, per])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[paal, per])
        election.register_ballot(ranked_candidates=[paal, per, askeladden])

        winners = pyrankvote.voting_methods.preferential_block_voting(election)
        self.assertEqual(1, len(winners), "Function should return a list with one item")
        self.assertListEqual([per], winners, "Winners should be Per")

    def test_simple_pbv(self):

        election = pyrankvote.Election(number_of_seats=2)
        election.add_candidate("Per")
        election.add_candidate("Pål")
        election.add_candidate("Askeladden")

        per, paal, askeladden = election.get_candidates()
        election.register_ballot(ranked_candidates=[askeladden, per])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[paal, per])
        election.register_ballot(ranked_candidates=[paal, per, askeladden])

        winners = pyrankvote.voting_methods.preferential_block_voting(election)
        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertListEqual([per, paal], winners, "Winners should be Per and Pål")

    def test_irv_with_second_selection_if_equal(self):

        election = pyrankvote.Election(number_of_seats=1)
        election.add_candidate("Stay")
        election.add_candidate("Soft Brexit")
        election.add_candidate("Hard Brexit")

        stay, soft, hard = election.get_candidates()
        election.register_ballot(ranked_candidates=[stay, soft, hard])
        election.register_ballot(ranked_candidates=[hard, soft, stay])
        election.register_ballot(ranked_candidates=[soft, stay, hard])

        winners = pyrankvote.voting_methods.preferential_block_voting(election)
        self.assertEqual(1, len(winners), "Function should return a list with one item")

        winner = winners[0]
        self.assertEqual(soft, winner, "Winner should be soft")

    def test_simple_pbv_with_second_selection_if_equal(self):

        election = pyrankvote.Election(number_of_seats=2)
        election.add_candidate("Stay")
        election.add_candidate("Soft Brexit")
        election.add_candidate("Hard Brexit")

        stay, soft, hard = election.get_candidates()
        election.register_ballot(ranked_candidates=[stay, soft, hard])
        election.register_ballot(ranked_candidates=[hard, soft, stay])
        election.register_ballot(ranked_candidates=[soft, stay, hard])

        winners = pyrankvote.voting_methods.preferential_block_voting(election)
        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertListEqual([soft, stay], winners, "Winners should be Soft and Stay")


class TestSingleTransferableVote(unittest.TestCase):
    def test_simple_irv(self):

        election = pyrankvote.Election(number_of_seats=1)
        election.add_candidate("Stay")
        election.add_candidate("Soft Brexit")
        election.add_candidate("Hard Brexit")

        stay, soft, hard = election.get_candidates()
        election.register_ballot(ranked_candidates=[soft, stay])
        election.register_ballot(ranked_candidates=[stay, soft])
        election.register_ballot(ranked_candidates=[stay, soft])
        election.register_ballot(ranked_candidates=[hard, soft])
        election.register_ballot(ranked_candidates=[hard, stay, soft])

        winners = pyrankvote.voting_methods.single_transferable_vote(election)
        self.assertEqual(1, len(winners), "Function should return a list with one item")

        winner = winners[0]
        self.assertEqual(stay, winner, "Winner should be Soft")

    def test_simple_irv2(self):

        election = pyrankvote.Election(number_of_seats=1)
        election.add_candidate("Per")
        election.add_candidate("Pål")
        election.add_candidate("Askeladden")

        per, paal, askeladden = election.get_candidates()
        election.register_ballot(ranked_candidates=[askeladden, per])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[paal, per])
        election.register_ballot(ranked_candidates=[paal, per, askeladden])

        winners = pyrankvote.voting_methods.single_transferable_vote(election)
        self.assertEqual(1, len(winners), "Function should return a list with one item")
        self.assertListEqual([per], winners, "Winners should be Per")

    def test_case1_simple(self):

        election = pyrankvote.Election(number_of_seats=2)
        election.add_candidate("Per")
        election.add_candidate("Pål")
        election.add_candidate("Askeladden")

        per, paal, askeladden = election.get_candidates()
        election.register_ballot(ranked_candidates=[askeladden, per])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[paal, per])
        election.register_ballot(ranked_candidates=[paal, per, askeladden])

        winners = pyrankvote.voting_methods.single_transferable_vote(election)
        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertListEqual([per, paal], winners, "Winners should be Per and Pål")

    def test_case2(self):

        election = pyrankvote.models.Election(number_of_seats=2)
        election.add_candidate("Per")
        election.add_candidate("Pål")
        election.add_candidate("Maria")
        election.add_candidate("Ingrid")
        per, paal, maria, ingrid = election.get_candidates()

        # Quote = 4.33 with 10 votes and 2 seat

        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[maria, ingrid])
        election.register_ballot(ranked_candidates=[ingrid, maria])
        election.register_ballot(ranked_candidates=[ingrid, maria])

        # 1. round: Per: 7, Ingrid: 2, Maria: 1, Pål: 0
        #       --> Per is elected and 2.67 votes are transfered to Pål
        # 2. round: Pål: 2.67, Ingrid: 2, Maria: 1
        #       --> Maria is excluded and her one vote is transfered to Ingrid
        # 3. round: Ingrid: 3, Pål: 2.67
        #       --> Ingrid is elected

        winners = pyrankvote.voting_methods.single_transferable_vote(election)
        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertListEqual([per, ingrid], winners, "Winners should be Per and Ingrid")

    def test_case3(self):

        election = pyrankvote.models.Election(number_of_seats=2)
        election.add_candidate("Per")
        election.add_candidate("Pål")
        election.add_candidate("Maria")
        election.add_candidate("Ingrid")
        per, paal, maria, ingrid = election.get_candidates()

        # Quote = 4.67 with 11 votes and 2 seat

        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[per, paal])
        election.register_ballot(ranked_candidates=[maria, ingrid])
        election.register_ballot(ranked_candidates=[ingrid, maria])
        election.register_ballot(ranked_candidates=[ingrid, maria])

        # 1. round: Per: 7, Ingrid: 2, Maria: 1, Pål: 0
        #       --> Per is elected and 3.33 votes are transfered to Pål
        # 2. round: Pål: 3.33, Ingrid: 2, Maria: 1
        #       --> Maria is excluded and her one vote is transfered to Ingrid
        # 3. round: Pål: 3.33, Ingrid: 3
        #       --> Pål is elected

        winners = pyrankvote.voting_methods.single_transferable_vote(election)
        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertListEqual([per, paal], winners, "Winners should be Per and Pål")
