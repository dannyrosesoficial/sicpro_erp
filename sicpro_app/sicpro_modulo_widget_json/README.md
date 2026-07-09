
Uso
=====


      Python
      
      ```
      from odoo import fields, models
      
      class SomeModel(models.Model):
          _name = 'some.model'
      
          json_data = fields.Json(string="JSON Data")
      ```
      
      XML view
      ```
      <field name="json_data" widget="json_widget"/>
      ```
