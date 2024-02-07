from fastapi import APIRouter
import pandas as pd
from sklearn.metrics.pairwise        import cosine_similarity
from sklearn.metrics.pairwise        import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


router = APIRouter()

# Funcion1 que entrega el año de lanzamiento con más horas jugadas segun el genero 

@router.get('/PlayTimeGenre/{genre}')
def PlayTimeGenre(genre: str) -> dict:

    # Convertir el género, primera mayúscula
    genre = genre.capitalize()
    
    df_games2 = pd.read_csv('dataset_finales/steam_games_cunsulta.csv')
    df_items = pd.read_csv('dataset_finales/australian_users_items_organizados.csv')

    
    merged_df = pd.merge(df_games2, df_items, on='id')
    # Filtrar el DataFrame por el género especificado
    genre_df = merged_df[merged_df[genre] == 1]
    
    # Agrupar por 'release_date' y calcular la suma total de 'playtime_forever'
    year_playtime_df = genre_df.groupby('release_date')['playtime_forever'].sum().reset_index()
    
    # Encontrar el año con la mayor cantidad de horas jugadas
    max_playtime_year = year_playtime_df.loc[year_playtime_df['playtime_forever'].idxmax(), 'release_date']
    
    return {"Género": genre, "Año de lanzamiento con más horas jugadas para Género :": int(max_playtime_year)}#max_playtime_year
    


# Función2 que entrega el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación
# de horas jugadas por año

@router.get('/UserForGenre/{genre}')
def UserForGenre(genre: str) -> dict:

    # Convertir el género, primera mayúscula
    genre = genre.capitalize()
    
    df_games2 = pd.read_csv('dataset_finales/steam_games_cunsulta.csv')
    df_items = pd.read_csv('dataset_finales/australian_users_items_organizados.csv')
        
    merged_df = pd.merge(df_games2, df_items, on='id')
    merged_df['playtime_hours'] = merged_df['playtime_forever'] / 60

    # Filtrar el DataFrame por el género especificado
    genre_df = merged_df[merged_df[genre] == 1]
    
    # Agrupar por 'release_date' y calcular la acumulación de horas jugadas por año
    year_playtime = genre_df.groupby('release_date')['playtime_hours'].sum().reset_index()
    
    # Encontrar al usuario con más horas jugadas en el género especificado
    user_most_playtime = genre_df.loc[genre_df['playtime_hours'].idxmax(), 'user_id']
    
    # Crear la lista de horas jugadas por año
    playtime_list = year_playtime.values.tolist()
    
    # Construir el resultado
    resultado = {
        "Usuario con más horas jugadas para Género " + genre: user_most_playtime,
        "Horas jugadas": playtime_list
    }
    return resultado


#Función3 que entrega el top 3 de juegos más recomendados por usuarios para el año dado.
# (reviews.recommend = True y comentarios positivos/neutrales)

@router.get('/UsersRecommend/{year}')
def UsersRecommend(year: int) -> dict:

    df_games = pd.read_csv('dataset_finales/steam_games_cunsulta.csv')
    df_reviews = pd.read_csv('dataset_finales/user_reviews_consulta.csv')
    
    # Filtrar los juegos para el año dado
    df_games_year = df_games[df_games['release_date'] == year]

    # Fusionar los DataFrames en función del 'item_id'
    merged_df = pd.merge(df_reviews, df_games_year, left_on='item_id', right_on='id')

    # Filtrar para obtener las recomendaciones válidas
    valid_recommendations = merged_df[(merged_df['recommend'] == True) & 
                                      (merged_df['sentiment_score'] == 2)]

    # Ordenar por 'sentiment_score' en orden descendente
    sorted_df = valid_recommendations.sort_values(by='sentiment_score', ascending=False)

    # Seleccionar los tres primeros juegos
    top_3_games = sorted_df.head(3)

    # Crear el resultado con los nombres de los juegos en los tres primeros puestos
    resultado = {
        "Puesto 1": top_3_games.iloc[0]['app_name'],
        "Puesto 2": top_3_games.iloc[1]['app_name'],
        "Puesto 3": top_3_games.iloc[2]['app_name']
    }

    return resultado


#--> FUNCIÓN4 que entrega el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.
#    (reviews.recommend = False y comentarios negativos)
#--> Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

@router.get('/UsersWorstDeveloper/{year}')
def UsersRecommend(year: int) -> dict:
    
    df_games = pd.read_csv('dataset_finales/steam_games_cunsulta.csv')
    df_reviews = pd.read_csv('dataset_finales/user_reviews_consulta.csv')

    # Filtrar los juegos para el año dado
    df_games_year = df_games[df_games['release_date'] == year]

    # Fusionar los DataFrames en función del 'id'
    merged_df = pd.merge(df_reviews, df_games_year, left_on='item_id', right_on='id')

    # Filtrar para obtener las recomendaciones válidas
    valid_recommendations = merged_df[(merged_df['recommend'] == False) & 
                                      (merged_df['sentiment_score'] == 0)]

    # Contar las recomendaciones por desarrollador
    developer_recommendations = valid_recommendations['developer'].value_counts().reset_index()
    developer_recommendations.columns = ['developer', 'recommendation_count']

    # Ordenar por recomendaciones en orden ascendente
    sorted_df = developer_recommendations.sort_values(by='recommendation_count', ascending=True)

    # Seleccionar los tres desarrolladores con menos recomendaciones
    top_3_developers = sorted_df.head(3)

    # Crear el resultado con los nombres de los desarrolladores en los tres primeros puestos
    resultado = {
        "Desarrolladores menos recomendados en el año : ": year,
        "Puesto 1": top_3_developers.iloc[0]['developer'],
        "Puesto 2": top_3_developers.iloc[1]['developer'],
        "Puesto 3": top_3_developers.iloc[2]['developer']
    }

    return resultado


#--> FUNCIÓN5: Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total 
#    de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor. 
#--> Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}

@router.get('/sentiment_analysis/{developer}')
def sentiment_analysis(developer : str) -> dict:
    
    df_games = pd.read_csv('dataset_finales/steam_games_cunsulta.csv')
    df_reviews = pd.read_csv('dataset_finales/user_reviews_consulta.csv')

    # Filtrar por el desarrollador específico
    df_developer = df_games[df_games['developer'] == developer]
    
    # Fusionar los DataFrames en función del 'id'
    merged_df = pd.merge(df_reviews, df_developer, left_on='item_id', right_on='id')
    
    # Contar las ocurrencias de cada análisis de sentimiento
    sentiment_counts = merged_df['sentiment_score'].value_counts()

    # Crear el diccionario con los resultados
    result = {
        "Desarrollador": developer,
        "Positive": int(sentiment_counts.get(2, 0)),
        "Neutral": int(sentiment_counts.get(1, 0)),
        "Negative": int(sentiment_counts.get(0, 0))
    }
    return result


# --> FUNCIÓN 6
#sistema de recomendación con relación ítem-ítem, esto es se toma un item, en base a que tan similar es ese ítem
# respecto al resto, se recomiendan similares. Aquí el input es un juego y el output es una lista de juegos
# recomendados. Se usa *similitud del coseno*. 
 
@router.get('/recomendacion_id/{id_producto}')
def recomendacion(id_producto: int):    

    muestra = pd.read_csv('dataset_finales/steam_games_cunsulta.csv')
    
    tfidf = TfidfVectorizer(stop_words='english')
    muestra=muestra.fillna("")
    tdfid_matrix = tfidf.fit_transform(muestra['app_name'])
    cosine_similarity = linear_kernel( tdfid_matrix, tdfid_matrix)

    if id_producto not in muestra['id'].values:
        return {'mensaje': 'No existe el id del producto.'}
    else:  
         
        filtered_df = muestra[muestra['id'] != id_producto]
    
        tdfid_matrix_filtered = tfidf.transform(filtered_df['app_name'])
        cosine_similarity_filtered = linear_kernel(tdfid_matrix_filtered, tdfid_matrix_filtered)

        idx = muestra[muestra['id'] == id_producto].index[0]
        sim_cosine = list(enumerate(cosine_similarity_filtered[idx]))
        sim_scores = sorted(sim_cosine, key=lambda x: x[1], reverse=True)
        sim_ind = [i for i, _ in sim_scores[1:6]]
        sim_juegos = filtered_df['app_name'].iloc[sim_ind].values.tolist()

    return {'juegos recomendados': list(sim_juegos)}
