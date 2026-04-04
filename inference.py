import requests
import os

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

TASKS = [
    "easy_detection",
    "mixed_traffic",
    "obfuscated_tunnel"
]



def decide_action(features):
    domain_length, request_freq, entropy, query_type = features

    # strong indicators
    if entropy > 0.6 and request_freq > 0.5:
        return 2  # block

    # suspicious patterns
    if entropy > 0.45:
        if request_freq > 0.3 or domain_length > 0.5:
            return 1  # investigate

    # stealth tunneling detection
    if request_freq > 0.6:
        return 1  # investigate

    # avoid false positives
    if entropy < 0.2 and request_freq < 0.2:
        return 0  # allow

    # fallback
    if entropy > 0.3:
        return 1
    else:
        return 0


def run_task(task_name):
    print(f"\nRunning task: {task_name}")

    res = requests.post(f"{BASE_URL}/reset", json={"task": task_name})
    state = res.json()["state"]

    total_reward = 0
    steps = 0

    while True:
        features = state["features"]

        action = decide_action(features)

        step_res = requests.post(
            f"{BASE_URL}/step",
            json={"action": action}
        ).json()

        total_reward += step_res["reward"]
        steps += 1

        if step_res["done"]:
            break

        state = step_res["state"]

    score = total_reward / max(1, steps)
    print(f"Score: {score:.4f}")


def main():
    for task in TASKS:
        run_task(task)


if __name__ == "__main__":
    main()