import requests
import os

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

TASKS = [
    "easy_detection",
    "mixed_traffic",
    "obfuscated_tunnel"
]


# -------------------------------
# Simple safe agent
# -------------------------------
def decide_action(features):
    domain_length, request_freq, entropy, query_type = features

    if entropy > 0.5:
        return 2
    elif entropy > 0.3 or request_freq > 0.5:
        return 1
    else:
        return 0


# -------------------------------
# Run one task safely
# -------------------------------
def run_task(task_name):
    print(f"\nRunning task: {task_name}")

    try:
        res = requests.post(f"{BASE_URL}/reset", json={"task": task_name}, timeout=10)
        data = res.json()
    except Exception as e:
        print("Reset request failed:", e)
        return

    if "state" not in data:
        print("Reset failed:", data)
        return

    state = data["state"]

    total_reward = 0
    steps = 0

    while True:
        try:
            features = state.get("features", [])
            if not features:
                print("Invalid state:", state)
                break

            action = decide_action(features)

            step_res = requests.post(
                f"{BASE_URL}/step",
                json={"action": action},
                timeout=10
            )

            data = step_res.json()

        except Exception as e:
            print("Step request failed:", e)
            break

        reward = data.get("reward", 0)
        done = data.get("done", True)

        total_reward += reward
        steps += 1

        if done:
            break

        if "state" not in data:
            print("Missing state in response:", data)
            break

        state = data["state"]

    if steps > 0:
        score = total_reward / steps
        print(f"Score: {score:.4f}")
    else:
        print("No steps executed")


# -------------------------------
# MAIN
# -------------------------------
def main():
    for task in TASKS:
        run_task(task)


if __name__ == "__main__":
    main()
