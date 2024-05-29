import argparse
import time
import threading
import mouse
import keyboard


def monitorMouseKeyboardEvents(stop_recording_key):
    """
    Monitor and record mouse and keyboard events until a specified key is pressed.

    This function starts recording mouse and keyboard events and stores them in
    separate lists. The recording stops when the specified key is pressed on the keyboard.

    Args:
        stop_recording_key (str): The key that stops the recording when pressed.

    Returns:
        tuple: A tuple containing two lists:
            - mouse_events (list): A list of recorded mouse events.
            - keyboard_events (list): A list of recorded keyboard events.
    """
    # These are the lists where all the events will be stored
    mouse_events = []
    keyboard_events = []
    
    # Start recording
    mouse.hook(mouse_events.append)  # Start recording mouse events
    keyboard.start_recording()       # Start recording keyboard events
    
    keyboard.wait(stop_recording_key)  # Waiting for the stop recording key to be pressed
    
    # Stop recording
    mouse.unhook(mouse_events.append)  # Stop recording mouse events
    keyboard_events = keyboard.stop_recording()  # Stop recording keyboard events
    
    return mouse_events, keyboard_events


def playMouseMouseKeyboardEvents(mouse_events, keyboard_events):
    """
    Play back recorded mouse and keyboard events simultaneously.

    This function plays back the recorded mouse and keyboard events in separate
    threads to ensure they are played simultaneously.

    Args:
        mouse_events (list): A list of recorded mouse events.
        keyboard_events (list): A list of recorded keyboard events.
    """
    # Playing the recorded keyboard events in a separate thread
    k_thread = threading.Thread(target=lambda: keyboard.play(keyboard_events))
    k_thread.start()
    
    # Playing the recorded mouse events in a separate thread
    m_thread = threading.Thread(target=lambda: mouse.play(mouse_events))
    m_thread.start()
    
    # Waiting for both threads to complete
    k_thread.join()
    m_thread.join()


def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Record and play back mouse and keyboard events.")
    parser.add_argument('duration_until_recording', type=float, help="Duration before recording starts.")
    parser.add_argument('duration_while_loop', type=float, help="Duration for the while loop to keep running.")
    parser.add_argument('duration_between_loops', type=float, help="Duration between each loop iteration.")
    parser.add_argument('-s', '--seconds', action='store_true', help="Duration in seconds.")
    parser.add_argument('-m', '--minutes', action='store_true', help="Duration in minutes.")
    parser.add_argument('-h', '--hours', action='store_true', help="Duration in hours.")
    parser.add_argument('-k', '--key', type=str, default='p', help="Key to stop recording (default: 'p').")
    
    return parser.parse_args()


def convert_duration(duration, seconds, minutes, hours):
    """
    Convert duration to seconds based on the given flags.

    Args:
        duration (float): The duration value.
        seconds (bool): Flag indicating if the duration is in seconds.
        minutes (bool): Flag indicating if the duration is in minutes.
        hours (bool): Flag indicating if the duration is in hours.

    Returns:
        float: The converted duration in seconds.
    """
    if minutes:
        return duration * 60
    elif hours:
        return duration * 3600
    else:
        return duration


if __name__ == "__main__":
    args = parse_arguments()
    duration_until_recording = convert_duration(args.duration_until_recording, args.seconds, args.minutes, args.hours)
    duration_while_loop = convert_duration(args.duration_while_loop, args.seconds, args.minutes, args.hours)
    duration_between_loops = convert_duration(args.duration_between_loops, args.seconds, args.minutes, args.hours)
    
    time.sleep(duration_until_recording)
    print("Start Recording Input...")
    mouse_events, keyboard_events = monitorMouseKeyboardEvents(args.key)
    
    start_time = time.time()
    end_time = start_time
    while end_time - start_time < duration_while_loop:
        playMouseMouseKeyboardEvents(mouse_events, keyboard_events)
        time.sleep(duration_between_loops)
        end_time = time.time()
