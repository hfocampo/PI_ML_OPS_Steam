# Importamos galerias 

from fastapi import FastAPI
from routers.funciones import router as steam_router
#import pandas as pd 
#from sklearn.metrics.pairwise        import cosine_similarity
#from sklearn.metrics.pairwise        import linear_kernel
#from sklearn.feature_extraction.text import TfidfVectorizer


app=FastAPI()#debug=True)

@app.get('/')
def message():
    return 'PROYECTO INTEGRADOR ML OPS 01 HECTOR OCAMPO GAVIRIA DATAFT-19'

app.include_router(steam_router)




