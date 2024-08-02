#!/usr/bin/env python
import sys
from fitmentiq.crew import FitmentiqCrew
import subprocess

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    command = ["streamlit", "run", "src/fitmentiq/app.py"]

# Start the process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Capture the output and error (if any)
    stdout, stderr = process.communicate()

    # Print the output and error
    print("Output:\n", stdout)
    print("Error:\n", stderr)

    # Check the return code
    return_code = process.returncode
    print("Return code:", return_code)


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         FitmentiqCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         FitmentiqCrew().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")
