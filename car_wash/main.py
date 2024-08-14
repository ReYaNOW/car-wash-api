from fastapi import FastAPI

from car_wash.users.router import router as users_router

app = FastAPI(title='Car Wash')

app.include_router(users_router)
