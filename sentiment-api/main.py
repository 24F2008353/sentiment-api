from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: list[str]

def classify(text: str):
    text = text.lower()

    positive = [
        "love","great","good","excellent","awesome","amazing",
        "fantastic","wonderful","best","happy","perfect","nice",
        "recommend","thanks","thank you","helpful","useful",
        "success","successful","enjoy","liked"
    ]

    negative = [
        "bad","terrible","awful","hate","worst","horrible",
        "sad","poor","problem","issue","broken","bug",
        "error","failed","failure","annoying","disappointing"
    ]

    for word in positive:
        if word in text:
            return "happy"

    for word in negative:
        if word in text:
            return "sad"

    return "neutral"
    
@app.post("/sentiment")
def sentiment(req: SentimentRequest):
    return {
        "results": [
            {
                "sentence": s,
                "sentiment": classify(s)
            }
            for s in req.sentences
        ]
    }

@app.get("/")
def root():
    return {"status": "ok"}

@app.head("/")
def root_head():
    return {}
