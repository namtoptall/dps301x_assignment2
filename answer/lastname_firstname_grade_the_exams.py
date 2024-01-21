import os
import pandas as pd
import numpy as np

# Set the predefined answer key as a list
answer_key = ['B', 'A', 'D', 'D', 'C', 'B', 'D', 'A', 'C', 'C', 'D', 'B', 'A', 'B', 'A', 'C', 'B', 'D', 'A', 'C', 'A', 'A', 'B', 'D', 'D']

# function for task 1: open file
def open_file(folder, filename):
    file_path = os.path.join(folder, filename)
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"File '{filename}' cannot be found in the '{folder}' folder. Please try again.")
    return [] 

# get the answer key 
def get_answer_key(data_lines):
    if data_lines:
        first_line = data_lines[0].strip().split(',')
        if len(first_line) == 26 and first_line[0].startswith('N'):
            return ','.join(first_line[1:])

# function for task 2: validation and prints out the data
def validation(line):
    parts = line.strip().split(',')
    return (
        len(parts) == 26
        and parts[0].startswith('N')
        and parts[0][1:].isdigit()
        and len(parts[0]) == 9
    )

def analyze_data(data_lines):
    total_lines = len(data_lines)
    valid_lines = 0
    invalid_lines = 0

    for line in data_lines:
        if validation(line):
            valid_lines += 1
        else:
            invalid_lines += 1
            print(f"Invalid line of data: {line}")

    print("**** REPORT ****")
    print(f"Total valid lines of data: {valid_lines}")
    print(f"Total invalid lines of data: {invalid_lines}")

# task 3: grade 
def grade_exam(answer_key, data_lines):
    """
    Grade the exam for each student based on the provided answer key.

    Parameters:
    - answer_key (list): A list representing the correct answers to the exam.
    - data_lines (list): A list of strings, each representing a line of student responses.

    Returns:
    - scores (list): A list of integers representing the scores for each student.
    """
    # Initialize variables to store scores and track skipped/wrong answers
    scores = []
    skipped_questions = {}
    wrong_answers = {}

    # Iterate through each line of student responses
    for line in data_lines:
        parts = line.strip().split(',')
        student_id = parts[0]
        student_answers = parts[1:]

        # Skip invalid lines
        if not validation(line):
            continue

        # Initialize variables for the current student
        score = 0
        skipped = 0
        wrong = 0

        # Iterate through each answer in the student's responses
        for i, answer in enumerate(student_answers):
            if answer == '':
                # Record skipped question
                skipped += 1
                if i + 1 not in skipped_questions:
                    skipped_questions[i + 1] = 1
                else:
                    skipped_questions[i + 1] += 1
            elif answer == answer_key[i]:
                # Award 4 points for a correct answer
                score += 4
            else:
                # Record wrong answer
                wrong += 1
                if i + 1 not in wrong_answers:
                    wrong_answers[i + 1] = 1
                else:
                    wrong_answers[i + 1] += 1

        # Ensure the score is non-negative
        scores.append(max(score, 0))

    # Calculate and print statistics
    high_scores = sum(score > 80 for score in scores)
    mean_score = round(np.mean(scores), 2)
    highest_score = max(scores)
    lowest_score = min(scores)
    score_range = highest_score - lowest_score
    sorted_scores = sorted(scores)
    middle_index = len(sorted_scores) // 2

    if len(sorted_scores) % 2 == 1:
        median_score = sorted_scores[middle_index]
    else:
        median_score = (sorted_scores[middle_index - 1] + sorted_scores[middle_index]) / 2

    print("\n**** REPORT ****")
    print(f"Total valid lines of data: {len(scores)}")
    print(f"Total invalid lines of data: {len(data_lines) - len(scores)}")

    print(f"\nTotal students with high scores (>80): {high_scores}")
    print(f"Mean (average) score: {mean_score}")
    print(f"Highest score: {highest_score}")
    print(f"Lowest score: {lowest_score}")
    print(f"Range of scores: {score_range}")
    print(f"Median score: {median_score}")

    print("\nQuestions that most people skip:")
    for question, count in sorted(skipped_questions.items(), key=lambda x: x[1], reverse=True):
        skip_percentage = round(count / len(scores), 2)
        print(f"{question} - {count} - {skip_percentage}")

    print("\nQuestions that most people answer incorrectly:")
    for question, count in sorted(wrong_answers.items(), key=lambda x: x[1], reverse=True):
        wrong_percentage = round(count / len(scores), 2)
        print(f"{question} - {count} - {wrong_percentage}")

    return scores

def save_result(folder, class_name, student_ids, scores):
    """
    Save the grades of students to a CSV file.

    Parameters:
    - folder (str): The folder where the result file will be saved.
    - class_name (str): The name of the class or the input filename (excluding extension).
    - student_ids (list): A list of student IDs corresponding to the grades.
    - scores (list): A list of integers representing the scores for each student.

    Returns:
    None
    """
    # Create the output folder if it doesn't exist
    output_folder = os.path.join(folder, "class_grades")
    os.makedirs(output_folder, exist_ok=True)

    # Define the output filename
    output_filename = os.path.join(output_folder, f"{class_name}_grades.txt")

    # Create a DataFrame to store the student IDs and scores
    data = {'Student_ID': student_ids, 'Score': scores}
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv(output_filename, index=False)

# Main program
def main():
    while True:
        class_name = input("Enter a class to grade (e.g., class1 for class1.txt): ")
        if class_name.lower() == 'exit':
            break

        data_lines = open_file("data", f"{class_name}.txt")

        if data_lines:
            print(f"**** ANALYZING {class_name} ****")

            # Analyze data and get scores using the predefined answer key
            scores = grade_exam(answer_key, data_lines)

            # Extract student IDs
            student_ids = [line.strip().split(',')[0] for line in data_lines if validation(line)]

            # Save grades to file in class_grades folder
            save_result("data", class_name, student_ids, scores)
            print(f"\nGrades saved to class_grades/{class_name}_grades.txt")

        else:
            print(f"Failed to open {class_name}.txt")

if __name__ == "__main__":
    main()
