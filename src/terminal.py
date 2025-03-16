import readline
from commands import execute_command
history = []

def fake_terminal():
    while True:
        try:
            command = input("> ").strip().lower()

            if command:
                history.append(command)
            
            if command == "exit":
                print("Exiting...")
                break
            
            execute_command(command)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
