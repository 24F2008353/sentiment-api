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
    t = text.lower()

    positive_words = [
        "love","like","good","great","excellent","awesome","amazing",
        "fantastic","wonderful","best","happy","brilliant","perfect",
        "nice","super","outstanding","incredible","beautiful",
        "enjoy","recommend","favorite","win","cool","fun"
    ]

    negative_words = [
        "bad","terrible","awful","hate","sad","worst","horrible",
        "poor","angry","disappointing","failure","failed","useless",
        "boring","annoying","problem","issue","broken","bug"
    ]

    pos = sum(1 for w in positive_words if w in t)
    neg = sum(1 for w in negative_words if w in t)

    if pos > neg:
        return "happy"
    elif neg > pos:
        return "sad"
    else:
        return "neutral"
        
def classify(text: str):
    text = text.lower()

    pos = sum(word in text for word in positive_words)
    neg = sum(word in text for word in negative_words)

    if pos > neg:
        return "happy"
    elif neg > pos:
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
