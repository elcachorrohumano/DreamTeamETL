# DreamTeamETL

## Primer paso

1. Construir y levantar los servicios:

    ```sh
    docker-compose up -d --build
    ```

2. Ejecutar `app.py` dentro del contenedor `app`:

    ```sh
    docker-compose exec app python app.py
    ```
3. Ejecutar `top.py` dentro del contenedor `app`:

    ```sh
    docker-compose exec app python top.py
    ```
    
4. Ejecutar `import.py` dentro del contenedor `app`:

    ```sh
    docker-compose exec app python import.py
    ```

---
#### Playlist
Si queren usar su playlist cambien el playlist_id. en el app.py linea 76. Si la quieren comparar con otra que no sea el top 50 cambien el playlist_id de top.py.
Su playlist_id es un número así 37i9dQZEVXbMDoHDwVN2tF sacado del link de su playlist, https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF. Si tiene más números el es el número hasta el sigo ?.
### Descripción

DreamTeamETL es un proyecto de extracción, transformación y carga (ETL) que transfiere datos de una base de datos MongoDB a una base de datos Neo4j. Sigue los pasos anteriores para construir y ejecutar los servicios Docker necesarios para el proyecto.

#### Requisitos

- Docker
- Docker Compose

#### Estructura del Proyecto

