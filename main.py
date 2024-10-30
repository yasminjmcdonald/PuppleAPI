from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth, owners, dogs, admin

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(owners.router)
app.include_router(dogs.router)
app.include_router(admin.router)

