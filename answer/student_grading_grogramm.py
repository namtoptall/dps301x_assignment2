import os

# function for task 1 : open file
def open_file(folder, filename):
    file_path = os.path.join(folder, filename)
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"File '{filename}' cannot be found in the '{folder}' folder. Please try again.")
    return [] 

# function for task 2 : validation and prints out the data
def validation(line):
    '''
    check if there is valid line 
    parameters: line
    '''
    parts = line.strip().split(',')
    if len(parts) != 26:
        return False
    if not (parts[0].startswith('N') and parts[0][1:].isdigit() and len(parts[0]) == 9):
        return False
    return True

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


def main():
    data_folder = "data"
    answer_folder = "answer"

    while True:
        filename = input("Enter a class file to grade (e.g., class1 for class1.txt): ")
        if filename.lower() == 'exit':
            break

        data_lines = open_file(data_folder, f"{filename}.txt")
        if data_lines:
            print(f"Successfully opened {filename}.txt")
            print("**** ANALYZING ****")
            analyze_data(data_lines)

if __name__ == "__main__":
    main()