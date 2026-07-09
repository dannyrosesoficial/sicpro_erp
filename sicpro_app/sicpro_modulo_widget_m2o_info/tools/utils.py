def sicpro_many2one_info_data(record, field_names):

    record.ensure_one()
    res = []
    for field_name in field_names:
        res += [{
            'value': record[field_name],
            'string': record._fields[field_name].get_description(
                record.env)['string'],
            'name': field_name,
        }]
    return res
