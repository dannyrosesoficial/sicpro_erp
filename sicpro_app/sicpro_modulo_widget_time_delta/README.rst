
Uso
=====

Declarar un integer por defecto para los segundos.

    duración = fields.integer(string="Duración", default="60")


vista Tree
    ...
    <field name="arch" type="xml">
        <tree string="View name">
            ...
            <field name="duración" widget="time_delta_list"/>
            ...
        </tree>
    </field>
    ...

Vista Form
    ...
    <field name="arch" type="xml">
        <form string="View name">
            ...
            <field name="duración" widget="time_delta"/>
            ...
        </rom>
    </field>
    ...

XML string:
            For Form View - added = widget="time_delta"
            For List View - added = widget="time_delta"

            <field name="duration" widget="time_delta" options="{'mask_humanize_string': 'h,m',  'mask_picker_field' : ''}" />

            XML field:
            <field
                    name="duration" widget="time_delta"
                    options="{'mask_humanize_field': 'duration_scale', 'mask_picker_field' : 'duration_picker'}"
                    class="oe_inline"
            />

            PYTHON
            duración = fields.Integer(string='Plan duración') store in seconds.

            duration_scale = fields.Char(string='Duration Scale', related="project_id.duration_scale", readonly=True, )
            duration_picker = fields.Selection(string='Duration Picker', related="project_id.duration_picker", readonly=True, )


            Selection
            @api.model
            def _get_duration_picker(self):
                value = [
                    ('day', _('Day')),
                    ('second', _('Second')),
                    ('day_second', _('Day Second'))
                ]
            return value
