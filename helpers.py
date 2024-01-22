import csv
import os

# Save quiz
def save_quiz(quiz_dict, file_path):
    is_empty = os.path.getsize(file_path) == 0

    with open(file_path, "a", newline="") as file:
        fieldnames = ["category", "difficulty", "score"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if is_empty:
            writer.writeheader()
        writer.writerow(quiz_dict)


# Load quizzes from quizzes file
def load_quizzes(file_path):
    with open(file_path) as file:
        reader = csv.DictReader(file)

        quizzes_list = [quiz for quiz in reader]

        return quizzes_list