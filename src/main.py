# from fastapi import FastAPI, UploadFile, File, HTTPException
# from src.preprocessing import preprocess
# import uvicorn

# app = FastAPI(title="WhatsApp Chat Analysis API", description="API for analyzing WhatsApp chat data.", version="0.0.1")

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the WhatsApp Chat Analysis API. Use the /upload endpoint to upload a chat file."}

# @app.post("/upload-chat")
# async def upload_chat(file: UploadFile = File(...)):
#     if not file.filename.endswith('.txt'):
#         raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .txt file.")
    
#     try:
#         content = await file.read()
#         text = content.decode('utf-8-sig')
#         df = preprocess(text)

#         result_json = df.to_dict(orient='records')
        
#         return {"message": "File processed successfully", "data": result_json,"records_parsed": len(result_json)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")