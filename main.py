from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv, find_dotenv
from routes.chat import chat_router
from routes.files import file_upload_router
from database import Base, engine


import sys
sys.stdout.reconfigure(encoding='utf-8')



app = FastAPI()


app.include_router(chat_router)
app.include_router(file_upload_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "Server running"}




if __name__ == "__main__":
    load_dotenv(find_dotenv())
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, port=8070)
    
    
    
    
    
    

    
    
    
    
    
    


