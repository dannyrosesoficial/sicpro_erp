
Documentación URIs
------------------
============================================== ==============================================
URI                                            Descripción
============================================== ==============================================
`/<api-docs>/v<api_version>`                   API Documentation (generate with swagger)
`/<api-docs>/v<api_version>/swagger.json`      Json Swagger
============================================== ==============================================


API URIs
--------
============================================== ======= ===============================================================
URI                                            Método  Descripción
============================================== ======= ===============================================================
`/<api>/v<api_version>/<api_name>`             GET     Read all (with optional domain, fields, offset, limit, order)
`/api/v<api_version>/<api_name>/<id>`          GET     Read one (with optional fields)
`/api/v<api_version>/<api_name>`               POST    Create a record
`/api/v<api_version>/<api_name>/<id>`          PUT     Update a record
`/api/v<api_version>/<api_name>/<id>`          DELETE  Delete a record
`/api/v<api_version>/<api_name>/custom`        PUT     Call method (with optional parameters)
`/api/v<api_version>/<api_name>/custom/<id>`   PUT     Call method on record (with optional parameters)
============================================== ======= ===============================================================

Respuesta de Error
--------------

    {
        'code': <code>  # Código de error,
        'error': <error>  # Nombre del error,
        'description': <description>  # Descripción del error,
    }


USO
------------------
Modificar el odoo.config y agregar:
;dbfilter = ^sicpro$


     PYTHON:


        usuario = 'user'
        password = 'pass'
        base_datos = 'sicpro'
        url_login = 'https://192.168.56.10/web/session/authenticate'
        url_cierre = 'https://192.168.56.10/web/session/logout'


        if usuario and password:
            # Busco el api-key para poder conectar con la api
            headers = {"Content-Type": "application/json", }
            data = {"jsonrpc": "2.0", "method": "call", "id": 0,
                    "params": {"db": base_datos, "login": usuario,
                               "password": password, "context": {}, }, }

            response = requests.post(url_login, data=json.dumps(data),
                                     headers=headers, verify=False)
            data_key = response.json()

            if response.status_code == 200:
                x_api_key = data_key['result']['api_rest_key']
                print(x_api_key)

                # Busco los datos de la api
                url_data = 'https://192.168.56.10/api/vv1/Trabajadores'
                headers = {'accept': 'application/json', 'x-api-key': x_api_key,}
                params = (('limit', '100'),)
                response = requests.get(url_data, headers=headers,
                                        params=params, verify=False)

                data_json = response.json()
                print(data_json)

                # cierro sesión
                response = requests.get(url_cierre, verify=False)
                print(response.content)


    PHP: