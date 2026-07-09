Realizar consultas directas al ldap empresarial

.. code:: PYTHON

        import sicpro_modulo_ldap_query
        filtro_nombre = 'uid'
        filtro_valor = 'daniel.borrero'
        data = sicpro_modulo_ldap_query.models.sicpro_modulo_ladap_query.check_ldap_usuario(self, filtro_nombre, filtro_valor)

        for item in data:
            print(item)
        print(len(data))

Para obtener los valores limpios:: PYTHON

    valor = tools.ustr(data[0][1]['accountStatus'][0])
    print(valor)