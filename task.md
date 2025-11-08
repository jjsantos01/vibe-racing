Este proyecto está basado en una muy buena práctica de John Carmack. Uno de los mejores programadores de la historia. John Carmack publicaba notas de lo que iba desarrollando desde que empezó a crear videojuegos en los 80’s. Algunas notas parecían mas como un ToDo list de lo que iba terminando, algunas explicaban como programo cosas muy complejas.
https://github.com/oliverbenns/john-carmack-plan/blob/master/archive/1996-04-16.md

Hoy tenemos que crear un decentralized dev notes.

Paso 1: Crear y deployear un blog de dev notes donde pueda agregar notas de desarrollo de lo que van creando.

El blog además de tener su vista de lista y detalle de cada nota require tener 3 endpoints:
Endpoint the metadata: En archivo JSON con metadata de donde esta la lista del file. Sus datos de contacto(nombre, cuenta de github, cuenta linkedin y otros lugares que les gustaría que se muestran en su perfil), avatar.
Endpoint de lista de notas. Array de URLs de las notas.

Endpoint con la nota, la nota tiene que ser en formato Markdown con Frontmatter.

JSON Spec del metadata https://claude.ai/share/ebdba228-0108-46f1-8955-14a0834bf21e

Cuando termines en paso 1 pública la url de tu metadata en el chat de evento para que otros desarrolladores puedan consumirlo. Ve publicando notas de lo que vayas creando durante este viberating.

Al final del viberacing tiene que tener por lo menos 5 notas publicadas en su blog. Los blogs haganlos lo más vintage hacker like posible.

Paso 2: Crear un cliente de los dev notes de todos los asistentes al Viberacing. El cliente tiene el objetivo de permitir estar al día de lo que crean los asistentes a este Viberacing de ahora en adelante.

Idealmente creamos repo de blog(o varios) y un cliente que nos permita tener DevNotes como comunidad de ahora en adelante. Tal vez hasta publicar esos DevNotes en el sitio de RbR.
