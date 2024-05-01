## Instrucciones para poblar la base de datos utilizando la clase `populate_db.py`

**IMPORTANTE:** El paso 1 solo debe realizarse si es la primera vez que va a utilizar la biblioteca `factory-boy` en el
proyecto.

1. Abre la carpeta del proyecto en tu explorador de archivos y luego abre una terminal. En esa terminal, introduce el
   siguiente comando para instalar la biblioteca utilizada en la simulación de datos:

``` Shell
pip install factory-boy
```

2. Abre una consola e ingresa el siguiente comando:

``` Shell
python manage.py shell
```

3. Importa todas las fábricas desde la clase de fábrica con el siguiente comando:

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

**Recomendaciones adicionales:**

- Los periodos académicos se programaron para ser generados desde el 2020-1, por lo que máximo es posible crear hasta 9
  periodos académicos.
- Es recomendable crear máximo 8 programas de posgrado para que los nombres no se repitan y se mantenga la integridad de
  los datos.