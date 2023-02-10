import json, uuid

def readJson(path: str) -> list | dict:
    try:
        with open(path) as file:
            data = json.load(file)

        if not data:
            return []

        return data
    except Exception as e:
        print(e)
        return []
     
def writeJson(path: str, mode: str = 'w', *, data: dict):
    try:
        with open(path, mode) as file:
            file.write(json.dumps(data))
    except Exception as e:
        print(e)

def generateUUID() -> str:
    return str(uuid.uuid4())