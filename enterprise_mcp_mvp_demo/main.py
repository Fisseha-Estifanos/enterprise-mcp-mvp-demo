from fastapi import FastAPI

from routes.auth_router import auth_router
from routes.user_router import user_router
from routes.role_router import role_router
from routes.server_router import server_router
from routes.request_router import request_router
from routes.permission_router import permission_router
from routes.association_router import association_router


app = FastAPI(title="Enterprise mcp mvp demo")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(server_router)
app.include_router(request_router)
app.include_router(permission_router)
app.include_router(association_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
    # reload=True)
