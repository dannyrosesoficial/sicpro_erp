Modo de Uso en Cualquier Otro Módulo (Ej. Transporte).
Cuando vayas a crear o modificar el módulo de transporte, la conexión será directa y limpia.
En el archivo .py de tu vehículo harás esto:

class SicproTransportVehicle(models.Model):
    _name = 'sicpro.transport.vehicle'
    # Heredamos el mixin multimedia
    _inherit = ['sicpro.transport.vehicle', 'sicpro.multimedia.mixin']

    name = fields.Char(string="Vehículo", required=True)
    marca = fields.Char(string="Marca")

Y en el XML del formulario del vehículo, agregas un botón inteligente (Smart Button) arriba a la derecha
para acceder de golpe a todas sus fotos:

<sheet>
    <div class="oe_button_box" name="button_box">
        <button name="action_view_associated_multimedia" type="object" class="oe_stat_button" icon="fa-image">
            <field string="Fotos / Medios" name="multimedia_count" widget="statinfo"/>
        </button>
    </div>
    <!-- Resto de tus campos (Nombre, Marca, etc) -->
</sheet>