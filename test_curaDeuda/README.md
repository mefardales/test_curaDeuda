## Descripción:

### El API presenta los siguientes endpoind:
### Vistas POST
##### /auth    -- para el login
##### parametros:
###### username: usuario
###### password: contraseña

#### /reg_up_user  –registro y actualización de los usuarios ‘solo administradores’
##### parámetros:
###### username: usuario
###### password: contraseña
###### is_superuser: administrador (si o no)
###### is_advicer: role avanzado del programa pero no es administrador
###### is_active: activación del usuario, por defecto es siempre activo

##### /deluser  –eliminar usuarios ‘solo administradores’
##### parámetros:
###### username: usuario
##### -- el primer registro y el primer login serán registrados automáticamente en la base de datos, es crucial que sea hecho en el orden de login-registro para que quede plasmado correctamente, se debe escribir el mismo usuario que se autentifico en el login previo. Los siguientes usuarios registrados seran creados por una cuenta administradora de lo contrario no serán creados y dicha primera cuenta debe establecerse como administrador al ser registrada si no en el próximo login solo sera un usuario común.

##### /api/importar – importar los datos desde el archivo excel
##### parametros:
###### filename: nombre del archivo a buscar dentro de la carpeta “dir_file”
###### cant_pag: cantidad de paginas que se leerán de el archivo excel, por defecto son “33”
##### --una mas que la cantidad real a leer y comienza a leer en la pagina 1 no en la 0 porque esta esta con la presentación

### Vistas GET
##### /estado  -- leer los datos de los estados de la base de datos
##### parámetros:
###### est: nombre del estado a buscar
###### limit: limite de la cantidad de resultados, por defecto es el máximo

##### /municipios – leer los datos de los municipios de la base de datos
##### parámetros:

###### mun: nombre del municipio a buscar
###### cpm: codigo postal del municipo a buscar
###### limit: limite de la cantidad de resultados, por defecto es el máximo
##### -- se puede combinar las búsquedas para mejor filtrado de los datos

##### /colonias – leer los datos de las colonias en la base de datos
##### parámetros:
###### cpp: codigo postal de las colonias a buscar
###### name_col: nombre de las colonias a buscar
###### mun: nombre del municipio a buscar
###### cpm: codigo postal del municipo a buscar
###### colon: filtro para buscar solo las colonias o el Fraccionamiento en el campo tipo_col
###### limit: limite de la cantidad de resultados, por defecto es el máximo


#### Variables de entorno:
###### DB_SQLITE: activa la base de datos sqlite para trabajar con ella, por defecto esta activa
###### DB_POSTGRESQL: activa la base de datos postgresql para trabajar con ella, por defecto esta desactivda, se activa se deja de utilizar la base de datos sqlite
##### valor 0 desactivada y 1 activada
###### Datos de la coneccion a la base de datos posgresql
###### DB_HOST: host del servidor, por defecto “localhost”
###### DB_USER: usuario de acceso, por defecto “root”
###### DB_PASSWD: contraseña de acceso, por defecto “passwd”
###### DB_PORT: puerto de acceso, por defecto “5432”
###### DB_DB: base de datos a conectar, por defecto “api”

##### Servidor:
###### HOST: ip o dominio donde correrá el servidor, por defecto “0.0.0.0”
###### PORT: puerto de trabajo del api, por defecto “8000”
###### DEBUG: modo debug o producción, por defecto “debug”
##### valor 0 debug, 1 producción


##### Notas:
###### La importación del archivo excel es relativamente lenta por la cantidad de paginas a leer y de datos a importar hacia las tablas.
###### Se fragmento una fila real del archivo excel en tres subgrupos, “estados”, “municipios” y “colonias” así a la hora de proyectar cada fila se leen los tres fragmentos y se mezclan para crear la fila original.


