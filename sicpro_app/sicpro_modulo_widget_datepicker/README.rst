Uso
=====
PYTHON

    multi_fechas = fields.Char(string="Multiples Fechas")

XML
    ...
    <field name="arch" type="xml">
        <form string="View name">
            ...
            <field name="multi_fechas" widget="multiple_datepicker"/>
            ...
        </form>
    </field>
    ...
