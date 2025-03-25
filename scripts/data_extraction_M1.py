def extract_answers_sequence(file_path):
    """Extract a respondent's answers from a quiz text file into a sequence.
    
    Args:
        file_path (str): Path to the respondent's answer text file (e.g., 'answers_respondent_1.txt').
    
    Returns:
        list: List of 100 integers where each is 1, 2, 3, 4 (answer selected) or 0 (unanswered).
    
    Raises:
        FileNotFoundError: If the specified file_path does not exist.
        ValueError: If the file does not contain exactly 100 questions or is malformed.
    """
    answers = []
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            i = 0
            question_num = 1
            while question_num <= 100 and i < len(lines):
                if lines[i].startswith(f"Question {question_num}."):
                    opts = lines[i + 1:i + 5]
                    if len(opts) != 4:
                        raise ValueError(f"Malformed question block at Question {question_num} in {file_path}")
                    answer = 0  # Unanswered default
                    for j, opt in enumerate(opts, 1):
                        if '[x]' in opt:
                            answer = j
                            break
                    answers.append(answer)
                    question_num += 1
                    i += 5
                else:
                    i += 1
        if len(answers) != 100:
            raise ValueError(f"Expected 100 questions, found {len(answers)} in {file_path}")
        return answers
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

def write_answers_sequence(answers, n):
    """Write an answer sequence to a text file.
    
    Args:
        answers (list): List of 100 integers representing the respondent's answers.
        n (int): Respondent identifier (e.g., 1 for 'respondent_1').
    
    Returns:
        None
    
    Raises:
        ValueError: If answers list does not contain exactly 100 elements.
        TypeError: If answers is not a list or n is not an integer.
    """
    if not isinstance(answers, list):
        raise TypeError("answers must be a list")
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if len(answers) != 100:
        raise ValueError("answers must contain exactly 100 elements")
    with open(f"answers_list_respondent_{n}.txt", 'w') as f:
        f.write(','.join(map(str, answers)))