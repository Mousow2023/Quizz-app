import requests
import string
import re
import json
import sys
import random
from tabulate import tabulate
from helpers import save_quiz, load_quizzes


class Quizz:
    def __init__(
        self, num_questions, category=None, difficulty=None, quiz_type=None
    ):
        # Initialize quiz attributes
        self.category = category
        self.difficulty = difficulty
        self.num_questions = num_questions
        self.quiz_type = quiz_type
        self.score = 0


    def fetch_questions(self):
        # Fetch quiz questions from the API based on category, difficulty, and number of questions
        base_url = "https://opentdb.com/api.php?"

        # Construct the parameters dictionary
        parameters = {"amount": self.num_questions}

        # Add additional parameters if provided
        if self.category is not None:
            parameters["category"] = self.category
        if self.difficulty is not None:
            parameters["difficulty"] = self.difficulty
        if self.quiz_type is not None:
            parameters["type"] = self.quiz_type

        # Construct the final URL with parameters
        api_url = f"{base_url}{'&'.join(f'{k}={v}' for k, v in parameters.items())}"
        
        obj = requests.get(api_url).json()
        return obj


    def store_questions(self):
        # Get the fetched questions and store them in a list of questions
        fetched_questions = self.fetch_questions()
        questions = [
            {
                "question": question["question"],
                "correct_answer": question["correct_answer"],
                "incorrect_answers": question["incorrect_answers"],
                "answers": [question["correct_answer"]] + question["incorrect_answers"]
            }
            for question in fetched_questions["results"]
        ]

        for question in questions:
            random.shuffle(question["answers"])
        return questions


    def display_question(self, n, question):
        # Display a quiz question to the user
        print(n, end=". ")

        print(question["question"].replace("&quot;", "'").replace("&#039;", "'").replace("&lt;", "<").replace("&gt;", ">"))
        print()
        answers = [question["correct_answer"]] + question["incorrect_answers"]
        random.shuffle(answers)

        # Get the index of the correct answer
        correct_index = answers.index(question["correct_answer"])
        letter_index = string.ascii_lowercase[correct_index]

        for idx, answer in enumerate(answers):
            index = string.ascii_lowercase[idx]
            formatted_answer = answer.replace("&quot;", "'").replace("&#039;", "'").replace("&lt;", "<").replace("&gt;", ">")
            print(f"{index}. {formatted_answer}")
        
        for _ in range(3):
            user_answer = input("Choose the correct answer: ").lower()
        
            try:
                index = ord(user_answer) - ord("a")
                if 0 <= index < len(answers):
                    break
                else:
                    print("Invalid Choice")

            except ValueError:
                raise ValueError("Invalid Answer")
        
        if not (0 <= index < len(answers)):
            return f"The correct answer is {letter_index}. {question['correct_answer']}"

        elif answers[index] == question["correct_answer"]:
            # Update the score
            self.score += 1
            return "CORRECT ✅"
        else:
            # correct_index = next(i for i, ans in enumerate(answers) if ans == question["correct_answer"])
            print("INCORRECT ❌")
            return f"The correct answer is {letter_index}. {question['correct_answer']}"


    def score_question(self, user_answer, correct_answer):
        # Score a user's answer and update the quiz score
        pass

    def display_score(self):
        # Display the final score to the user
        pass

def main():
    file = "quizzes.csv"

    while True:
        print("\nQuizz App Menu:")
        print("1. Take a Quiz")
        print("2. View Preview Sessions")
        print("3. Quit")

        choice = input("Enter your choice: ")
        match choice:
            case "1":
                preferences = get_user_preferences()
                # print(preferences)
                quiz = Quizz(*preferences[:4])
                # quiz = Quizz(num_questions="2", category=11, difficulty="easy", quiz_type="multiple")
                questions = quiz.store_questions()
                for i, question in enumerate(questions):
                    print(quiz.display_question(i + 1, question))
                    print()
                
                score = f"{quiz.score}/{quiz.num_questions}"
                print(f"Score: {score}")

                # Save the quiz in csv file
                quiz_dict = {"category": preferences[-1], "difficulty": quiz.difficulty, "score": score}
                save_quiz(quiz_dict, file)

            case "2":
                quizzes = load_quizzes(file)
                print(tabulate(quizzes, headers="keys", tablefmt="fancy_grid"))
                pass

            case "3":
                sys.exit("Quitting the Quizz App")

            case _:
                print("Invalid command")


def get_user_preferences():
    # Get user preferences for quiz category, difficulty, and number of questions
    # Get the number of questions
    number_of_questions = input("How many questions would you like? ").strip()
    if number_of_questions:
        try:
            if int(number_of_questions) > 50:
                sys.exit("Maximum number of questions if 50")

        except ValueError:
            raise ValueError("Invalid number of questions")
    else:
        number_of_questions = 10

    # Get the category:
    categories_obj = requests.get("https://opentdb.com/api_category.php").json()
    categories = categories_obj["trivia_categories"]

    print("Choose a category:")
    print("1. Any Category")
    for i, category in enumerate(categories, 2):
        print(f"{i}. {category['name']}")

    try:
        category = int(input("\nEnter a category number ").strip())
        if category == 1:
            choosen_category = None
            category_name = "Any Category"

        elif 0 < category < len(categories) + 2:
            choosen_category = categories[category - 2]["id"]
            category_name = categories[category - 2]["name"]

        else:
            raise ValueError("Invalid category number")

    except ValueError:
        raise ValueError("Invalid category number")

    # Get the difficulty
    difficulties = ["Any Difficulty", "Easy", "Medium", "Hard"]
    print("Choose difficulty:")
    for i, difficulty in enumerate(difficulties, 1):
        print(f"{i}. {difficulty}")

    difficulty = int(input("\nEnter difficulty number ").strip())

    if difficulty != 1:
        if 0 < difficulty < len(difficulties) + 1:
            difficulty = difficulties[difficulty - 1].lower()
        else:
            raise ValueError("Invalid difficulty")
    else:
        difficulty = None

    # Get the type
    types = ["Any type", "multiple choice", "True/False"]
    print("Choose type")
    for i, typ in enumerate(types, 1):
        print(f"{i}. {typ.title()}")

    preferred_type = int(input("\nEnter type number ").strip())

    if preferred_type == 1:
        preferred_type = None
    elif preferred_type == 2:
        preferred_type = "multiple"
    elif preferred_type == 3:
        preferred_type = "boolean"
    else:
        raise ValueError("Invalid difficulty")

    # except ValueError as ve:
    # print(f"Error: {ve}")
    # You might want to handle this exception more gracefully, e.g., by asking the user to input again.

    return (number_of_questions, choosen_category, difficulty, preferred_type, category_name)


def test():
    pass

if __name__ == "__main__":
    main()
