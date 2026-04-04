import pandas as pd
from typing import List,Dict

DATA_PATH="dataset.csv"

df=pd.read_csv(DATA_PATH)

QUERY_MAP={
    'A':0,
    'AAAA':1,
    'MX':2,
    'TXT':3,
    'CNAME':4

}

def row_to_features(row) -> List[float]:
    return[
        float(row["domain_length"])/100.00,
         float(row["request_frequency"]) / 1000.0,     
        float(row["entropy"]) / 8.0,                  
        float(QUERY_MAP.get(row["query_type"], 0)) 
    ]


def process_dataframe(dataframe)-> List[Dict]:
    data=[]
    for _,row in dataframe.iterrows():
        data.append({
            "features": row_to_features(row),
            "label": row['label']
        })
    return data

def generate_eay_dataset()-> List[Dict]:
    data=df[df["difficulty"]=='easy']
    return process_dataframe(data)
def generate_medium_dataset() -> List[Dict]:
    data = df[df["difficulty"] == "medium"]
    return process_dataframe(data)


def generate_hard_dataset() -> List[Dict]:
    data = df[df["difficulty"] == "hard"]
    return process_dataframe(data)


TASKS={
    "easy_detection": generate_eay_dataset,
    "mixed_traffic": generate_medium_dataset,
    "obfuscated_tunnel": generate_hard_dataset
}


def get_task_data(task_name: str)-> List[Dict]:
    if task_name not in TASKS:
        raise ValueError(f"Unknown task: {task_name}")
    return TASKS[task_name]()