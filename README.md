# Proyecto Individual 1 - Sistema de Recomendación de Videojuegos para Steam

<p align="center">
  <img src="images/image (2).png" width="400" alt="Texto alternativo si la imagen no carga">
</p>


Steam es una plataforma multinacional de videojuegos y plantea la tarea de crear un sistema de recomendacion de videojuegos. En el proyecto desarrollo las etapas de Ingeniería de Datos con procesos como ETL y EDA y Data Analytics respondiendo endpoint o preguntas de valor para el usuario, también se hace el despliegue de la API con el marco de referencia de FastAPI. El objetivo final es que los usuarios conozcan más de  cerca de los juegos, los más recomendados, los géneros que más les puedan interesar, un análisis de sentimiento de juegos y un modelo de Machine Learnig.


# Etapas del proyecto

El sistema se construye en tres etapas:

### 1. Ingeniería de Datos y Desarrollo de API

- **ETL:** Se realizó la carga y limpieza inicial, y organización del dataset para su correcta lectura. Se implementó un análisis de sentimiento  usando la herramienta 'SentimentIntensityAnalyzercon' creando la columna 'sentiment_score', permitiendo mejorar el rendimiento de la API con FastAPI y el entrenamiento del modelo de Machine Learning.

- **API 'endpoints':** Se propuso y desarrolló una API usando FastAPI que ofrece diversas consultas a los datos disponibles, brindando información sobre géneros, desarrolladores, usuarios, géneros y juegos.


### 2. EDA y Modelos de Machine learning

- **Analisis exploratorio:** Se realizó un análisis exploratorio de los datos como nube de nombres de juegos más comunes, frecuencia en las que estas palabras aparecen, correlación entre variables claves, y otras importantes para comprender mejor las relaciones entre las variables del dataset. Todas estas relaciones y datos sirven para análisis posteriores.

- **Modelos de Recomendación:** Se implementó el sistemas de recomendación 'ítem-ítem'. Este modelo permite sugerir juegos similares basados en la similitud entre ítems o juegos.

### 3. Deployment y Documentación

- **Deployment:** La API se encuentra desplegada y disponible para ser consumida desde la web, utilizando el servicio Render y siguiendo el tutorial disponible en el repositorio.

- **Readme.md:** Se documenta el desarrollo del proyecto en sus respectivas etapas para que el usuario final pueda entender la dinámica de la solución y los entregable.

- **Video explicativo:** Se desarrolla un video explicativo sobre el proyecto, el cual queda disponible en Yuotube


## --> ETL

<p align="center">
  <img src="images/image (3).jpg" width="400" alt="Texto alternativo si la imagen no carga">
</p>

La etapa del ETL es quizás la más importante en el desarrollo del proyecto toda vez que nos asegura la entrega de datos confiables y reutilizables para las etapas de anális y de entrenaniento en Machine Learning, además aseguramos en este proceso que los datos pueden ser reutilizados en análisis posteriores. Describo a continuación lo realizado.

`steam_games_organizados.csvs`: Este dataset contiene información relativa a los juegos la cual se depuró dejando lo concerniente a 'géneros, título, fecha de lanzamiento, id y desarrollador'. En la base de datos original, se extrajeron los datos, se eliminaron las columnas sobrantes, se eliminaron filas completas con 100% de valores nulos y se dejaron solo las variables relevantes para los análisis.[ETL_tres_archivos.ipynb](ETL_tres_archivos.ipynb)

`australian_user_reviews_organizados.csv`: Este dataset contiene información de las reseñas de los juegos, con información como id del usuario y los reviews; esta última columna es una variable anidada tipo json, la cual se desanidó para extraer la información relavante por cada usario. Se limpió el dataset y se dejaron los campos relevantes para el análisis como id del usario, fecha del posted, recomendación y review. También se uso la columna review para hacer análisis de sentimientos mediante la herramienta 'SentimentIntensityAnalyzercon' que permitió conocer el nivel de recomendación de los juegos con recomendado=2, no recomendado=0 y neutro=1. [ETL_tres_archivos.ipynb](ETL_tres_archivos.ipynb)

`australian_users_items_organizados.csv`: Esta base de datos contiene información sobre los usuarios, los juegos y las horas de juego. Se extrajo información relevante para el análisis como id del usuario, tiempo de juego, id de los juegos. [ETL_tres_archivos.ipynb](ETL_tres_archivos.ipynb)

Estos tres primeros archivos se dejaron separados para análisis posteriores, pues contienen toda la información relevante para análisis posteriores.

`Dataset_final.csv`: Este conjunto de datos contiene información de los tres dataset anteriores 'steam_games, user_reviews y user_items'. Se realizó la unión de los tres datasets y se dejó un solo archivo de trabajo. [ETL_tres_archivos.ipynb](ETL_tres_archivos.ipynb)

`Dataset_final_numeros.csv`: Este conjunto de datos contiene información numérica tipo float, int para revisión en EDA de correlaciones entre variables. [ETL_tres_archivos.ipynb](ETL_tres_archivos.ipynb)


En resumen, cada archivo trabajado en el ETL quedó organizado y listo para ser usado y cargado sin inconvenientes en un Dataframe que se requiera para análisis.


## --> API 'endpoint'

<p align="center">
  <img src='images/image (1).jpg' width="400" alt="Texto alternativo si la imagen no carga">
</p>

### Deployment de la API

Se creó una API usando el módulo FastAPI con 5 funciones así:

+ PlayTimeGenre( *`genero` : str* )**:
    Devuelve `año` con mas horas jugadas para dicho género.
  
Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}
    
+ def **UserForGenre( *`genero` : str* )**:
    Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf,
			     "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

+ def **UsersRecommend( *`año` : int* )**:
   Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
  
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

+ def **UsersWorstDeveloper( *`año` : int* )**:
   Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
  
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

+ def **sentiment_analysis( *`empresa desarrolladora` : str* )**:
    Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total 
    de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor. 

Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}



`games_developer(desarrollador)` - Esta función toma como entrada una cadena de texto que representa el nombre de un desarrollador. Busca en un DataFrame que contiene información sobre juegos y filtra los datos para ese desarrollador. Luego, recorre las fechas de lanzamiento únicas y recopila información sobre cuántos juegos se lanzaron en cada año y cuántos de ellos eran gratuitos. Finalmente, devuelve un diccionario con dos claves: 'Cantidad de Items' y 'Contenido Free', cada una de las cuales contiene un diccionario con los años como claves y la cantidad de juegos o juegos gratuitos como valores.

`userdata(User_id)` - Esta función toma como entrada una cadena de texto que representa un usuario. Primero verifica si el usuario existe en un DataFrame que contiene información sobre los usuarios y sus juegos. Luego, lee un archivo CSV en bloques y busca el usuario en cada bloque. Una vez que encuentra al usuario, calcula la cantidad de dinero que ha gastado, la cantidad de juegos que tiene y el porcentaje de juegos que ha recomendado. Finalmente, devuelve un diccionario con esta información.

`best_developer_year(año)` - Esta función toma como entrada un entero que representa un año. Lee un archivo CSV que contiene información sobre los desarrolladores y la cantidad de juegos que lanzaron cada año. Filtra los datos para el año dado y luego devuelve un diccionario con la información del 'Top 1', 'Top 2' y 'Top 3' de los desarrolladores que lanzaron más juegos ese año.

`review_developer(desarrollador)` - Esta función toma como entrada una cadena de texto que representa el nombre de un desarrollador. Lee un archivo Parquet que contiene reseñas de los juegos de cada desarrollador. Filtra las reseñas para el desarrollador dado y luego devuelve un diccionario con la cantidad de reseñas positivas y negativas que ha recibido.


## Análisis exploratorio 'EDA'



## Modelos de recomendación

<p align="center">
  <img src="images/image (6).jpg" width="400" alt="Texto alternativo si la imagen no carga">

- **sistema de recomendación** Se solicita un modelo con una relación ítem-ítem, esto es se toma un item, en base a que tan similar esa ese ítem al resto, se recomiendan similares. Aquí el input es un juego y el output es una lista de juegos recomendados, para ello se usó la  *similitud del coseno*.

+ def **recomendacion_juego( *`id de producto`* )**:
    Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.


<h3><center>La forma en la que se creao y se utiliza cada funcion explicado con un enfoque tecnico, se encuentra detallada en profundidad en el directorio llamado FUNCIONES.</center></h3>




### Deployment y Documentación

Accede a la API desplegada en [https://proyecto-steamxxx.onrender.com/].

Accede al entorno virtual de la API en [https://proyecto-steamxxxx.onrender.com/docs].

Link al video : [https://youtube.com/]

## Autor

Nombre : Héctor Ocampo Gaviria

GitHub : [https://github.com/hfocampo/PI_ML_OPS_Steam]

Linkedin : [https://www.linkedin.com/in/]

 