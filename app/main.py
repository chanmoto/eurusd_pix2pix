import uvicorn
import database as db
import services.dataframe as df
from fastapi import FastAPI
from routers import admin_router as admin
from routers import forex_router as forex
from routers import backtest_router as backtest
from routers import ml_router as ml
from configuration import APIConfigurations 

db.start_db()#データモデルを作成
df.initialize()#CSVデータを読み込む


app = FastAPI(
    title=APIConfigurations.title,
    description=APIConfigurations.description,
    version=APIConfigurations.version,
)

"""
app.include_router(forex.routering,prefix=f"/v{APIConfigurations.version}", tags=["forex"])
app.include_router(admin.router, prefix=f"/v{APIConfigurations.version}", tags=["admin"])
app.include_router(ml.router, prefix=f"/v{APIConfigurations.version}", tags=["ml"])
"""

app.include_router(forex.router, tags=["forex"])
app.include_router(admin.router,  tags=["admin"])
app.include_router(ml.router, tags=["ml"])
app.include_router(backtest.router, tags=["backtest"])


#APIの起動処理
@app.on_event("startup")
async def startup_event():
    print("*** startup event ***")

if __name__ == "__main__":

    uvicorn.run("main:app", host='0.0.0.0', port=80, reload=True)
    
