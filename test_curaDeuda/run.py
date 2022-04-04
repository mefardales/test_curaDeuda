import uvicorn
import os

hostipapi = os.getenv("HOST") or "0.0.0.0"
portipapi = os.getenv("PORT") or '8000'
debugd = os.getenv("DEBUG") or '0'
if debugd == '0':
    DEBUG = True
else:
    DEBUG = False

if __name__ == '__main__':
    uvicorn.run("api:app",
            host=hostipapi,
            port=int(portipapi),
            lifespan='on',
            timeout_keep_alive=5,
            reload=DEBUG
            )
