from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('artists', views.artists, name='artists'),
    path('artists/<str:artist_id>', views.artist, name='artist'),
]

'''
    ---------------------- POST -------------------------------
    POST/artists: crea un artista y retorna el artista creado 
    POST/artists/<artist_id>/albums: crea un álbum delartista <artist_id> y retorna elálbum creado.
    POST/albums/<album_id>/tracks: crea una canción delálbum <album_id> yretorna la canción creada.Obtener:
    
    ---------------------- GET -------------------------------
    GET/artists: retorna todos los artistas.
    GET/albums: retorna todos los álbums.
    GET/tracks: retorna todas las canciones.
    GET/artists/<artist_id>: retorna el artista <artist_id>.
    GET/artists/<artist_id>/albums: retorna todos losalbums del artista <artist_id>.
    GET/artists/<artist_id>/tracks: retorna todas lascanciones del artista <artist_id>.
    GET/albums/<album_id>: retorna el álbum <album_id>.
    GET/albums/<album_id>/tracks: retorna todas las cancionesdel álbum<album_id>.
    GET/tracks/<track_id>: retorna la canción <track_id>.Reproducir:

    ---------------------- PUT -------------------------------
    PUT/artists/<artist_id>/albums/play: reproduce todaslas canciones de todos losálbums del artista <artist_id>.
    PUT/albums/<album_id>/tracks/play: reproduce todaslas canciones del álbum<album_id>.
    PUT/tracks/<track_id>/play: reproduce la canción<track_id>.

    ---------------------- DELETE ------------------------------- Eliminar (CASCADE)
    DELETE/artists/<artist_id>: elimina el artista <artist_id>y todos sus álbums.
    DELETE/albums/<album_id>: elimina el álbum <album_id>y todas sus canciones.
    DELETE/tracks/<track_id>: elimina la canción <track_id>.

'''