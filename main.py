import pandas as pd


def process_topic(topic_name):
    try:
        import pictory_main
        print("Sending the topic-name", topic_name, "to pictory_main.py file")
        ret_val = pictory_main.pictory_automation(topic_name)
        if ret_val:
            print("Video for :", topic_name, "is successfully uploaded. Back to main.py")
        else:
            print("Some Error occurred while requesting / creating / uploading the video for :", topic_name)
        return ret_val
    except Exception as exp:
        print("Exception occurred in main.py - process_topic :", exp)


# Load the Excel file
file_path = 'D:\\PictoryTopicsList\\Topics.xlsx'
df = pd.read_excel(file_path, sheet_name='List-1')

# Iterate through each row (excluding the header)
for index, row in df.iterrows():

    sno = row['Sno']
    topic_name = row['Topic Name']
    print("Picked the topic :", topic_name, "at S.No", sno)
    # Convert 'Status' to a string and set to 'Not Started' if NaN
    status = str(row['Status']).lower() if pd.notna(row['Status']) else 'Not Started'

    if status in ['Completed', 'completed']:
        # Skip already in-progress topics
        print("The status of the topic :", topic_name, "is showing completed. So skipping this topic")
        continue

    # Set status to In-Progress
    df.at[index, 'Status'] = 'In-Progress'
    print("Setting the status as In-Progress for the topic :", topic_name)

    # Save the changes to the Excel file after setting status to In-Progress
    df.to_excel(file_path, sheet_name='List-1', index=False)

    return_value = process_topic(topic_name)

    if return_value:
        # Set status to Completed
        df.at[index, 'Status'] = 'Completed'

        print("Setting the status as Completed for the topic :", topic_name)
        # Save the changes to the Excel file after processing each topic
        df.to_excel(file_path, sheet_name='List-1', index=False)

print("All topics processed and changes saved.")
