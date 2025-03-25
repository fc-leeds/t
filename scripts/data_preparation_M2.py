import os
import requests
from data_extraction_M1 import extract_answers_sequence

def download_answer_files(link, destination_folder, respondent_index):
    """Download a single respondent answer file from a Google Drive direct link and save it.
    
    Args:
        link (str): Direct Google Drive link to a file (e.g., a1.txt, a2.txt).
        destination_folder (str): Local folder where the file will be saved as answers_respondent_n.txt.
        respondent_index (int): Index to name the file (e.g., 1 for answers_respondent_1.txt).
    
    Returns:
        None
    
    Raises:
        ValueError: If the link is invalid, respondent_index is not a positive integer, or download fails.
        FileNotFoundError: If the destination folder cannot be created or accessed, or file isn’t saved.
    """
    if not isinstance(link, str):
        raise ValueError("link must be a string")
    if not isinstance(respondent_index, int) or respondent_index < 1:
        raise ValueError("respondent_index must be a positive integer")
    if "drive.google.com" not in link:
        raise ValueError(f"Link does not appear to be a valid Google Drive URL: {link}")
    
    # Ensure destination folder exists
    if not os.path.isdir(destination_folder):
        try:
            os.makedirs(destination_folder)
        except OSError as e:
            raise FileNotFoundError(f"Failed to create destination folder {destination_folder}: {str(e)}")
    
    # Extract file ID from URL and construct download link
    file_id = link.split("id=")[-1] if "id=" in link else link.split("/d/")[1].split("/")[0]
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    # Define the full path for saving the file
    local_filename = os.path.join(destination_folder, f"answers_respondent_{respondent_index}.txt")
    
    # Download and save the file
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
        # Verify the file was written
        if not os.path.isfile(local_filename):
            raise FileNotFoundError(f"File {local_filename} was not created after download")
    except requests.RequestException as e:
        raise ValueError(f"Failed to download file for respondent {respondent_index} from Google Drive: {str(e)}")

def collate_answers(data_folder_path):
    """Collate all respondent answer sequences into a single text file.
    
    Args:
        data_folder_path (str): Path to folder containing respondent answer files.
    
    Returns:
        list: List of lists, where each sublist is a respondent's 100-answer sequence.
    
    Raises:
        FileNotFoundError: If the data_folder_path does not exist or contains no valid files.
        ValueError: If any answer file fails to parse correctly.
    """
    if not os.path.isdir(data_folder_path):
        raise FileNotFoundError(f"Folder not found: {data_folder_path}")
    
    all_answers = []
    for filename in sorted(os.listdir(data_folder_path)):
        if filename.startswith("answers_respondent_") and filename.endswith(".txt"):
            file_path = os.path.join(data_folder_path, filename)
            try:
                answers = extract_answers_sequence(file_path)
                all_answers.append(answers)
            except (FileNotFoundError, ValueError) as e:
                raise ValueError(f"Error processing {filename}: {str(e)}")
    
    if not all_answers:
        raise FileNotFoundError(f"No valid answer files found in {data_folder_path}")
    
    with open(os.path.join(data_folder_path, "collated_answers.txt"), 'w') as f:
        for ans_seq in all_answers:
            f.write(','.join(map(str, ans_seq)) + '\n')
    
    return all_answers