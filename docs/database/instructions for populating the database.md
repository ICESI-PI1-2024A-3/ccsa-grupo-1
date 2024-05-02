## Instrucciones para crear y poblar la base de datos utilizando las funcionalidades proporcionadas por Django y la clase `populate_db.py`

1. Ejecuta el comando que proporciona Django para crear la base de datos utilizando los archivos de migraciones
   existentes. Para hacer esto, abre la carpeta del proyecto en tu explorador de archivos y luego abre una terminal
   desde allí (o abre
   una terminal y navega hasta la carpeta del proyecto). Luego, ejecuta el siguiente comando:

```shell
python manage.py migrate
```

2. Una vez creada la base de datos, se deben asignar los permisos que tendrán los usuarios en el sistema dependiendo de
   su rol. Estos permisos están definidos en el archivo `permissions.json`. Para cargarlos en la base de datos, ejecuta
   el siguiente comando:

```shell
python manage.py loaddata permissions.json
```

Después de ejecutar este comando, podrás utilizar el sistema con el único usuario registrado hasta el momento (el
usuario `admin`). Sin embargo, la base de datos estará prácticamente vacía. Por este motivo, lo óptimo sería poblar la
base de datos primero. Puedes hacerlo siguiendo los siguientes pasos:

### Población de la base de datos

1. **Instalación de dependencias:** En una terminal con las mismas características que la anterior, introduce el
   siguiente comando para instalar la biblioteca utilizada en la simulación de datos:

> [!IMPORTANT]
> Esta acción solo debe realizarse si es la primera vez que va a utilizar la biblioteca `factory-boy` en este proyecto.

```shell
pip install factory-boy
```

2. Ahora, para abrir una consola de Python ejecuta el siguiente comando:

```shell
python manage.py shell
```

3. Importa todas las "fábricas" desde la clase de fábrica (llamada en nuestro proyecto `populate_db`) con el siguiente
   comando:

``` Python
from AcademicProgrammingApplication.populate_db import SemesterFactory, SubjectFactory, ProgramFactory, TeacherFactory, ClassFactory, ContractFactory, ViaticFactory, StudentFactory
```

4. Crea las instancias con sus respectivas fábricas según sea necesario. Por ejemplo, para poblar la base de datos con
   10 profesores:

``` Python
TeacherFactory.create_batch(10)
```

Este comando generará 10 instancias de profesores en la base de datos.

Los valores recomendados para poblar la base de datos son los siguientes:

``` Python
SemesterFactory.create_batch(9)
SubjectFactory.create_batch(20)
ProgramFactory.create_batch(8)
TeacherFactory.create_batch(20)
ClassFactory.create_batch(200)
StudentFactory.create_batch(50)
ContractFactory.create_batch(10)
ViaticFactory.create_batch(10)
```

> **¿Cómo ingresar al sistema por primera vez?**  
> Como se mencionó anteriormente, hay un único usuario para acceder al sistema: `admin`. La contraseña para ingresar con
> este usuario es `admin`. Una vez dentro del sistema, podrás crear más usuarios y asignarles sus respectivos roles
> desde la pantalla de gestión de roles. Una vez hecho esto, podrá usar estos usuarios para acceder posteriormente al
> sistema desde la vista de inicio de sesión.

**Recomendaciones adicionales:**

- Los periodos académicos se programaron para ser generados desde el 2020-1, por lo que máximo es posible crear hasta 9
  periodos académicos.
- Es recomendable crear máximo 8 programas de posgrado para que los nombres no se repitan y se mantenga la integridad de
  los datos.