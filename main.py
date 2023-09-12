# TODO pick questions that were answered incorrectly more often
from utils import *
import argparse

# CLI that shows the user options to resume a previous session or start a new one using argparse
parser = argparse.ArgumentParser(
    description="Resume a previous session or start a new one."
)
# Argument for the path to the dataset, defaults to 'data.csv'
parser.add_argument(
    "--data", type=str, default="./data/dutcheng.csv", help="Path to the dataset."
)
args = parser.parse_args()


def main(args):
    # Setup session
    session = setup_session(args)
    # Print questions
    print_questions(session)
    # Save session
    session.save_session()
    # Print session stats
    session.print_session_stats()


main(args)
