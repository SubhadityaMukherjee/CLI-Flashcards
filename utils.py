import os
import pickle as pkl
import random
import time
from difflib import SequenceMatcher
import pandas as pd
import numpy as np
from tqdm import tqdm


# Class with session info, including the lists with num_corrects and num_incorrects for each question
class Session:
    """Class with session info, including the lists with num_corrects and num_incorrects for each question"""

    def __init__(self, args, data_file):
        self.data_file = data_file
        self.args = args
        self.resume = False

    def create_new_session(self):
        """Create a new session"""
        # rename cols to A and B
        self.data_file.columns = ["A", "B"]
        self.list_A = self.data_file["A"].tolist()
        self.list_B = self.data_file["B"].tolist()
        assert len(self.list_A) == len(
            self.list_B
        ), "The number of elements in col1 and col2 must be the same."

        # print number of questions
        self.total_num_questions = len(self.list_A)
        # print("Number of questions: {}".format(self.total_num_questions))

        self.max_questions = min(self.args.num_questions, self.total_num_questions)
        self.reverse = self.args.reverse if self.args.reverse else False
        self.num_corrects = [0] * len(self.list_A)
        self.num_incorrects = [0] * len(self.list_B)
        self.num_corrects_r = [0] * len(self.list_A)
        self.num_incorrects_r = [0] * len(self.list_B)

    def pack_save_file(self):
        """Pack session info into a dict to be saved as a pickle file"""
        return {
            "list_A": self.list_A,
            "list_B": self.list_B,
            "num_corrects": self.num_corrects,
            "num_incorrects": self.num_incorrects,
            "num_corrects_r": self.num_corrects_r,
            "num_incorrects_r": self.num_incorrects_r,
            "max_questions": self.max_questions,
        }

    def save_session(self):
        """Save session info as a pickle file"""
        pickle_file = self.pack_save_file()
        pkl.dump(pickle_file, open("./data/session.pkl", "wb"))

    def restore_session(self):
        """Restore session info from a pickle file"""

        pickle_file = pkl.load(open("./data/session.pkl", "rb"))
        self.list_A = pickle_file["list_A"]
        self.list_B = pickle_file["list_B"]
        self.num_corrects = pickle_file["num_corrects"]
        self.num_incorrects = pickle_file["num_incorrects"]
        self.num_corrects_r = pickle_file["num_corrects_r"]
        self.num_incorrects_r = pickle_file["num_incorrects_r"]
        self.max_questions = pickle_file["max_questions"]

    def print_session_stats(self):
        """Print session stats"""
        if self.reverse:
            print("Corrects: {}".format(sum(self.num_corrects_r)))
            print("Incorrects: {}".format(sum(self.num_incorrects_r)))
        else:
            print("Corrects: {}".format(sum(self.num_corrects)))
            print("Incorrects: {}".format(sum(self.num_incorrects)))
        print("Time taken: {}".format(self.time_taken))
        print("Incorrects:")
        for k,v in self.dict_wrongs.items():
            print(k,' -> ', v)


def string_similarity(str1, str2):
    """Return a similarity score between 0 and 1 for two strings"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def choice_while_answering(user_ans, correct_ans):
    """Return True if the user's answer is correct, False otherwise, while allowing the user to enter ? to see the correct answer, / to skip, and q to quit"""
    if user_ans == "?":
        input("Correct answer: {}".format(correct_ans))
        return False
    elif user_ans == "/":
        return False
    elif user_ans == "q":
        return False
    else:
        ifany = 0
        for option in correct_ans.split("/"):
            if string_similarity(user_ans, option.strip()) >= 0.8:
                ifany += 1
        if ifany == 0:
            input("Incorrect!, Correct answer: {}".format(correct_ans))
            return False


def print_questions(session):
    """
    This code does the following:
    1. Handle user input
    2. Get indexes of questions to be asked
    3. Timer
    4. Print questions
    """
    print("Enter the answer and hit enter")
    print("Enter ? to see the answer")
    print("Enter / to skip")
    print("Enter q to quit")

    # Get random indexes
    indexes = range(session.total_num_questions)
    # if session.resume is true, then sort indexes by the number of incorrects ; if there are more than 2 corrects then ignore the questions
    if session.resume:
        if session.reverse:
            indexes = sorted(
                indexes,
                key=lambda x: session.num_incorrects_r[x],
                reverse=True,
            )
            indexes = [i for i in indexes if session.num_corrects_r[i] < 2]
        else:
            indexes = sorted(
                indexes,
                key=lambda x: session.num_incorrects[x],
                reverse=True,
            )
            indexes = [i for i in indexes if session.num_corrects[i] < 2]
    indexes = random.sample(indexes, session.max_questions)

    # Start timer
    start_time = time.time()
    dict_wrongs = {}

    # Print questions
    for i in tqdm(indexes):
        if session.reverse:
            user_ans = input("{} : ".format(session.list_B[i]))
            if choice_while_answering(user_ans, session.list_A[i]):
                session.num_corrects_r[i] += 1
            else:
                session.num_incorrects_r[i] += 1
                dict_wrongs[session.list_B[i]] = session.list_A[i]
        else:
            user_ans = input("{} : ".format(session.list_A[i]))
            if choice_while_answering(user_ans, session.list_B[i]):
                session.num_corrects[i] += 1
            else:
                session.num_incorrects[i] += 1
                dict_wrongs[session.list_A[i]] = session.list_B[i]

        # Clear screen
        os.system("cls" if os.name == "nt" else "clear")
    # End timer and save time taken
    end_time = time.time()
    session.time_taken = end_time - start_time
    session.dict_wrongs = dict_wrongs


def setup_session(args):
    """This function sets up the session by asking the user for the number of questions and whether to reverse the pattern, and then creates a new session or restores a previous one"""
    data_file = pd.read_csv(args.data)
    # Print col names joined by '->' and ask user if they want to reverse
    print("Pattern: {} -> {}".format(data_file.columns[0], data_file.columns[1]))
    reverse = input("Reverse? (y/n): ")
    args.reverse = False
    if reverse == "y":
        args.reverse = True
        print("Pattern: {} -> {}".format(data_file.columns[1], data_file.columns[0]))

    # ask for number of questions and store
    num_questions = input("Number of questions: ")
    args.num_questions = int(num_questions) if num_questions else 30

    session = Session(args, data_file)

    session.create_new_session()
    # Check if previous session exists using a file called 'session.pkl'

    if os.path.isfile("./data/session.pkl"):
        resume = input("Resume previous session? (y/n): ")
        # Load previous session
        if resume == "y" or None:
            session.restore_session()
            session.resume = True
            print("Resuming previous session.")
        else:
            print("Starting a new session.")
    else:
        print("No previous session found.")
        print("Starting a new session.")
        # Create new session

    return session
