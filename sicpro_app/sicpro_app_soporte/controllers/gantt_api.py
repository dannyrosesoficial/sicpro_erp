import json
from datetime import datetime, timedelta

from odoo import http
from odoo.http import request


class GanttController(http.Controller):

    @http.route('/gantt_soporte_api', type='http', auth="user")
    def gantt_soporte_api(self, model_name, timezone_offset, domain=None, **kw):

        timezone_offset = int(timezone_offset)
        domain = json.loads(domain)
        tasks = request.env[model_name].search(domain).sorted('fecha_inicio')

        res_tasks = []
        res_links = []
        for tarea in tasks:
            fecha_inicio = tarea.fecha_inicio + timedelta(minutes=timezone_offset)
            res_tasks.append({
                'id': tarea.id,
                'text': tarea.name,
                'start_date': fecha_inicio.strftime("%d/%m/%Y %H:%M:%S"),
                'duration': tarea.duracion_tarea,
                'progress': tarea.progress / 100.0,
                'open': tarea.is_open,
            })
            for link in tarea.tareas_sucesoras_ids:
                res_links.append({
                    'id': link.id,
                    'source': link.tarea_id.id,
                    'target': link.anio_id.id,
                    'type': link.tipo_relacion
                })
        return json.dumps({
            'data': res_tasks,
            'links': res_links
        })

    @http.route('/gantt_soporte_api/tarea/<int:tarea_id>', type='http', auth="user", methods=['PUT'])
    def gantt_api_task_update(self, tarea_id, model_name, open, text, duration, progress, fecha_inicio, end_date, timezone_offset, parent, **kw):
        timezone_offset = int(timezone_offset)
        fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y %H:%M')
        fecha_inicio = fecha_inicio + timedelta(minutes=-timezone_offset)
        values = dict()
        values[request.params['map_date_start']] = fecha_inicio
        values[request.params['map_duration']] = duration
        request.env[model_name].browse([tarea_id]).write(values)
        return '{"action":"updated"}'

    @http.route('/gantt_soporte_api/link/<int:link_id>', type='http', auth="user", methods=['DELETE'])
    def gantt_api_link_delete(self, link_model, link_id, **kw):
        request.env[link_model].browse([link_id]).unlink()
        return '{"action":"updated"}'
