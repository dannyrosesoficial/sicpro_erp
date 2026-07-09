
.. code:: xml

          <!--Menu Dashboard-->
        <record id="administracion_dashboard_action" model="ir.actions.client">
            <field name="name">Dashboard</field>
            <field name="tag">sicpro_dashboard_view</field>
            <field name="context">{'nombre_modelo_dashboard': 'sicpro.app.administracion'}</field>
        </record>

        <menuitem id="menu_administracion_dashboard" name="Dashboard"
              parent="menu_administracion" action="administracion_dashboard_action"
                  sequence="1"/>
