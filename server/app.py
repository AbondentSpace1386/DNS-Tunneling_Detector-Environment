import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app

def main():
    return app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
