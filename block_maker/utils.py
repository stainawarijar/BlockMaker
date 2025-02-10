import datetime

def write_to_log(message):
    '''Write message to log file with date and time'''
    with open("BlockMaker.log", "a") as file:  # Use "a" to append to the file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if message.startswith("Start processing sequence"):
            # Add empty line before new sequence
            file.write(f"\n\n{timestamp}\t{message}")
        else:
            file.write(f"\n{timestamp}\t{message}")

