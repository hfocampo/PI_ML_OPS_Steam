from fastapi import APIRouter
import pandas as pd
from sklearn.metrics.pairwise        import cosine_similarity
from sklearn.metrics.pairwise        import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


router = APIRouter()

df = pd.read_csv('DataSet_Final.csv')
df_games = pd.read_csv('steam_games_organizados.csv')

# Funcion1 que entrega el año de lanzamiento con más horas jugadas segun el genero 

@router.get('/PlayTimeGenre/{genre}')
def PlayTimeGenre(genre: str) -> dict:
    genre = genre.capitalize()
    genre_df = df[df[genre] == 1]
    year_playtime_df = genre_df.groupby('release_date')['playtime_forever'].sum().reset_index()
    max_playtime_year = year_playtime_df.loc[year_playtime_df['playtime_forever'].idxmax(), 'release_date']
    return {"Género": genre, "Año de lanzamiento con más horas jugadas para Género :": int(max_playtime_year)}


# Función2 que entrega el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año

@router.get('/UserForGenre/{genre}')
def UserForGenre(genre: str) -> dict:
    genre = genre.capitalize()
    genre_df = df[df[genre] == 1]
    max_playtime_user = genre_df.loc[genre_df['playtime_forever'].idxmax(), 'user_id']
    year_playtime_df = genre_df.groupby('release_date')['playtime_forever'].sum().reset_index()
    playtime_list = year_playtime_df.to_dict(orient='records')
    result = {
        "Usuario con más horas jugadas para Género " + genre: max_playtime_user,
        "Horas jugadas": playtime_list}
    return result


#Función3 que entrega el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)

@router.get('/UsersRecommend/{year}')
def UsersRecommend(year: int) -> dict:
    df_filtrado = df[(df['release_date'] == year) & (df['recommend'] == True) & (df['sentiment_score'] >= 1)]
    if df_filtrado.empty:
        return {"error": 'Valor no encontrado'}
    df_ordenado = df_filtrado.sort_values(by='sentiment_score', ascending=False)
    top_3_reseñas = df_ordenado.head(3)
    resultado = {
        "Puesto 1": top_3_reseñas.iloc[0]['app_name'],
        "Puesto 2": top_3_reseñas.iloc[1]['app_name'],
        "Puesto 3": top_3_reseñas.iloc[2]['app_name']
    }
    return resultado


"""
--> FUNCIÓN4 que entrega el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.
    (reviews.recommend = False y comentarios negativos)
--> Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
"""

@router.get('/UsersWorstDeveloper/{year}')
def UsersRecommend(year: int) -> dict:
    df_filtrado = df[(df['release_date'] == year) & (df['recommend'] == False) & (df['sentiment_score'] == 0 )]
    if df_filtrado.empty:
        return {"error": 'Valor no encontrado'}
    df_ordenado = df_filtrado.sort_values(by='sentiment_score', ascending=False)
    top_3_reseñas = df_ordenado.head(3)
    resultado = {
        "Puesto 1": top_3_reseñas.iloc[0]['developer'],
        "Puesto 2": top_3_reseñas.iloc[1]['developer'],
        "Puesto 3": top_3_reseñas.iloc[2]['developer']
    }
    return resultado


"""
--> FUNCIÓN5: Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total 
    de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor. 

--> Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}
"""

@router.get('/sentiment_analysis/{developer}')
def sentiment_analysis(developer : str) -> dict:
    filtered_df = df[df['developer'] == developer]
    sentiment_counts = filtered_df['sentiment_score'].value_counts()
    result = {
        "Developer": developer,
        " Positive": int(sentiment_counts.get(2, 0)),
        " Neutral": int(sentiment_counts.get(1, 0)),
        " Negative": int(sentiment_counts.get(0, 0))
    }
    return result


"""
--> FUNCIÓN6: 

"""

muestra = df_games
tfidf = TfidfVectorizer(stop_words='english')
muestra=muestra.fillna("")
tdfid_matrix = tfidf.fit_transform(muestra['app_name'])
cosine_similarity = linear_kernel( tdfid_matrix, tdfid_matrix)




#muestra = df.head(6000)
#tfidf = TfidfVectorizer(stop_words='english')

#muestra=muestra.fillna("")

#tdfid_matrix = tfidf.fit_transform(muestra['review'])
#cosine_similarity = linear_kernel( tdfid_matrix, tdfid_matrix)
 
@router.get('/recomendacion_id/{id_producto}')
def recomendacion(id_producto: int):
    if id_producto not in muestra['id'].values:
        return {'mensaje': 'No existe el id del producto.'}
    else:  
        #generos = muestra.columns[2:17] 
        filtered_df = muestra[muestra['id'] != id_producto]
    
        tdfid_matrix_filtered = tfidf.transform(filtered_df['app_name'])
        cosine_similarity_filtered = linear_kernel(tdfid_matrix_filtered, tdfid_matrix_filtered)


        # Now you can proceed with your subsequent code
        idx = muestra[muestra['id'] == id_producto].index[0]
        sim_cosine = list(enumerate(cosine_similarity_filtered[idx]))
        sim_scores = sorted(sim_cosine, key=lambda x: x[1], reverse=True)
        sim_ind = [i for i, _ in sim_scores[1:6]]
        sim_juegos = filtered_df['app_name'].iloc[sim_ind].values.tolist()

    return {'juegos recomendados': list(sim_juegos)}

"""    
        filtered_df = muestra[(muestra[generos] == 1).any(axis=1) & (muestra['steam_id'] != id_producto)]
        tdfid_matrix_filtered = tfidf.transform(filtered_df['review'])
        cosine_similarity_filtered = linear_kernel(tdfid_matrix_filtered, tdfid_matrix_filtered)
        idx = muestra[muestra['steam_id'] == id_producto].index[0]
        sim_cosine = list(enumerate(cosine_similarity_filtered[idx]))
        sim_scores = sorted(sim_cosine, key=lambda x: x[1], reverse=True)
        sim_ind = [i for i, _ in sim_scores[1:6]]
        sim_juegos = filtered_df['app_name'].iloc[sim_ind].values.tolist()
"""    
    

"""
#def recomendacion(id_producto: int):
id_producto = 293960
if id_producto not in muestra['id'].values:
    print('mensaje: No existe el id del usuario.')
else:  
    ##generos = muestra.columns[2:17] 
        

    #filtered_df = muestra[(muestra[generos] == 1).any(axis=1) & (muestra['id'] != id_producto)]
    
    
#return {'juegos recomendados': list(sim_juegos)}
"""