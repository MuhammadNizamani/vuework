import os

import uvicorn

ENV: str = os.getenv("ENV", "dev").lower()
if __name__ == "__main__":
    uvicorn.run(
        "server.backend:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        workers=int(os.getenv("WORKERS", 4)),
        reload=ENV == "dev",
    )