from fastapi import FastAPI
from starlette.responses import HTMLResponse
app = FastAPI()

@app.get("/helo")
def hello():
    with open("hello.html","r",encoding= "utf-8") as file:
        html_content =file.read()
        return HTMLResponse(content=html_content)

