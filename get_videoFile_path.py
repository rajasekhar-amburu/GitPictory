import os


def get_most_recent_file(folder_path="C:/Users/Rajasekhar/Downloads"):
    # Get a list of all files in the folder
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
             os.path.isfile(os.path.join(folder_path, f))]

    # If there are no files, return None
    if not files:
        return None

    # Get the most recently modified file
    most_recent_file = max(files, key=os.path.getmtime)

    if most_recent_file:
        print(f"The most recently downloaded file is: {most_recent_file}")
    else:
        print("No files found in the specified folder.")

    return most_recent_file
