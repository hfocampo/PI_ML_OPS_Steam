# Importamos galerias 

from fastapi import FastAPI
from routers.funciones import router as steam_router

app=FastAPI()#debug=True)

@app.get('/')
def message():
    return 'PROYECTO 1_PI_ML_OPS HECTOR OCAMPO GAVIRIA DATAFT-19'

app.include_router(steam_router)




