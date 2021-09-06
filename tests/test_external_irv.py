import unittest
import os
import csv
import votesim
from votesim import Candidate, Ballot
from votesim.test_helpers import assert_list_almost_equal


TEST_FOLDER = "test_data/external_irv/"
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_PATH = os.path.join(THIS_DIR, os.pardir, TEST_FOLDER)


def parse_ballots_csv_file(file_name):
    file_path = os.path.join(TEST_DATA_PATH, file_name)
    with open(file_path) as f:
        csv_file_without_header = list(csv.reader(f))[1:]
        parsed_csv_file = [
            (ballot_id, rank, candidate_name) for ballot_id, rank, candidate_name in csv_file_without_header
        ]
        # sorted_csv_file = sorted(parsed_csv_file, key=itemgetter(0,1))
        sorted_csv_file = parsed_csv_file

        candidates = {}
        ballots = []
        last_ballot_id = 0
        ranked_candidates = []

        for ballot_id, _, candidate_name in sorted_csv_file:
            if ballot_id != last_ballot_id and last_ballot_id != 0:
                ballot = Ballot(ranked_candidates)
                ballots.append(ballot)
                ranked_candidates = []

            last_ballot_id = ballot_id
            if candidate_name == "$UNDERVOTE":
                continue
            if candidate_name == "$OVERVOTE":
                continue
            if candidate_name in candidates:
                candidate = candidates[candidate_name]

            else:
                candidate = Candidate(name=candidate_name)
                candidates[candidate_name] = candidate
            ranked_candidates.append(candidate)

        ballot = Ballot(ranked_candidates)
        ballots.append(ballot)

        return list(candidates.values()), ballots


class TestExternalIRV(unittest.TestCase):
    def test_us_vt_btv_2009_03_mayor(self):
        """
        Burlington 2009 Mayoral Election
        Source: https://ranked.vote/us/vt/btv/2009/03/mayor/
        Data source: https://s3.amazonaws.com/ranked.vote-reports/us/vt/btv/2009/03/mayor/us_vt_btv_2009_03_mayor.normalized.csv.gz
        """

        file_name = "us_vt_btv_2009_03_mayor.normalized.csv"
        candidates, ballots = parse_ballots_csv_file(file_name)

        election_result = votesim.instant_runoff_voting(candidates, ballots, pick_random_if_blank=False)
        last_round = election_result.rounds[-1]

        blank_votes = last_round.number_of_blank_votes
        correct_blank_votes = 607
        self.assertEqual(correct_blank_votes, blank_votes)

        number_of_votes = [candidate_result.number_of_votes for candidate_result in last_round.candidate_results]
        correct_number_of_votes = [4313, 4060, 0, 0, 0, 0]
        assert_list_almost_equal(self, correct_number_of_votes, number_of_votes)

    def test_us_me_2018_06_cd02_primary(self):
        """
        Test Maine 2018 Congress District 2 Democrat Primary Election
        Source: https://ranked.vote/us/me/2018/06/cd02-primary/
        Data source: https://s3.amazonaws.com/ranked.vote-reports/us/me/2018/06/cd02-primary/us_me_2018_06_cd02-primary.normalized.csv.gz
        """

        file_name = "us_me_2018_06_cd02-primary.normalized.csv"
        candidates, ballots = parse_ballots_csv_file(file_name)

        election_result = votesim.instant_runoff_voting(candidates, ballots, pick_random_if_blank=False)
        last_round = election_result.rounds[-1]

        blank_votes = last_round.number_of_blank_votes
        correct_blank_votes = 7381
        self.assertEqual(correct_blank_votes, blank_votes)

        number_of_votes = [candidate_result.number_of_votes for candidate_result in last_round.candidate_results]
        correct_number_of_votes = [23611, 19853, 0, 0]
        assert_list_almost_equal(self, correct_number_of_votes, number_of_votes)

    def test_us_me_2018_11_cd02(self):
        """
        Maine 2018 Congress District 2 General Election
        Source: https://ranked.vote/us/me/2018/11/cd02/
        Data source: https://s3.amazonaws.com/ranked.vote-reports/us/me/2018/11/cd02/us_me_2018_11_cd02.normalized.csv.gz
        """

        file_name = "us_me_2018_11_cd02.normalized.csv"
        candidates, ballots = parse_ballots_csv_file(file_name)

        election_result = votesim.instant_runoff_voting(candidates, ballots, pick_random_if_blank=False)
        last_round = election_result.rounds[-1]

        blank_votes = last_round.number_of_blank_votes
        correct_blank_votes = 14706
        self.assertEqual(correct_blank_votes, blank_votes)

        number_of_votes = [candidate_result.number_of_votes for candidate_result in last_round.candidate_results]
        correct_number_of_votes = [142440, 138931, 0, 0]
        assert_list_almost_equal(self, correct_number_of_votes, number_of_votes)
