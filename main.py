import uvicorn

if __name__ == "__main__":
    uvicorn.run("servers:fastjson", host="127.0.0.1", port=5000, log_level="error")
