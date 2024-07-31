#!/usr/bin/env python
import sys
from fitmentiq.crew import FitmentiqCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    resumes = ["/home/asi/new_proj/fitmentiq/src/fitmentiq/data/Resumes/CHANDAN_VK_RESUME.pdf", ]
    job_description = "/home/asi/new_proj/fitmentiq/src/fitmentiq/data/JD/sample-job-description.pdf"

    dataset = [{"job_description": job_description, "resumes": resume_path} for resume_path in resumes]
    FitmentiqCrew().crew().kickoff_for_each(inputs=dataset)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        FitmentiqCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        FitmentiqCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
