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

positive_words = {
    "love","great","good","excellent","awesome","happy",
    "wonderful","amazing","fantastic","best","nice",
    "brilliant","perfect","enjoy","like"
}

negative_words = {
    "bad","terrible","awful","hate","sad",
    "worst","horrible","poor","angry",
    "disappointing","disappointed","useless",
    "boring","annoying"
}

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
