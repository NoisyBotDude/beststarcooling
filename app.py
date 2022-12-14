from venv import create
from api import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":
    uvicorn.run("__main__:app",host = '0.0.0.0',port = 5000, reload = True)