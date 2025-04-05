from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.session import engine
from models.user import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Backend API",
    description="FastAPI backend with user authentication and PostgreSQL integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
# Note: We'll add these in the next step
# from routers import auth, users
# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}
