from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import HTMLResponse

app = FastAPI()



@app.get("/ping")
def ping():
    return {"pong"}


@app.get("/home")
def hello():
    with open("hello.html","r",encoding= "utf-8") as file:
        html_content =file.read()
        return HTMLResponse(content=html_content)



class Posts(BaseModel):
    author: str
    title: str
    content: str
    creation_date: int

@app.post("/posts")
def add_posts(new_posts: List[Posts], posts=None):
    added = 0
    for post in new_posts:

        if not any(s["Reference"] == post.Reference for s in posts):
            posts.append(post.dict())
            added += 1
    return {
        "message": f"{added} posts ajouté(s)",
        "post": posts
    }


@app.get("/posts")
def get_posts(posts=None):
    return posts