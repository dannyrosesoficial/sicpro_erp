import sys
from datetime import date
from datetime import datetime

# Intentaremos usar la biblioteca caldav local, no la instalada en el sistema
sys.path.insert(0, "..")
sys.path.insert(0, ".")

import caldav

# ¡NO nombre su archivo calendar.py o caldav.py! Hemos tenido varios problemas
# archivados, las cosas se rompen porque se importaron los archivos incorrectos.
# No es un error con la biblioteca caldav per se.
#
# CONFIGURACIÓN. Edite aquí, o configure algo en testsconf_private.py
# (vea testsconf_private.py.EXAMPLE).
caldav_url = "https://calendar.example.com/dav"
username = "somebody"
password = "hunter2"

# Al usar la biblioteca caldav, siempre se debe comenzar iniciando un objeto
# DAVClient, que debe contener detalles de conexión y credenciales. Iniciar el
# objeto no provoca ninguna solicitud al servidor, por lo que no se interrumpirá
# incluso si la URL de caldav está configurada en example.com
client = caldav.DAVClient(url=caldav_url, username=username, password=password)

# Para mayor comodidad, si las cosas están configuradas correctamente en la
# configuración de prueba, el siguiente código puede reemplazar el objeto del
# cliente con uno que funcione.
if "example.com" in caldav_url and password == "hunter2":
    from tests.conf import client as client_

    client = client_()

# Por lo general, el siguiente paso es obtener un objeto principal. Esto
# provocará la comunicación con el servidor.
my_principal = client.principal()

# Los calendarios de los directores se pueden obtener así:
calendars = my_principal.calendars()
if calendars:
    # Algunos servidores de calendario incluirán todos los calendarios a los
    # que tiene acceso en esta lista, y no solo los calendarios propiedad de
    # este principal.
    print("your principal has %i calendars:" % len(calendars))
    for c in calendars:
        print("    Name: %-20s  URL: %s" % (c.name, c.url))
else:
    print("your principal has no calendars")

# Intentemos encontrar o crear un calendario...
try:
    # Esto generará un NotFoundError si el calendario no existe
    my_new_calendar = my_principal.calendar(name="Test calendar")
    assert my_new_calendar
# existió el calendario, probablemente se hizo en una
# ejecución anterior de este script
except caldav.error.NotFoundError:
    # Vamos a crear un calendario
    my_new_calendar = my_principal.make_calendar(name="Test calendar")

# Agreguemos un evento a nuestro calendario recién creado
# (este patrón de uso es nuevo desde v0.9. Anteriormente, save_event solo
# aceptaría algunos datos ical)
my_event = my_new_calendar.save_event(
    dtstart=datetime(2020, 5, 17, 8),
    dtend=datetime(2020, 5, 18, 1),
    summary="Do the needful",
    rrule={"FREQ": "YEARLY"},
)

# Busquemos el evento recién agregado. (esto puede fallar si el
# servidor no admite la expansión)
print("Here is some icalendar data:")
try:
    events_fetched = my_new_calendar.date_search(
        start=datetime(2021, 5, 16), end=datetime(2024, 1, 1), expand=True
    )
    print(events_fetched[0].data)
except:
    print("Your calendar server does apparently not support expanded search")
    events_fetched = my_new_calendar.date_search(
        start=datetime(2020, 5, 16), end=datetime(2024, 1, 1), expand=False
    )
    print(events_fetched[0].data)

event = events_fetched[0]

# Para modificar un evento, es mejor usar el módulo vobject o icalendar.
# La biblioteca caldav siempre ha sido compatible con vobject desde el primer
# momento, pero icalendar es más popular. event.instance a partir de la
# versión 0.x producirá una instancia de vobject, pero esto puede cambiar en
# futuras versiones. Tanto event.vobject_instance como event.icalendar_instance
# funcionan desde 0.7.
event.vobject_instance.vevent.summary.value = "Norwegian national day celebratiuns"
event.icalendar_instance.subcomponents[0][
    "summary"
] = event.icalendar_instance.subcomponents[0]["summary"].replace(
    "celebratiuns", "celebrations"
)
event.save()

# Tenga en cuenta que la forma correcta de guardar nuevos datos de icalendar
# en el calendario es calendar.save_event(ics_data), mientras que la forma
# correcta de actualizar un evento de calendario es event.save().
# Hacer calendar.save_event(event.data) puede fallar.
# Consulte https:github.compython-caldavcaldavissues153 para
# obtener más información.

# Es posible acceder a objetos como calendarios sin pasar por un objeto
# Principal si se conoce la URL del calendario.
the_same_calendar = client.calendar(url=my_new_calendar.url)

# para obtener todos los eventos del calendario, también es posible usar el
# método events(). Los eventos recurrentes no se ampliarán.
all_events = the_same_calendar.events()

# También es posible usar .objetos.
all_objects = the_same_calendar.objects()

# dado que solo hemos agregado eventos (y no todos ni diarios), deberían ser
# iguales ... excepto que all_objects es un iterador y no una lista.
assert len(all_events) == len(list(all_objects))

# Comprobemos que el resumen salió bien
assert all_events[0].vobject_instance.vevent.summary.value.startswith("Norwegian")
assert all_events[0].vobject_instance.vevent.summary.value.endswith("celebrations")

# Este calendario debería admitir, como mínimo, VEVENT... lo más probable es
# que también admita VTODO y tal vez incluso VJOURNAL. Podemos consultar al
# servidor qué puede aceptar:
acceptable_component_types = my_new_calendar.get_supported_components()
assert "VEVENT" in acceptable_component_types

# Limpiar: eliminar el nuevo calendario
my_new_calendar.delete()

# Probemos con una lista de tareas. Algunos servidores no pueden combinar
# eventos y todos en el mismo calendario.
my_new_tasklist = my_principal.make_calendar(
    name="Test tasklist", supported_calendar_component_set=["VTODO"]
)

# Agregaremos una tarea a la lista de tareas
my_new_tasklist.add_todo(
    ics="RRULE:FREQ=YEARLY",
    summary="Deliver some data to the Tax authorities",
    dtstart=date(2020, 4, 1),
    due=date(2020, 5, 1),
    categories=["family", "finance"],
    status="NEEDS-ACTION",
)

# Obtener las tareas
todos = my_new_tasklist.todos()
assert len(todos) == 1
assert "FREQ=YEARLY" in todos[0].data

print("Here is some more icalendar data:")
print(todos[0].data)

# date_search también funciona en listas de tareas, pero uno tiene que ser
# explícito para obtenerlas
todos_found = my_new_tasklist.date_search(
    start=datetime(2021, 1, 1),
    end=datetime(2024, 1, 1),
    compfilter="VTODO",
    expand=True,
)
if not todos_found:
    print(
        "Apparently your calendar server does not support searching for future instances of reoccurring tasks"
    )
else:
    print("Here is even more icalendar data:")
    print(todos_found[0].data)

# Marcar la tarea como completada
todos[0].complete()

# Esta es una tarea anual. Completarlo durante un año probablemente debería
# generar una nueva instancia de recurrencia de tareas para el próximo año.
# El RFC no dice nada al respecto, parece que depende del clima de los clientes
# implementar dicha lógica o no. Implementé dicha lógica en el proyecto
# calendar-cli, tal vez debería moverse a la biblioteca caldav, pero por ahora
# ... completar la tarea hará que la lista de tareas se vacíe.
todos = my_new_tasklist.todos()
assert len(todos) == 0

# También es posible obtener tareas históricas.
todos = my_new_tasklist.todos(include_completed=True)
assert len(todos) == 1

# y es posible eliminar tareas por completo
todos[0].delete()

my_new_tasklist.delete()
