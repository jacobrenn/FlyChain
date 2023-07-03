import shutil
import csv
import os

chat = {'msg': None, 'bot_msg': None, 'binary_feedback' : None, 'correction' : None}

def binary_feedback_handler(choice):
    binary_feedback = 1 if choice == 'Upvote' else -1
    chat['binary_feedback'] = binary_feedback

def correction_feedback_handler(correction):
    chat['correction'] = correction

def submit_feedback():
    if chat['msg'] is not None and chat['bot_msg'] is not None:
        save_to_csv(chat['msg'], chat['bot_msg'], chat['binary_feedback'], chat['correction'])
        chat['msg'] = None
        chat['bot_msg'] = None
        chat['binary_feedback'] = None
        chat['correction'] = None

def save_to_csv(msg, bot_msg, value, correction = None):
    csv_exists = os.path.isfile('./feedback.csv')
    with open('./feedback.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if not csv_exists:
            writer.writerow(['user_prompt', 'bot_response', 'binary_feedback', 'correction'])
        writer.writerow([msg, bot_msg, value, correction])

def save_to_downloads():
    filename = 'feedback.csv'
    home = os.path.expanduser("~")
    if os.name == 'nt':  # If the OS is Windows
        downloads_folder = os.path.join(home, 'Downloads')
    else:                # For UNIX, Linux, MacOS, etc.
        downloads_folder = os.path.join(home, 'Downloads')
        
    src_file = os.path.join(os.getcwd(), filename)
    dst_file = os.path.join(downloads_folder, filename)

    if not os.path.isfile(src_file):
        print(f"No such file {src_file} in the current directory.")
        return

    try:
        shutil.copy2(src_file, dst_file)
        print(f"File {filename} has been copied to {downloads_folder}")
    except PermissionError:
        print(f"Permission denied: could not copy {filename} to {downloads_folder}")
    except Exception as e:
        print(f"An error occurred while copying {filename} to {downloads_folder}: {e}")

def delete_csv():
    filename = 'feedback.csv'
    if os.path.isfile(filename):
        try:
            os.remove(filename)
            print(f"File {filename} has been successfully deleted.")
        except Exception as e:
            print(f"Error occurred while deleting file {filename}: {e}")
    else:
        print(f"No such file {filename} in the current directory.")