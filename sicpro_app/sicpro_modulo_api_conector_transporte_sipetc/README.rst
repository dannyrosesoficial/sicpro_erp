<?xml version="1.0" encoding="utf-8"?>
<!--
##############################################################################
PROYECTO: SICPRO ERP
AUTOR: Daniel Barrero Reyes (Danny Rose's)
CONTACTO: daniel.borrero@etecsa.cu
Copyright (C) 2020-2026 SICPRO ERP.
Todos los derechos reservados.
##############################################################################
-->
<odoo>
    <data noupdate="0">
        <record model="sicpro.app.transporte.api" id="transporte_api_1">
            <field name="name">SipeTC</field>
            <field name="web">https://sipetc.etecsa.cu/login</field>
            <field name="url_login">https://sipetc.etecsa.cu/rest/api/login</field>
            <field name="url_data">https://sipetc.etecsa.cu/rest/api/equipos/unidad/dvpe</field>
            <field name="url_cierre">https://sipetc.etecsa.cu/rest/api/logout</field>
            <field name="descripcion"> Sistema de Información de los Portadores Energéticos, Transporte y Equipos Consumidores de Combustible </field>
        </record>
    </data>


</odoo>