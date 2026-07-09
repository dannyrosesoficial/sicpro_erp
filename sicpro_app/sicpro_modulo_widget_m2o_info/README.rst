
USO
'''''
.. modo:: 1

    .. codigo:: xml

       <field name="widget_partner_id"
              placeholder="Partner..."
              widget="m2o_info"
              options="{
                  'info_fields': [
                      'name', 'commercial_company_name', 'website',
                      'email', 'phone', 'mobile']}"/>


.. modo:: 2

    .. codigo:: python

        class ResPartner(models.Model):
            _inherit = 'res.partner'

            def helper_many2one_info(self):
                self.ensure_one()
                res = []
                read_fields = [
                    'name', 'commercial_company_name', 'website',
                    'email', 'phone', 'mobile'
                ]
                for field_name in read_fields:
                    res += [{
                        'value': self[field_name],
                        'string': self._fields[field_name].get_description(
                            self.env)['string'],
                        'name': field_name,
                    }]
                return res

    .. codigo:: xml

        <field name="widget_partner_id"
              placeholder="Partner..."
              widget="m2o_info"
              options="{'info_method': 'helper_many2one_info'}"/>


.. modo:: 3

    .. code:: python

        from odoo.addons.sicpro_modulo_widget_m2o_info import helper_get_many2one_info_data

        class ResPartner(models.Model):
            _inherit = 'res.partner'

            def helper_many2one_info(self):
                return helper_get_many2one_info_data(self, [
                    'name', 'commercial_company_name', 'website',
                    'email', 'phone', 'mobile'
                ])