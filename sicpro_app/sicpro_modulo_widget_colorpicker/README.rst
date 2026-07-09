

Uso
=====

You need to declare a char.

    colorpicker = fields.Char(
        string="Color Picker",
    )


In the view declaration,

    ...
    <field name="arch" type="xml">
        <form string="View name">
            ...
            <field name="colorpicker" widget="colorpicker"/>
            ...
        </form>
    </field>
    ...


