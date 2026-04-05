from fastapi import FastAPI
from model import Action, ResetRequest, ResetResponse, StepResponse, State
from env import DNSenv, easy_data, medium_data, hard_data
from typing import Optional
app = FastAPI()


env = None

@app.get("/")
def home():
    return {"message": "DNS Tunneling OpenEnv API is running"}
@app.post("/reset", response_model=ResetResponse)
def reset(req: Optional[ResetRequest] = None):

    global env

    task = "easy_detection"

    if req is not None and req.task is not None:
        task = req.task

    if task == "easy_detection":
        env = DNSenv(easy_data)
    elif task == "mixed_traffic":
        env = DNSenv(medium_data)
    elif task == "obfuscated_tunnel":
        env = DNSenv(hard_data)
    else:
        env = DNSenv(easy_data)

    state = env.reset()

    return ResetResponse(state=state)
@app.post("/step", response_model=StepResponse)
def step(action: Action):

    global env

    if env is None:
        state = DNSenv(easy_data).reset()
        return StepResponse(state=state, reward=0.0, done=False)

    return env.step(action.action)


@app.get("/state", response_model=State)
def state():

    global env

    if env is None:
        return State(features=[0.0, 0.0, 0.0, 0.0])

    current_state = env.state()

    if current_state is None:
        return State(features=[0.0, 0.0, 0.0, 0.0])

    return current_state

 
