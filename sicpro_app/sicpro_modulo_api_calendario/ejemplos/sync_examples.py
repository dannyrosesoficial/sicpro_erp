# Algunos ejemplos de pseudocódigo ("pseudo", lo que significa que en realidad
# no he verificado que el siguiente código funcione, pero existe un código
# similar en el archivo teststest_caldav.py. Plantee un problema de github o
# comuníquese por correo electrónico o escriba una solicitud de extracción o
# envíe un parche si hay errores en este código) ...

# CASO DE USO 1: tendremos
# una copia local de todos los contenidos del calendario en un proceso de python
# en ejecución, y luego nos gustaría sincronizar los contenidos locales.
# (En caso de reinicio, todo el contenido se descargará nuevamente).

my_events = my_calendar.objects(load_objects=True)
# (... algún tiempo después ...)
my_events.sync()
for event in my_events:
    print(event.icalendar.subcomponents[0]["SUMMARY"])

# CASO DE USO 2, enfoque 1: Queremos cargar todos los objetos del servidor
# caldav remoto e insertarlos en una base de datos. Más tarde, debemos realizar
# una sincronización unidireccional desde el servidor caldav remoto a la
# base de datos.
my_events = my_calendar.objects(load_objects=True)
for event in my_events:
    save_event_to_database(event)
save_sync_token_to_database(my_events.sync_token)

# (... some time later ...)

sync_token = load_sync_token_from_database()
my_updated_events = my_calendar.objects_by_sync_token(sync_token, load_objects=True)
for event in my_updated_events:
    if event.data is None:
        delete_event_from_database(event)
    else:
        update_event_in_database(event)

# CASO DE USO 2, enfoque 2, usando my_events.sync().
# Ref https:github.compython-caldavcaldavissues122, esto puede ser
# significativamente más rápido si el servidor caldav tiende a descartar
# tokens de sincronización o si el servidor caldav remoto admite etags
# pero no tokens de sincronización.
my_events = my_calendar.objects(load_objects=True)
for event in my_events:
    save_event_to_database(event)
save_sync_token_to_database(my_events.sync_token)

# (... some time later ...)

updated, deleted = my_events.sync()
for event in updated:
    update_event_in_database(event)
for event in deleted:
    delete_event_in_database(event)

# ... pero el enfoque anterior se vuelve un poco complicado cuando se reinicia
# el servidor. Eventualmente, es posible guardar los etags en la base de datos.
# Siéntase libre de plantear un problema de github o contácteme en privado si
# necesita más ayuda.

## Tobias Brox, 2020-12-28
