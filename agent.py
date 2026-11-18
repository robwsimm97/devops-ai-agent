import os
import requests


from openai import OpenAI
from dotenv import load_dotenv

from tools import read_logs, classify_error

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def run_agent():

    print("Starting DevOps AI Agent...")

    # Tool 1: Read pipeline logs
    logs = read_logs("logs/sample_error.log")

    # Tool 2: Classify the error
    error_type = classify_error(logs)

    print(f"Detected error: {error_type}")

    # AI reasoning
    response = client.responses.create(
        model="gpt-6-luna",
        instructions="""
        You are an experienced DevOps engineer.

        Analyze CI/CD pipeline errors.

        Identify:
        1. Root cause
        2. Severity
        3. Recommended solution
        4. Prevention steps

        Never execute remediation commands.
        Only recommend actions.
        """,
        input=f"""
        Error type: {error_type}

        Pipeline logs:
        {logs}
        """
    )

    report = response.output_text

    os.makedirs("reports", exist_ok=True)

    with open(
        "reports/incident_report.txt",
        "w"
    ) as file:
        file.write(report)

    print("\nAI Incident Report:")
    print(report)


if __name__ == "__main__":
    run_agent()