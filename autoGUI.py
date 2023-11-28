import pyautogui
import time
import pickle


# Function to record cursor movements and clickable actions
def record_actions():
    actions = []
    try:
        while True:
            x, y = pyautogui.position()
            action = {
                'x': x,
                'y': y,
                'click': pyautogui.mouseDown(button='left')
            }
            actions.append(action)
            time.sleep(0.1)  # Record actions every 0.1 seconds
    except KeyboardInterrupt:
        pass

    # Save recorded actions to a file
    with open('actions.pkl', 'wb') as file:
        pickle.dump(actions, file)
    print('Actions recorded successfully.')


# Function to replay recorded actions
def replay_actions():
    # Load recorded actions from the file
    with open('actions.pkl', 'rb') as file:
        actions = pickle.load(file)

    # Replay recorded actions
    for action in actions:
        pyautogui.moveTo(action['x'], action['y'])
        if action['click']:
            pyautogui.mouseDown(button='left')
        time.sleep(0.1)  # Pause for 0.1 seconds between actions


# Main function
if __name__ == '__main__':
    print('Press Ctrl + C to stop recording.')
    record_actions()

    # Uncomment the following line to replay the recorded actions
    # replay_actions()
