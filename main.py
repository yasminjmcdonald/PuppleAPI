from fastapi import FastAPI
import models
from database import engine
from routers import auth, owners, dogs, admin

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(owners.router)
app.include_router(dogs.router)
app.include_router(admin.router)

