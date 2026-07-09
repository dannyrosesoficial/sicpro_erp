Realizar consultas directas al ldap empresarial

.. Links API::

API: https://nube.etecsa.cu/index.php/apps/deck/api/v1.0

        ### Mapeos de los payload ###

        # Board
        payload_board = json.dumps(
            {"title": "Sicpro:boards",
             "color": "282BFF",
             })

        # Estados
        payload_estado = json.dumps(
            {"title": "Sicpro:boards",
             "color": "282BFF",
             })

        # Tarjetas
        payload_tarjeta = json.dumps(
            {"title": "Test",
             "description": 'descripción',
             "stackId": 'estado_id',
             "type": "plain",
             "labels": 'etiqueta_id',
             "assignedUsers": 'usuario',
             "order": 999,
             "duedate": "2019-12-24T19:29:30+00:00",
             })

        # Etiquetas
        payload_etiqueta = json.dumps(
            {"title": "Finished",
             "color": "31CC7C",
             "boardId": 10,
             })

        # Usuario
        payload_usuario = json.dumps(
            {"userId": 'daniel.borrero',
             })

        # Participantes
        payload_participante = json.dumps(
            {"type": 0,
             "participant": 'daniel.borrero',
             "permissionEdit": False,
             "permissionShare": False,
             "permissionManage": False,})