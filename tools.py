def read_logs(file_path):

    with open(file_path, "r") as file:
        logs = file.read()

    return logs


def classify_error(logs):

    if "ModuleNotFoundError" in logs:
        return "Dependency Error"

    if "Permission denied" in logs:
        return "Permission Error"

    if "Connection refused" in logs:
        return "Network Error"

    if "Exit code: 1" in logs:
        return "Application Failure"

    return "Unknown Error"