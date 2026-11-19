import os
import requests

# This allows your application to communicate with OpenAI models through an API
from openai import OpenAI

#This package loads environment variables from a .env file into the Python environment Loads variables from your .env file
from dotenv import load_dotenv

# Access tools.py and use functions read_logs and classify_error
from tools import read_logs, classify_error

# Load .env file to access which have the API key for OpenAI
load_dotenv()

# Verify API and load API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is missing")
client = OpenAI(api_key=api_key)

# Start agebt
def run_agent():

    print("Starting DevOps AI Agent...")

    # Opens the file, reads its contents, and returns the log data.
    logs = read_logs("logs/sample_error.log")

    # Takes the pipeline logs and identifies the error categoryr
    error_type = classify_error(logs)

    print(f"Detected error: {error_type}")

    # Takes the pipeline logs and identifies the error category
    response = client.responses.create(
        # Establishes the model's behavioral requirements and task context.
        # Note 1: instructions - Defines how the model should behave (What should you do)
        # Note 2: input - Supplies the information the model must analyze (What information should you use)
        model="gpt-6-luna",
        # Defining the AI application's operating policy
        instructions="""
        You are an experienced DevOps engineer.

        Analyze CI/CD pipeline errors.

        Identify:
        #1. Root cause
        #2. Severity
        #3. Recommended solution
        #4. Prevention steps

        Never execute remediation commands.
        Only recommend actions.
        """,
        # Actual information being analyzed. Using a Python f-string to dynamically insert variables into the prompt.
        input=f"""
        Error type: {error_type}

        Pipeline logs:
        {logs}
        """
    )
    # Retrieve generated text from a Responses API result.
    # Note 1: response - contains the API response object.
    # Note 2: response.output_text - extracts the generated textual content.
    # Note 3: report - stores that content for your application to use
    report = response.output_text
    # Ensures that the output directory exists
    os.makedirs("reports", exist_ok=True)
    
    # Writes the AI-generated analysis to a text file.
    with open(
        "reports/incident_report.txt",
        "w"
    ) as file:
        file.write(report)

    print("\nAI Incident Report:")
    print(report)


if __name__ == "__main__":
    run_agent()
