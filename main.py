from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette import status
from starlette.responses import HTMLResponse, JSONResponse

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

@app.put("/posts")
def update_or_add_post(post: Posts, posts=None):
    for i, existing in enumerate(posts):
        if existing["Reference"] == post.Reference:
            posts[i] = post.dict()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Post mis à jour", "post": post.dict()}
            )


    posts.append(post.dict())
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Nouveau post ajouté", "post": post.dict()}
    )