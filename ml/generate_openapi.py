import json
from main import app

def main():
    spec = app.openapi()
    with open("openapi_generated.json", "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    print("Wrote openapi_generated.json")

if __name__ == '__main__':
    main()
