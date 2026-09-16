# SICPRO ERP — Índice de Arquitectura

> Índice generado automáticamente desde el árbol local del proyecto. Este documento no modifica ningún archivo del código fuente.

## Módulos detectados: 104

## sicpro_app_actividades

**Ruta:** `sicpro_app/sicpro_app_actividades`

### Manifest

- **name:** `SICPRO: Actividades`
- **version:** `19.0.0.0.1`
- **category:** `Productividad`
- **summary:** `Esta aplicación se encargará de la gestión y productividad mediantes tareas y notas.`
- **description:** `Esta aplicación se encargará de la gestión y productividad mediantes tareas y notas.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`
- `project`
- `project_todo`

### Python

- `sicpro_app_actividades/__init__.py`
- `sicpro_app_actividades/__manifest__.py`
- `sicpro_app_actividades/hooks.py`

### XML

- `sicpro_app_actividades/views/actividades_menu_views.xml`

---

## sicpro_app_administracion

**Ruta:** `sicpro_app/sicpro_app_administracion`

### Manifest

- **name:** `SICPRO: Administración`
- **version:** `19.0.0.0.1`
- **category:** `Administración`
- **summary:** `Aplicación para la administración de SICPRO ERP`
- **description:** `Aplicación para la administración de SICPRO ERP`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `web`
- `calendar`
- `base_automation`
- `base_import`
- `auth_ldap`
- `bus`
- `sicpro_modulo_roles`

### Modelos Python

- `AdministracionAccesos`
- `AdministracionMenus`
- `Company`
- `IrHttp`
- `IrModel`
- `Partner`
- `SicproAdministracion`
- `Users`

### Python

- `sicpro_app_administracion/__init__.py`
- `sicpro_app_administracion/__manifest__.py`
- `sicpro_app_administracion/models/__init__.py`
- `sicpro_app_administracion/models/constants.py`
- `sicpro_app_administracion/models/ir_http.py`
- `sicpro_app_administracion/models/ir_model.py`
- `sicpro_app_administracion/models/res_company.py`
- `sicpro_app_administracion/models/res_partner.py`
- `sicpro_app_administracion/models/res_users.py`
- `sicpro_app_administracion/models/sicpro_app_administracion.py`
- `sicpro_app_administracion/models/sicpro_app_administracion_menus.py`

### XML

- `sicpro_app_administracion/data/ir_config_parameter.xml`
- `sicpro_app_administracion/data/ir_cron.xml`
- `sicpro_app_administracion/data/ir_mail_server.xml`
- `sicpro_app_administracion/data/mail_channel.xml`
- `sicpro_app_administracion/data/mail_template.xml`
- `sicpro_app_administracion/data/res_company.xml`
- `sicpro_app_administracion/data/res_user.xml`
- `sicpro_app_administracion/security/security.xml`
- `sicpro_app_administracion/static/src/xml/base_import.xml`
- `sicpro_app_administracion/views/administracion_menu_views.xml`
- `sicpro_app_administracion/views/administracion_menus_accesos_view.xml`
- `sicpro_app_administracion/views/ir_module_view.xml`
- `sicpro_app_administracion/views/res_company.xml`
- `sicpro_app_administracion/views/res_users_view.xml`
- `sicpro_app_administracion/views/sicpro_app_administracion.xml`
- `sicpro_app_administracion/views/webclient_templates.xml`

### JavaScript / OWL

- `sicpro_app_administracion/static/src/js/import_menu_patch.js`

### CSV / Seguridad / Datos

- `sicpro_app_administracion/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_app_administracion/static/src/css/web_administracion.scss`

---

## sicpro_app_calendario

**Ruta:** `sicpro_app/sicpro_app_calendario`

### Manifest

- **name:** `SICPRO: Calendario`
- **version:** `19.0.0.0.1`
- **category:** `Productividad`
- **summary:** `Aplicación para la gestión de calendario de SICPRO ERP`
- **description:** `Aplicación para la gestión de calendario de SICPRO ERP`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `calendar`
- `sicpro_modulo_nomencladores`
- `sicpro_app_trabajadores`
- `sicpro_app_reuniones`
- `sicpro_app_administracion`

### Modelos Python

- `Alarm`
- `AlarmManager`
- `Attendee`
- `CalendarCumplimientoReport`
- `CalendarPlanReport`
- `Meeting`
- `MeetingActividadesOrganizativas`
- `MeetingCargosExternos`
- `MeetingPieFirmas`
- `MeetingTipoCalendario`
- `Partner`
- `RecurrenceRule`

### Python

- `sicpro_app_calendario/__init__.py`
- `sicpro_app_calendario/__manifest__.py`
- `sicpro_app_calendario/models/__init__.py`
- `sicpro_app_calendario/models/calendar_actividades_organizativas.py`
- `sicpro_app_calendario/models/calendar_alarm.py`
- `sicpro_app_calendario/models/calendar_alarm_manager.py`
- `sicpro_app_calendario/models/calendar_attendee.py`
- `sicpro_app_calendario/models/calendar_cargos_externos.py`
- `sicpro_app_calendario/models/calendar_cumplimiento_reporte.py`
- `sicpro_app_calendario/models/calendar_event.py`
- `sicpro_app_calendario/models/calendar_pie_firmas.py`
- `sicpro_app_calendario/models/calendar_plan_reporte.py`
- `sicpro_app_calendario/models/calendar_recurrence.py`
- `sicpro_app_calendario/models/calendar_tareas_principales_generales.py`
- `sicpro_app_calendario/models/calendar_tipo_calendario.py`
- `sicpro_app_calendario/models/res_partner.py`

### XML

- `sicpro_app_calendario/data/ir_cron.xml`
- `sicpro_app_calendario/data/mail_template.xml`
- `sicpro_app_calendario/informes/calendar_reporte_cumplimiento_template.xml`
- `sicpro_app_calendario/informes/calendar_reporte_dvpe_template.xml`
- `sicpro_app_calendario/informes/calendar_reporte_individual_template.xml`
- `sicpro_app_calendario/views/calendar_actividades_organizativas_views.xml`
- `sicpro_app_calendario/views/calendar_cargos_externos_views.xml`
- `sicpro_app_calendario/views/calendar_menu_views.xml`
- `sicpro_app_calendario/views/calendar_pie_firma_views.xml`
- `sicpro_app_calendario/views/calendar_reporte_cumplimiento_wizard.xml`
- `sicpro_app_calendario/views/calendar_reporte_plan_wizard.xml`
- `sicpro_app_calendario/views/calendar_tareas_principales_generales_views.xml`
- `sicpro_app_calendario/views/calendar_tipo_calendario_views.xml`
- `sicpro_app_calendario/views/calendar_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_calendario/security/ir.model.access.csv`

---

## sicpro_app_clientes

**Ruta:** `sicpro_app/sicpro_app_clientes`

### Manifest

- **name:** `SICPRO: Clientes`
- **version:** `19.0.0.0.1`
- **category:** `Trabajadores`
- **summary:** `Esta aplicación le ofrece una vista rápida de su directorio de clientes, accesible desde su página de inicio.`
- **description:** `Esta aplicación le ofrece una vista rápida de su directorio de clientes, accesible desde su página de inicio.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_modulo_nomencladores`
- `mail`
- `sicpro_app_contactos`
- `sicpro_app_administracion`

### Modelos Python

- `AppClientes`
- `AppClientesEtiquetas`
- `Users`

### Python

- `sicpro_app_clientes/__init__.py`
- `sicpro_app_clientes/__manifest__.py`
- `sicpro_app_clientes/models/__init__.py`
- `sicpro_app_clientes/models/res_users.py`
- `sicpro_app_clientes/models/sicpro_app_clientes.py`
- `sicpro_app_clientes/models/sicpro_app_clientes_etiquetas.py`

### XML

- `sicpro_app_clientes/data/sicpro_app_clientes_etiquetas.xml`
- `sicpro_app_clientes/security/security.xml`
- `sicpro_app_clientes/views/clientes_etiquetas_views.xml`
- `sicpro_app_clientes/views/clientes_menu_views.xml`
- `sicpro_app_clientes/views/clientes_views.xml`
- `sicpro_app_clientes/views/res_user.xml`

### CSV / Seguridad / Datos

- `sicpro_app_clientes/security/ir.model.access.csv`

---

## sicpro_app_cmi

**Ruta:** `sicpro_app/sicpro_app_cmi`

### Manifest

- **name:** `SICPRO: Cuadro de Mando Integral`
- **version:** `19.0.0.0.1`
- **category:** `Producción`
- **summary:** `La aplicación se encarga de la gestión del CMI de la DVPE.`
- **description:** `La aplicación se encarga de la gestión del CMI de la DVPE.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `sicpro_app_administracion`
- `sicpro_modulo_nomencladores`

### Modelos Python

- `AppCMIAcciones`
- `AppCMIAccionesEstado`
- `AppCMIAccionesModoControl`
- `AppCMIIndicadores`
- `AppCMIIndicadoresCambios`
- `AppCMIIndicadoresGraficos`
- `AppCMIIndicadoresValores`
- `AppCMIObjetivosAnuales`
- `AppCMIObjetivosEstrategicos`
- `AppCMIPerspectivas`
- `AppCMIPerspectivasAnios`
- `AppCMIPerspectivasEjeEstrategico`
- `AppCMIPerspectivasPeriodos`

### Wizards / TransientModel

- `AppCMIIndicadoresModalCambios`
- `AppCMIReportes`

### Python

- `sicpro_app_cmi/__init__.py`
- `sicpro_app_cmi/__manifest__.py`
- `sicpro_app_cmi/informes/__init__.py`
- `sicpro_app_cmi/informes/sicpro_app_cmi_reporte.py`
- `sicpro_app_cmi/models/__init__.py`
- `sicpro_app_cmi/models/sicpro_app_cmi_acciones.py`
- `sicpro_app_cmi/models/sicpro_app_cmi_acciones_estado.py`
- `sicpro_app_cmi/models/sicpro_app_cmi_acciones_modo_control.py`
- `sicpro_app_cmi/models/sicpro_app_cmi_indicadores.py`
- `sicpro_app_cmi/models/sicpro_app_cmi_indicadores_cambios.py`
- `sicpro_app_cmi/models/sicpro_app_cmi_indicadores_graficos.py`
- `sicpro_app_cmi/models/sicpro_app_cmi_indicadores_valores.py`
- `sicpro_app_cmi/models/sicpro_app_cmi_objetivos_anuales.py`
- `sicpro_app_cmi/models/sicpro_app_cmi_objetivos_estrategicos.py`
- `sicpro_app_cmi/models/sicpro_app_cmi_perspectivas.py`
- `sicpro_app_cmi/models/sicpro_app_cmi_perspectivas_anio.py`
- `sicpro_app_cmi/models/sicpro_app_cmi_perspectivas_eje_estrategico.py`
- `sicpro_app_cmi/models/sicpro_app_cmi_perspectivas_periodos.py`

### XML

- `sicpro_app_cmi/data/ir_cron.xml`
- `sicpro_app_cmi/data/mail_template.xml`
- `sicpro_app_cmi/data/sicpro_app_cmi_acciones_estado.xml`
- `sicpro_app_cmi/data/sicpro_app_cmi_perspectivas_periodos.xml`
- `sicpro_app_cmi/informes/cmi_reporte_template_acciones.xml`
- `sicpro_app_cmi/informes/cmi_reporte_template_completo.xml`
- `sicpro_app_cmi/informes/cmi_reporte_template_ejes.xml`
- `sicpro_app_cmi/informes/cmi_reporte_wizard.xml`
- `sicpro_app_cmi/report/indicadores_report_views.xml`
- `sicpro_app_cmi/security/security.xml`
- `sicpro_app_cmi/views/cmi_acciones_estados_views.xml`
- `sicpro_app_cmi/views/cmi_acciones_modo_control_views.xml`
- `sicpro_app_cmi/views/cmi_indicadores_acciones_views.xml`
- `sicpro_app_cmi/views/cmi_indicadores_cambios_views.xml`
- `sicpro_app_cmi/views/cmi_indicadores_views.xml`
- `sicpro_app_cmi/views/cmi_menu_views.xml`
- `sicpro_app_cmi/views/cmi_objetivos_anuales_views.xml`
- `sicpro_app_cmi/views/cmi_objetivos_estrategicos_views.xml`
- `sicpro_app_cmi/views/cmi_perspectivas_anios_views.xml`
- `sicpro_app_cmi/views/cmi_perspectivas_eje_estrategico_views.xml`
- `sicpro_app_cmi/views/cmi_perspectivas_periodo_views.xml`
- `sicpro_app_cmi/views/cmi_perspectivas_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_cmi/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_app_cmi/static/src/css/progress_bar_color.css`
- `sicpro_app_cmi/static/src/scss/dashboard.scss`

---

## sicpro_app_contactos

**Ruta:** `sicpro_app/sicpro_app_contactos`

### Manifest

- **name:** `SICPRO: Contactos`
- **version:** `19.0.0.0.1`
- **category:** `Trabajadores`
- **summary:** `Visualización de los contactos del sistema`
- **description:** `Visualización de los contactos del sistema`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `contacts`
- `base`
- `mail`
- `sicpro_app_administracion`
- `sicpro_app_trabajadores`

### Modelos Python

- `Partner`
- `Users`

### Python

- `sicpro_app_contactos/__init__.py`
- `sicpro_app_contactos/__manifest__.py`
- `sicpro_app_contactos/models/__init__.py`
- `sicpro_app_contactos/models/res_partner.py`
- `sicpro_app_contactos/models/res_users.py`

### XML

- `sicpro_app_contactos/views/contactos_menu_views.xml`
- `sicpro_app_contactos/views/contactos_trabajadores_views.xml`
- `sicpro_app_contactos/views/contactos_views.xml`

---

## sicpro_app_control_informacion

**Ruta:** `sicpro_app/sicpro_app_control_informacion`

### Manifest

- **name:** `SICPRO: Control de la Información`
- **version:** `19.0.0.0.1`
- **category:** `Productividad`
- **summary:** `Esta aplicación se encarga del control y gestión de las informaciones que se procesan en la DVPE.`
- **description:** `Esta aplicación se encarga del control y gestión de las informaciones que se procesan en la DVPE.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `calendar`
- `sicpro_app_trabajadores`
- `sicpro_app_administracion`

### Modelos Python

- `ControlInformacion`
- `ControlInformacionActividades`
- `ControlInformacionAreas`
- `ControlInformacionControlActividades`
- `ControlInformacionDias`
- `ControlInformacionEtiquetas`
- `ControlInformacionMotivosRechazos`

### Wizards / TransientModel

- `ControlInformacionMotivoRechazo`

### Python

- `sicpro_app_control_informacion/__init__.py`
- `sicpro_app_control_informacion/__manifest__.py`
- `sicpro_app_control_informacion/models/__init__.py`
- `sicpro_app_control_informacion/models/sicpro_app_control_informacion.py`
- `sicpro_app_control_informacion/models/sicpro_app_control_informacion_actividad.py`
- `sicpro_app_control_informacion/models/sicpro_app_control_informacion_areas.py`
- `sicpro_app_control_informacion/models/sicpro_app_control_informacion_control_actividades.py`
- `sicpro_app_control_informacion/models/sicpro_app_control_informacion_dias.py`
- `sicpro_app_control_informacion/models/sicpro_app_control_informacion_etiquetas.py`
- `sicpro_app_control_informacion/models/sicpro_app_control_informacion_motivos_devolucion.py`

### XML

- `sicpro_app_control_informacion/data/ir_cron.xml`
- `sicpro_app_control_informacion/data/mail_template.xml`
- `sicpro_app_control_informacion/informes/dinamica_atividades_evaluacion_view.xml`
- `sicpro_app_control_informacion/security/security.xml`
- `sicpro_app_control_informacion/views/control_informacion_actividades_control_view.xml`
- `sicpro_app_control_informacion/views/control_informacion_actividades_views.xml`
- `sicpro_app_control_informacion/views/control_informacion_areas_views.xml`
- `sicpro_app_control_informacion/views/control_informacion_dashboard_view.xml`
- `sicpro_app_control_informacion/views/control_informacion_dias_views.xml`
- `sicpro_app_control_informacion/views/control_informacion_etiquetas_views.xml`
- `sicpro_app_control_informacion/views/control_informacion_menu_views.xml`
- `sicpro_app_control_informacion/views/control_informacion_motivo_devolucion_views.xml`
- `sicpro_app_control_informacion/views/control_informacion_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_control_informacion/security/ir.model.access.csv`

---

## sicpro_app_credenciales

**Ruta:** `sicpro_app/sicpro_app_credenciales`

### Manifest

- **name:** `SICPRO: Credenciales`
- **version:** `19.0.0.0.1`
- **category:** `Trabajadores`
- **summary:** `Esta aplicación se encargará del control de las credenciales de accesos de los trabajadores a la entidad`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_trabajadores`
- `base`
- `mail`
- `web`
- `sicpro_app_administracion`

### Modelos Python

- `Credenciales`
- `CredencialesAccesos`
- `CredencialesCancelacion`
- `CredencialesSiglas`
- `CredencialesTipo`
- `DashboardExtendidoIdentificador`

### Wizards / TransientModel

- `CredencialesCancelarTrabajadores`
- `CredencialesImageCropper`

### Python

- `sicpro_app_credenciales/__init__.py`
- `sicpro_app_credenciales/__manifest__.py`
- `sicpro_app_credenciales/models/__init__.py`
- `sicpro_app_credenciales/models/dashboard_extendido_identificador.py`
- `sicpro_app_credenciales/models/sicpro_app_credenciales.py`
- `sicpro_app_credenciales/models/sicpro_app_credenciales_accesos.py`
- `sicpro_app_credenciales/models/sicpro_app_credenciales_alcance.py`
- `sicpro_app_credenciales/models/sicpro_app_credenciales_cancelacion.py`
- `sicpro_app_credenciales/models/sicpro_app_credenciales_siglas.py`
- `sicpro_app_credenciales/models/sicpro_app_credenciales_tipo.py`
- `sicpro_app_credenciales/wizards/__init__.py`
- `sicpro_app_credenciales/wizards/recortador_de_imagenes.py`

### XML

- `sicpro_app_credenciales/data/ir_cron.xml`
- `sicpro_app_credenciales/data/mail_template.xml`
- `sicpro_app_credenciales/data/sicpro_app_credenciales_accesos.xml`
- `sicpro_app_credenciales/data/sicpro_app_credenciales_alcance.xml`
- `sicpro_app_credenciales/data/sicpro_app_credenciales_siglas.xml`
- `sicpro_app_credenciales/data/sicpro_app_credenciales_tipo.xml`
- `sicpro_app_credenciales/informes/credencial_laptop.xml`
- `sicpro_app_credenciales/informes/credencial_personal.xml`
- `sicpro_app_credenciales/informes/credencial_personal_laptop.xml`
- `sicpro_app_credenciales/informes/credencial_pvc.xml`
- `sicpro_app_credenciales/informes/plantilla.xml`
- `sicpro_app_credenciales/security/security.xml`
- `sicpro_app_credenciales/static/src/xml/templates_recortador.xml`
- `sicpro_app_credenciales/views/credenciales_accesos_views.xml`
- `sicpro_app_credenciales/views/credenciales_alcance.xml`
- `sicpro_app_credenciales/views/credenciales_cancelacion_views.xml`
- `sicpro_app_credenciales/views/credenciales_menu_views.xml`
- `sicpro_app_credenciales/views/credenciales_siglas_views.xml`
- `sicpro_app_credenciales/views/credenciales_tipo_views.xml`
- `sicpro_app_credenciales/views/credenciales_views.xml`
- `sicpro_app_credenciales/wizards/recortador_de_imagenes.xml`

### JavaScript / OWL

- `sicpro_app_credenciales/static/lib/cropper/cropper.min.js`
- `sicpro_app_credenciales/static/src/js/image_processing.js`
- `sicpro_app_credenciales/static/src/js/imagen_con_recortar.js`
- `sicpro_app_credenciales/static/src/js/widget_recortar_imagen.js`

### CSV / Seguridad / Datos

- `sicpro_app_credenciales/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_app_credenciales/static/lib/cropper/cropper.min.css`
- `sicpro_app_credenciales/static/src/css/credencial_pvc.css`
- `sicpro_app_credenciales/static/src/scss/imagen_con_recortar.scss`
- `sicpro_app_credenciales/static/src/scss/recortador.scss`
- `sicpro_app_credenciales/static/src/scss/sicpro_app_credenciales.backend.scss`

---

## sicpro_app_db_explorer

**Ruta:** `sicpro_app/sicpro_app_db_explorer`

### Manifest

- **name:** `SICPRO: DB-Master Explorer`
- **version:** `19.0.0.0.1`
- **category:** `Administración`
- **summary:** `Gestión dinámica y edición de tablas crudas con seguridad de doble factor.`
- **description:** `Herramienta de administración avanzada para visualizar y editar cualquier tabla del sistema dinámicamente. Incluye bloqueo de seguridad por contraseña maestra.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `LogAnomalyRule`
- `LogRecord`
- `LogSeverity`
- `LogSource`
- `LogTag`
- `SicproDBAuditLog`
- `SicproDBExplorerTable`
- `SicproLogAnomalyRule`
- `SicproLogRecord`
- `SicproLogSeverity`
- `SicproLogSource`
- `SicproLogTag`

### Wizards / TransientModel

- `SicproMasterPasswordWizard`

### Python

- `sicpro_app_db_explorer/__init__.py`
- `sicpro_app_db_explorer/__manifest__.py`
- `sicpro_app_db_explorer/models/__init__.py`
- `sicpro_app_db_explorer/models/db_audit_log.py`
- `sicpro_app_db_explorer/models/db_explorer.py`
- `sicpro_app_db_explorer/models/log_config.py`
- `sicpro_app_db_explorer/models/log_record.py`
- `sicpro_app_db_explorer/models/sicpro_app_log_anomaly_rule.py`
- `sicpro_app_db_explorer/models/sicpro_app_log_record.py`
- `sicpro_app_db_explorer/models/sicpro_app_log_severity.py`
- `sicpro_app_db_explorer/models/sicpro_app_log_sources.py`
- `sicpro_app_db_explorer/models/sicpro_app_log_tag.py`
- `sicpro_app_db_explorer/wizard/__init__.py`
- `sicpro_app_db_explorer/wizard/master_password_wizard.py`

### XML

- `sicpro_app_db_explorer/data/security_config_data.xml`
- `sicpro_app_db_explorer/data/table_blacklist_data.xml`
- `sicpro_app_db_explorer/security/log_report.xml`
- `sicpro_app_db_explorer/security/security.xml`
- `sicpro_app_db_explorer/views/db_audit_log_views.xml`
- `sicpro_app_db_explorer/views/db_explorer_views.xml`
- `sicpro_app_db_explorer/views/log_config_views.xml`
- `sicpro_app_db_explorer/views/log_record_views.xml`
- `sicpro_app_db_explorer/views/menus.xml`
- `sicpro_app_db_explorer/wizard/master_password_wizard_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_db_explorer/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_app_db_explorer/static/src/css/explorer_style.css`

---

## sicpro_app_encuestas

**Ruta:** `sicpro_app/sicpro_app_encuestas`

### Manifest

- **name:** `SICPRO: Encuestas`
- **version:** `19.0.0.0.1`
- **category:** `Productividad`
- **summary:** `Esta aplicación se encargará de todo el control de las encuestas y pruebas creadas por los usuarios.`
- **description:** `Esta aplicación se encargará de todo el control de las encuestas y pruebas creadas por los usuarios.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `survey`
- `sicpro_app_trabajadores`
- `sicpro_app_administracion`

### Modelos Python

- `SurveyUserInput`

### Python

- `sicpro_app_encuestas/__init__.py`
- `sicpro_app_encuestas/__manifest__.py`
- `sicpro_app_encuestas/models/__init__.py`
- `sicpro_app_encuestas/models/survey_user_input.py`

### XML

- `sicpro_app_encuestas/views/survey_templates.xml`
- `sicpro_app_encuestas/views/survey_user_views.xml`

---

## sicpro_app_gestor_documental

**Ruta:** `sicpro_app/sicpro_app_gestor_documental`

### Manifest

- **name:** `SICPRO: Gestor Documental`
- **version:** `19.0.0.0.1`
- **category:** `Documentos`
- **summary:** `Gestor de los Documentos de la DVPE`
- **description:** `Esta aplicación se encargará de todo el control de la documentación de la división`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `base`
- `mail`

### Modelos Python

- `GestorDocumentos`

### Python

- `sicpro_app_gestor_documental/__init__.py`
- `sicpro_app_gestor_documental/__manifest__.py`
- `sicpro_app_gestor_documental/models/__init__.py`
- `sicpro_app_gestor_documental/models/sicpro_app_documentos.py`

### XML

- `sicpro_app_gestor_documental/security/security.xml`
- `sicpro_app_gestor_documental/views/gestor_documental_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_gestor_documental/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_app_gestor_documental/static/src/css/document_management_system.scss`

---

## sicpro_app_gitlab

**Ruta:** `sicpro_app/sicpro_app_gitlab`

### Manifest

- **name:** `SICPRO: Acceso directo a GitLab`
- **version:** `19.0.0.0.1`
- **category:** `Administración`
- **summary:** `Permite la integración del SICPRO ERP con la aplicación de Gitlab`
- **description:** `Permite la integración del SICPRO ERP con la aplicación de Gitlab`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `base`

### Python

- `sicpro_app_gitlab/__init__.py`
- `sicpro_app_gitlab/__manifest__.py`

### XML

- `sicpro_app_gitlab/views/gitlab_views.xml`

---

## sicpro_app_instrucciones

**Ruta:** `sicpro_app/sicpro_app_instrucciones`

### Manifest

- **name:** `SICPRO: Instrucciones Laborales`
- **version:** `19.0.0.0.1`
- **category:** `Trabajadores`
- **summary:** `Esta aplicación se encargará de todo el control de las instrucciones que se le realizan a los trabajadores`
- **description:** `Esta aplicación se encargará de todo el control de las instrucciones que se le realizan a los trabajadores`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `survey`
- `sicpro_app_trabajadores`
- `sicpro_app_encuestas`
- `sicpro_app_administracion`

### Modelos Python

- `InstruccionesEtiquetas`
- `InstruccionesInstruccion`
- `InstruccionesTrabajador`
- `UsersContext`

### Python

- `sicpro_app_instrucciones/__init__.py`
- `sicpro_app_instrucciones/__manifest__.py`
- `sicpro_app_instrucciones/controllers/__init__.py`
- `sicpro_app_instrucciones/controllers/main.py`
- `sicpro_app_instrucciones/models/__init__.py`
- `sicpro_app_instrucciones/models/res_users.py`
- `sicpro_app_instrucciones/models/sicpro_app_instrucciones_etiquetas.py`
- `sicpro_app_instrucciones/models/sicpro_app_instrucciones_instruccion.py`
- `sicpro_app_instrucciones/models/sicpro_app_instrucciones_trabajador.py`

### XML

- `sicpro_app_instrucciones/data/ir_cron.xml`
- `sicpro_app_instrucciones/data/mail_template.xml`
- `sicpro_app_instrucciones/informes/informe_modelo_instrucciones_views.xml`
- `sicpro_app_instrucciones/security/security.xml`
- `sicpro_app_instrucciones/views/instrucciones_dashboard_views.xml`
- `sicpro_app_instrucciones/views/instrucciones_etiquetas_views.xml`
- `sicpro_app_instrucciones/views/instrucciones_instruccion_views.xml`
- `sicpro_app_instrucciones/views/instrucciones_menu_views.xml`
- `sicpro_app_instrucciones/views/instrucciones_trabajador_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_instrucciones/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_app_instrucciones/static/src/scss/instrucciones.scss`

---

## sicpro_app_log_guardian

**Ruta:** `sicpro_app/sicpro_app_log_guardian`

### Manifest

- **name:** `SICPRO: Log Guardian`
- **version:** `19.0.0.0.1`
- **category:** `Administración`
- **summary:** `Gestión centralizada de Logs, monitorización y ciclo de vida de errores.`
- **description:** `Módulo avanzado para la lectura, monitorización y gestión de resoluciones de archivos de Log (Odoo, Nginx, PostgreSQL) integrando detecciones de anomalías y alertas en tiempo real para el ecosistema SICPRO.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `sicpro_app_administracion`

### Modelos Python

- `SicproLogAnomalyRule`
- `SicproLogRecord`
- `SicproLogSeverity`
- `SicproLogSource`
- `SicproLogTag`

### Python

- `sicpro_app_log_guardian/__init__.py`
- `sicpro_app_log_guardian/__manifest__.py`
- `sicpro_app_log_guardian/models/__init__.py`
- `sicpro_app_log_guardian/models/sicpro_app_log_anomaly_rule.py`
- `sicpro_app_log_guardian/models/sicpro_app_log_record.py`
- `sicpro_app_log_guardian/models/sicpro_app_log_severity.py`
- `sicpro_app_log_guardian/models/sicpro_app_log_sources.py`
- `sicpro_app_log_guardian/models/sicpro_app_log_tag.py`

### XML

- `sicpro_app_log_guardian/data/anomaly_detection_rules.xml`
- `sicpro_app_log_guardian/data/email_templates_data.xml`
- `sicpro_app_log_guardian/data/log_sources_data.xml`
- `sicpro_app_log_guardian/data/retention_rules_data.xml`
- `sicpro_app_log_guardian/data/sequence_data.xml`
- `sicpro_app_log_guardian/data/severity_mappings_data.xml`
- `sicpro_app_log_guardian/report/log_report.xml`
- `sicpro_app_log_guardian/security/security.xml`
- `sicpro_app_log_guardian/views/log_config_views.xml`
- `sicpro_app_log_guardian/views/log_record_views.xml`
- `sicpro_app_log_guardian/views/menus.xml`

### CSV / Seguridad / Datos

- `sicpro_app_log_guardian/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_app_log_guardian/static/src/css/log_styles.css`

---

## sicpro_app_materiales_insumos

**Ruta:** `sicpro_app/sicpro_app_materiales_insumos`

### Manifest

- **name:** `SICPRO: Materiales e Insumos`
- **version:** `19.0.0.0.1`
- **category:** `Producción`
- **summary:** `Esta aplicación le ofrece un control de los Materiales e Insumos que se utilizan en los procesos.`
- **description:** `Esta aplicación le ofrece un control de los Materiales e Insumos que se utilizan en los procesos.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `base`
- `mail`
- `sicpro_modulo_nomencladores`

### Modelos Python

- `MaterialesInsumos`
- `ProductosEtiquetas`
- `ProductosUM`

### Python

- `sicpro_app_materiales_insumos/__init__.py`
- `sicpro_app_materiales_insumos/__manifest__.py`
- `sicpro_app_materiales_insumos/models/__init__.py`
- `sicpro_app_materiales_insumos/models/sicpro_app_productos.py`
- `sicpro_app_materiales_insumos/models/sicpro_app_productos_etiquetas.py`
- `sicpro_app_materiales_insumos/models/sicpro_app_productos_um.py`

### XML

- `sicpro_app_materiales_insumos/data/sicpro_app_materiales_insumos_etiquetas.xml`
- `sicpro_app_materiales_insumos/data/sicpro_app_materiales_insumos_um.xml`
- `sicpro_app_materiales_insumos/security/security.xml`
- `sicpro_app_materiales_insumos/views/productos_etiquetas_views.xml`
- `sicpro_app_materiales_insumos/views/productos_materiales_insumos_views.xml`
- `sicpro_app_materiales_insumos/views/productos_um_views.xml`
- `sicpro_app_materiales_insumos/views/productos_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_materiales_insumos/security/ir.model.access.csv`

---

## sicpro_app_medios_informaticos

**Ruta:** `sicpro_app/sicpro_app_medios_informaticos`

### Manifest

- **name:** `SICPRO: Medios Informáticos`
- **version:** `19.0.0.0.1`
- **category:** `Servicios de Apoyo`
- **summary:** `Esta aplicación se encarga del control, gestión de mantenimiento y destinos finales de los medios informáticos.`
- **description:** `Esta aplicación se encarga del control, gestión de mantenimiento y destinos finales de los medios informáticos.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`
- `sicpro_modulo_nomencladores`
- `sicpro_app_trabajadores`

### Modelos Python

- `ApiConectorHistorial`
- `MediosInformaticos`
- `MediosInformaticosBajas`
- `MediosInformaticosImportar`
- `MediosInformaticosPdtesPiezas`
- `MediosInformaticosTaller`
- `MediosInformaticosTipoEquipo`
- `Trabajadores`

### Wizards / TransientModel

- `MediosInformaticosImportarWizard`

### Python

- `sicpro_app_medios_informaticos/__init__.py`
- `sicpro_app_medios_informaticos/__manifest__.py`
- `sicpro_app_medios_informaticos/models/__init__.py`
- `sicpro_app_medios_informaticos/models/sicpro_app_medios_informaticos.py`
- `sicpro_app_medios_informaticos/models/sicpro_app_medios_informaticos_bajas.py`
- `sicpro_app_medios_informaticos/models/sicpro_app_medios_informaticos_historial.py`
- `sicpro_app_medios_informaticos/models/sicpro_app_medios_informaticos_importar.py`
- `sicpro_app_medios_informaticos/models/sicpro_app_medios_informaticos_pdtes_piezas.py`
- `sicpro_app_medios_informaticos/models/sicpro_app_medios_informaticos_taller.py`
- `sicpro_app_medios_informaticos/models/sicpro_app_medios_informaticos_tipo_equipo.py`
- `sicpro_app_medios_informaticos/models/sicpro_app_medios_informaticos_tramites.py`
- `sicpro_app_medios_informaticos/models/sicpro_app_trabajadores.py`
- `sicpro_app_medios_informaticos/wizard/__init__.py`
- `sicpro_app_medios_informaticos/wizard/medios_informaticos_importar_wizard.py`

### XML

- `sicpro_app_medios_informaticos/data/mail_template.xml`
- `sicpro_app_medios_informaticos/data/sicpro_app_medios_informaticos_tipo_equipo.xml`
- `sicpro_app_medios_informaticos/data/sicpro_app_medios_informaticos_tramites.xml`
- `sicpro_app_medios_informaticos/security/security.xml`
- `sicpro_app_medios_informaticos/static/src/xml/importar_medios_informaticos.xml`
- `sicpro_app_medios_informaticos/views/medios_informaticos_baja_views.xml`
- `sicpro_app_medios_informaticos/views/medios_informaticos_historial_views.xml`
- `sicpro_app_medios_informaticos/views/medios_informaticos_importar_views.xml`
- `sicpro_app_medios_informaticos/views/medios_informaticos_menu_views.xml`
- `sicpro_app_medios_informaticos/views/medios_informaticos_pendientes_piezas_views.xml`
- `sicpro_app_medios_informaticos/views/medios_informaticos_taller_views.xml`
- `sicpro_app_medios_informaticos/views/medios_informaticos_tipo_equipo_views.xml`
- `sicpro_app_medios_informaticos/views/medios_informaticos_trabajador_views.xml`
- `sicpro_app_medios_informaticos/views/medios_informaticos_tramites_views.xml`
- `sicpro_app_medios_informaticos/views/medios_informaticos_views.xml`
- `sicpro_app_medios_informaticos/wizard/medios_informaticos_importar_wizard_views.xml`

### JavaScript / OWL

- `sicpro_app_medios_informaticos/static/src/js/importar_medios_informaticos.js`

### CSV / Seguridad / Datos

- `sicpro_app_medios_informaticos/security/ir.model.access.csv`

---

## sicpro_app_metrologia

**Ruta:** `sicpro_app/sicpro_app_metrologia`

### Manifest

- **name:** `SICPRO: Metrología`
- **version:** `19.0.0.0.1`
- **category:** `Servicios de Apoyo`
- **summary:** `Esta aplicación se encargará de todo el control de los instrumentos de medición de la división.`
- **description:** `Esta aplicación se encargará de todo el control de los instrumentos de medición de la división.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `sicpro_app_administracion`
- `sicpro_modulo_nomencladores`
- `sicpro_app_trabajadores`

### Modelos Python

- `MetrologiaCentroCalibracion`
- `MetrologiaDirecciones`
- `MetrologiaEquipos`
- `MetrologiaEquiposTransferencias`
- `MetrologiaEstadoTecnico`
- `MetrologiaMagnitudes`
- `Trabajadores`

### Python

- `sicpro_app_metrologia/__init__.py`
- `sicpro_app_metrologia/__manifest__.py`
- `sicpro_app_metrologia/models/__init__.py`
- `sicpro_app_metrologia/models/sicpro_app_metrologia_centro_calibracion.py`
- `sicpro_app_metrologia/models/sicpro_app_metrologia_equipos.py`
- `sicpro_app_metrologia/models/sicpro_app_metrologia_equipos_procesos.py`
- `sicpro_app_metrologia/models/sicpro_app_metrologia_estado_tecnico.py`
- `sicpro_app_metrologia/models/sicpro_app_metrologia_magnitud.py`
- `sicpro_app_metrologia/models/sicpro_app_trabajadores.py`

### XML

- `sicpro_app_metrologia/data/ir_cron.xml`
- `sicpro_app_metrologia/data/mail_template.xml`
- `sicpro_app_metrologia/data/sicpro_app_metrologia_centro_calibracion.xml`
- `sicpro_app_metrologia/data/sicpro_app_metrologia_estado_tecnico.xml`
- `sicpro_app_metrologia/security/security.xml`
- `sicpro_app_metrologia/views/mail_activity_views.xml`
- `sicpro_app_metrologia/views/metrologia_centro_calibracion_views.xml`
- `sicpro_app_metrologia/views/metrologia_dashboard_equipos_views.xml`
- `sicpro_app_metrologia/views/metrologia_equipamientos_views.xml`
- `sicpro_app_metrologia/views/metrologia_equipos_procesos_views.xml`
- `sicpro_app_metrologia/views/metrologia_estado_tecnico_views.xml`
- `sicpro_app_metrologia/views/metrologia_magnitudes_views.xml`
- `sicpro_app_metrologia/views/metrologia_menu_views.xml`
- `sicpro_app_metrologia/views/metrologia_plan_calibracion_views.xml`
- `sicpro_app_metrologia/views/metrologia_registro_magnitudes_views.xml`
- `sicpro_app_metrologia/views/metrologia_todos_equipos_views.xml`
- `sicpro_app_metrologia/views/metrologia_trabajadores_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_metrologia/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_app_metrologia/static/src/scss/maintenance_team_dashboard.scss`

---

## sicpro_app_multimedia

**Ruta:** `sicpro_app/sicpro_app_multimedia`

### Manifest

- **name:** `SICPRO: Almacén Multimedia Centralizado`
- **version:** `19.0.0.0.1`
- **category:** `Administración`
- **summary:** `Gestión centralizada y optimizada de activos multimedia para todos los módulos de SICPRO.`
- **description:** `Gestión centralizada y optimizada de activos multimedia para todos los módulos de SICPRO.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `SicproMultimediaAsset`
- `SicproMultimediaMixin`
- `SicproMultimediaTag`

### Python

- `sicpro_app_multimedia/__init__.py`
- `sicpro_app_multimedia/__manifest__.py`
- `sicpro_app_multimedia/models/__init__.py`
- `sicpro_app_multimedia/models/multimedia_asset.py`
- `sicpro_app_multimedia/models/multimedia_mixin.py`
- `sicpro_app_multimedia/models/multimedia_tag.py`

### XML

- `sicpro_app_multimedia/data/ir_cron_data.xml`
- `sicpro_app_multimedia/informes/informe_vivienda_anexo_2_views.xml`
- `sicpro_app_multimedia/informes/informe_vivienda_anexo_3_views.xml`
- `sicpro_app_multimedia/informes/informe_vivienda_anexo_4_views.xml`
- `sicpro_app_multimedia/informes/informe_vivienda_estadisticas_views.xml`
- `sicpro_app_multimedia/informes/reporte_vivienda_consolidad_compras_views.xml`
- `sicpro_app_multimedia/security/security.xml`
- `sicpro_app_multimedia/views/multimedia_asset_views.xml`
- `sicpro_app_multimedia/views/multimedia_tag_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_multimedia/security/ir.model.access.csv`

---

## sicpro_app_ordenes_trabajo

**Ruta:** `sicpro_app/sicpro_app_ordenes_trabajo`

### Manifest

- **name:** `SICPRO: Órdenes de Trabajo`
- **version:** `19.0.0.0.1`
- **category:** `Producción`
- **summary:** `Esta aplicación se encarga de la creación y control de las órdenes de trabajo de inversiones y mantenimiento.`
- **description:** `Esta aplicación se encarga de la creación y control de las órdenes de trabajo de inversiones y mantenimiento.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `base`
- `calendar`
- `sicpro_app_clientes`
- `sicpro_app_trabajadores`
- `sicpro_app_transporte`
- `sicpro_app_solicitudes`

### Modelos Python

- `OrdenesClasesProyectos`
- `OrdenesEstados`
- `OrdenesEstadosTrabajador`
- `OrdenesEstadosTransporteEquipos`
- `OrdenesEtiquetas`
- `OrdenesGrupoTransporte`
- `OrdenesGrupoTransporteEquipos`
- `OrdenesParalizacion`
- `OrdenesProblemas`
- `OrdenesProgramaConsecutivos`
- `OrdenesProgramaInversiones`
- `OrdenesTrabajo`
- `OrdenesTrabajoAnexoProblemas`
- `OrdenesTrabajoEquiposComplementarios`
- `OrdenesTrabajoEquiposEspecializados`
- `OrdenesTrabajoTrabajadores`
- `OrdenesTrabajoTransporte`

### Wizards / TransientModel

- `OrdenesTrabajoAvisoIntension`
- `OrdenesTrabajoMotivoCancelacion`
- `OrdenesTrabajoMotivoParalizacion`
- `OrdenesTrabajoMotivoRechazo`
- `OrdensAnexo3`

### Python

- `sicpro_app_ordenes_trabajo/__init__.py`
- `sicpro_app_ordenes_trabajo/__manifest__.py`
- `sicpro_app_ordenes_trabajo/models/__init__.py`
- `sicpro_app_ordenes_trabajo/models/sicpro_app_ordenes_clases_proyecto.py`
- `sicpro_app_ordenes_trabajo/models/sicpro_app_ordenes_consecutivos.py`
- `sicpro_app_ordenes_trabajo/models/sicpro_app_ordenes_estados.py`
- `sicpro_app_ordenes_trabajo/models/sicpro_app_ordenes_estados_trabajador.py`
- `sicpro_app_ordenes_trabajo/models/sicpro_app_ordenes_estados_transporte_equipos.py`
- `sicpro_app_ordenes_trabajo/models/sicpro_app_ordenes_etiquetas.py`
- `sicpro_app_ordenes_trabajo/models/sicpro_app_ordenes_grupo_transporte_equipos.py`
- `sicpro_app_ordenes_trabajo/models/sicpro_app_ordenes_paralizacion.py`
- `sicpro_app_ordenes_trabajo/models/sicpro_app_ordenes_problemas.py`
- `sicpro_app_ordenes_trabajo/models/sicpro_app_ordenes_programa_inversiones.py`
- `sicpro_app_ordenes_trabajo/models/sicpro_app_ordenes_trabajo.py`
- `sicpro_app_ordenes_trabajo/wizard/__init__.py`
- `sicpro_app_ordenes_trabajo/wizard/ordenes_modelo_anexo3_wizard.py`

### XML

- `sicpro_app_ordenes_trabajo/data/mail_template.xml`
- `sicpro_app_ordenes_trabajo/data/sicpro_app_ordenes_clases_proyecto.xml`
- `sicpro_app_ordenes_trabajo/data/sicpro_app_ordenes_consecutivos.xml`
- `sicpro_app_ordenes_trabajo/data/sicpro_app_ordenes_estados.xml`
- `sicpro_app_ordenes_trabajo/data/sicpro_app_ordenes_etiquetas.xml`
- `sicpro_app_ordenes_trabajo/data/sicpro_app_ordenes_paralizacion.xml`
- `sicpro_app_ordenes_trabajo/data/sicpro_app_ordenes_problemas.xml`
- `sicpro_app_ordenes_trabajo/data/sicpro_app_ordenes_programa_inversiones.xml`
- `sicpro_app_ordenes_trabajo/informes/informe_ordenes_anexo_3_views.xml`
- `sicpro_app_ordenes_trabajo/security/security.xml`
- `sicpro_app_ordenes_trabajo/views/ordenes_clases_proyectos_views.xml`
- `sicpro_app_ordenes_trabajo/views/ordenes_consecutivos_views.xml`
- `sicpro_app_ordenes_trabajo/views/ordenes_estado_ordenes_views.xml`
- `sicpro_app_ordenes_trabajo/views/ordenes_estados_trabajador_views.xml`
- `sicpro_app_ordenes_trabajo/views/ordenes_estados_transporte_equipos_views.xml`
- `sicpro_app_ordenes_trabajo/views/ordenes_estados_views.xml`
- `sicpro_app_ordenes_trabajo/views/ordenes_etiquetas_views.xml`
- `sicpro_app_ordenes_trabajo/views/ordenes_grupos_transporte_equipos_views.xml`
- `sicpro_app_ordenes_trabajo/views/ordenes_menu_views.xml`
- `sicpro_app_ordenes_trabajo/views/ordenes_paralizacion_views.xml`
- `sicpro_app_ordenes_trabajo/views/ordenes_problemas_views.xml`
- `sicpro_app_ordenes_trabajo/views/ordenes_programa_inversiones_views.xml`
- `sicpro_app_ordenes_trabajo/views/ordenes_trabajo_views.xml`
- `sicpro_app_ordenes_trabajo/wizard/ordenes_modelo_anexo3_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_ordenes_trabajo/security/ir.model.access.csv`

---

## sicpro_app_programa_viviendas

**Ruta:** `sicpro_app/sicpro_app_programa_viviendas`

### Manifest

- **name:** `SICPRO: Programa de la vivienda`
- **version:** `19.0.0.0.1`
- **category:** `Trabajadores`
- **summary:** `Módulo para el control de los materiales que se asignan a los trabajadores de la DVPE por el programa de la vivienda.`
- **description:** `Módulo para el control de los materiales que se asignan a los trabajadores de la DVPE por el programa de la vivienda.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`
- `sicpro_app_trabajadores`
- `sicpro_modulo_nomencladores_sindicato`

### Modelos Python

- `Trabajadores`
- `ViviendaEscalafon`
- `ViviendaEtapas`
- `ViviendaFondo`
- `ViviendaMateriales`
- `ViviendaMaterialesUM`
- `ViviendaOfertas`
- `ViviendaProveedor`
- `ViviendaTrabajador`
- `ViviendaTrabajadorProductos`

### Wizards / TransientModel

- `ViviendaAnexo3`
- `ViviendaAnexo4`
- `ViviendaAnexoEstadistica`
- `ViviendaTrabajadorCancelacion`
- `ViviendaTrabajadorRechazo`

### Python

- `sicpro_app_programa_viviendas/__init__.py`
- `sicpro_app_programa_viviendas/__manifest__.py`
- `sicpro_app_programa_viviendas/models/__init__.py`
- `sicpro_app_programa_viviendas/models/sicpro_app_trabajadores.py`
- `sicpro_app_programa_viviendas/models/sicpro_app_vivienda_escalafon.py`
- `sicpro_app_programa_viviendas/models/sicpro_app_vivienda_etapas.py`
- `sicpro_app_programa_viviendas/models/sicpro_app_vivienda_fondo.py`
- `sicpro_app_programa_viviendas/models/sicpro_app_vivienda_materiales.py`
- `sicpro_app_programa_viviendas/models/sicpro_app_vivienda_materiales_um.py`
- `sicpro_app_programa_viviendas/models/sicpro_app_vivienda_proveedor.py`
- `sicpro_app_programa_viviendas/models/sicpro_app_vivienda_trabajador.py`
- `sicpro_app_programa_viviendas/wizard/__init__.py`
- `sicpro_app_programa_viviendas/wizard/sicpro_app_vivienda_anexo3_reporte_wizard.py`
- `sicpro_app_programa_viviendas/wizard/sicpro_app_vivienda_anexo4_reporte_wizard.py`
- `sicpro_app_programa_viviendas/wizard/sicpro_app_vivienda_estadistica_reporte_wizard.py`
- `sicpro_app_programa_viviendas/wizard/sicpro_app_vivienda_ofertas_wizard.py`

### XML

- `sicpro_app_programa_viviendas/data/mail_template.xml`
- `sicpro_app_programa_viviendas/data/sicpro_app_vivienda_escalafon.xml`
- `sicpro_app_programa_viviendas/informes/informe_vivienda_anexo_2_views.xml`
- `sicpro_app_programa_viviendas/informes/informe_vivienda_anexo_3_views.xml`
- `sicpro_app_programa_viviendas/informes/informe_vivienda_anexo_4_views.xml`
- `sicpro_app_programa_viviendas/informes/informe_vivienda_estadisticas_views.xml`
- `sicpro_app_programa_viviendas/informes/reporte_vivienda_consolidad_compras_views.xml`
- `sicpro_app_programa_viviendas/security/security.xml`
- `sicpro_app_programa_viviendas/views/trabajadores_vivienda_views.xml`
- `sicpro_app_programa_viviendas/views/vivienda_escalafon_views.xml`
- `sicpro_app_programa_viviendas/views/vivienda_etapas_economia_views.xml`
- `sicpro_app_programa_viviendas/views/vivienda_etapas_views.xml`
- `sicpro_app_programa_viviendas/views/vivienda_materiales_um_views.xml`
- `sicpro_app_programa_viviendas/views/vivienda_materiales_views.xml`
- `sicpro_app_programa_viviendas/views/vivienda_menu_views.xml`
- `sicpro_app_programa_viviendas/views/vivienda_proveedor_views.xml`
- `sicpro_app_programa_viviendas/views/vivienda_trabajador_views.xml`
- `sicpro_app_programa_viviendas/wizard/vivienda_anexo3_reporte_wizard_views.xml`
- `sicpro_app_programa_viviendas/wizard/vivienda_anexo4_reporte_wizard_views.xml`
- `sicpro_app_programa_viviendas/wizard/vivienda_estadistica_reporte_wizard_views.xml`
- `sicpro_app_programa_viviendas/wizard/vivienda_ofertas_wizard_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_programa_viviendas/security/ir.model.access.csv`

---

## sicpro_app_repositorio_institucional

**Ruta:** `sicpro_app/sicpro_app_repositorio_institucional`

### Manifest

- **name:** `SICPRO: Repositorio Institucional`
- **version:** `19.0.0.0.1`
- **category:** `Documentos`
- **summary:** `Esta aplicación se encargará de la gestión de la información institucional de la DVPE.`
- **description:** `Esta aplicación se encargará de la gestión de la información institucional de la división`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `sicpro_app_trabajadores`
- `base`
- `mail`

### Modelos Python

- `RepositorioInstitucional`
- `RepositorioInstitucionalAutores`
- `RepositorioInstitucionalEstados`
- `RepositorioInstitucionalEtiquetas`
- `RepositorioInstitucionalFacultad`
- `RepositorioInstitucionalLicencia`
- `RepositorioInstitucionalTipo`
- `RepositorioInstitucionalTutorExterno`
- `RepositorioInstitucionalTutorInterno`

### Python

- `sicpro_app_repositorio_institucional/__init__.py`
- `sicpro_app_repositorio_institucional/__manifest__.py`
- `sicpro_app_repositorio_institucional/models/__init__.py`
- `sicpro_app_repositorio_institucional/models/sicpro_repositorio_institucional.py`
- `sicpro_app_repositorio_institucional/models/sicpro_repositorio_institucional_estado.py`
- `sicpro_app_repositorio_institucional/models/sicpro_repositorio_institucional_etiquetas.py`
- `sicpro_app_repositorio_institucional/models/sicpro_repositorio_institucional_falcultad.py`
- `sicpro_app_repositorio_institucional/models/sicpro_repositorio_institucional_licencia.py`
- `sicpro_app_repositorio_institucional/models/sicpro_repositorio_institucional_tipo.py`

### XML

- `sicpro_app_repositorio_institucional/data/sicpro_app_repo_estados.xml`
- `sicpro_app_repositorio_institucional/data/sicpro_app_repo_facultad.xml`
- `sicpro_app_repositorio_institucional/data/sicpro_app_repo_licencia.xml`
- `sicpro_app_repositorio_institucional/data/sicpro_app_repo_tipo.xml`
- `sicpro_app_repositorio_institucional/security/security.xml`
- `sicpro_app_repositorio_institucional/views/repositorio_estado_views.xml`
- `sicpro_app_repositorio_institucional/views/repositorio_etiquetas_views.xml`
- `sicpro_app_repositorio_institucional/views/repositorio_facultad_views.xml`
- `sicpro_app_repositorio_institucional/views/repositorio_licencia_views.xml`
- `sicpro_app_repositorio_institucional/views/repositorio_menu_views.xml`
- `sicpro_app_repositorio_institucional/views/repositorio_tipo_views.xml`
- `sicpro_app_repositorio_institucional/views/repositorio_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_repositorio_institucional/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_app_repositorio_institucional/static/src/css/repositorio_institucional.scss`

---

## sicpro_app_reuniones

**Ruta:** `sicpro_app/sicpro_app_reuniones`

### Manifest

- **name:** `SICPRO: Gestor de Reuniones`
- **version:** `19.0.0.0.1`
- **category:** `Productividad`
- **summary:** `Gestor de Reuniones, actividades e indicaciones`
- **description:** `Esta aplicación se encarga de la gestión de reuniones y el cumplimiento de los acuerdos realizados en las reuniones de la DVPE`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `sicpro_app_trabajadores`
- `sicpro_app_administracion`

### Modelos Python

- `Reuniones`
- `ReunionesAcuerdos`
- `ReunionesDecisiones`
- `ReunionesDespachos`
- `ReunionesDespachosAgenda`
- `ReunionesDespachosComentarios`
- `ReunionesDespachosParticipantes`
- `ReunionesEstados`
- `ReunionesEtiquetas`
- `ReunionesEtiquetasCategorias`
- `ReunionesLugares`
- `ReunionesParticipantes`

### Wizards / TransientModel

- `AcuerdosCancelados`
- `AcuerdosRechazados`
- `DecisionesCanceladas`
- `DecisionesRechazadas`

### Python

- `sicpro_app_reuniones/__init__.py`
- `sicpro_app_reuniones/__manifest__.py`
- `sicpro_app_reuniones/models/__init__.py`
- `sicpro_app_reuniones/models/sicpro_app_reuniones.py`
- `sicpro_app_reuniones/models/sicpro_app_reuniones_acuerdos.py`
- `sicpro_app_reuniones/models/sicpro_app_reuniones_categorias.py`
- `sicpro_app_reuniones/models/sicpro_app_reuniones_decisiones.py`
- `sicpro_app_reuniones/models/sicpro_app_reuniones_despachos.py`
- `sicpro_app_reuniones/models/sicpro_app_reuniones_despachos_agenda.py`
- `sicpro_app_reuniones/models/sicpro_app_reuniones_despachos_comentarios.py`
- `sicpro_app_reuniones/models/sicpro_app_reuniones_despachos_participantes.py`
- `sicpro_app_reuniones/models/sicpro_app_reuniones_estados.py`
- `sicpro_app_reuniones/models/sicpro_app_reuniones_etiquetas.py`
- `sicpro_app_reuniones/models/sicpro_app_reuniones_lugares.py`
- `sicpro_app_reuniones/models/sicpro_app_reuniones_participantes.py`

### XML

- `sicpro_app_reuniones/data/ir_cron.xml`
- `sicpro_app_reuniones/data/mail_template.xml`
- `sicpro_app_reuniones/data/sicpro_app_reuniones_categorias.xml`
- `sicpro_app_reuniones/data/sicpro_app_reuniones_estados.xml`
- `sicpro_app_reuniones/data/sicpro_app_reuniones_lugares.xml`
- `sicpro_app_reuniones/informes/informe_modelo_despachos_views.xml`
- `sicpro_app_reuniones/security/security.xml`
- `sicpro_app_reuniones/views/reuniones_acuerdos_views.xml`
- `sicpro_app_reuniones/views/reuniones_decisiones_views.xml`
- `sicpro_app_reuniones/views/reuniones_despachos_views.xml`
- `sicpro_app_reuniones/views/reuniones_estados_views.xml`
- `sicpro_app_reuniones/views/reuniones_etiquetas_views.xml`
- `sicpro_app_reuniones/views/reuniones_lugares_views.xml`
- `sicpro_app_reuniones/views/reuniones_menu_views.xml`
- `sicpro_app_reuniones/views/reuniones_participantes_views.xml`
- `sicpro_app_reuniones/views/reuniones_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_reuniones/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_app_reuniones/static/src/scss/event.scss`

---

## sicpro_app_salon_clases

**Ruta:** `sicpro_app/sicpro_app_salon_clases`

### Manifest

- **name:** `SICPRO: Salón de Clases`
- **version:** `19.0.0.0.1`
- **category:** `Documentos`
- **summary:** `Esta aplicación se encargara de la preparación de los usuarios mediante de diversos temas de interés de trabajo.`
- **description:** `Esta aplicación se encargara de la preparación de los usuarios mediante de diversos temas de interés de trabajo.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `web`
- `base`
- `sicpro_app_administracion`

### Modelos Python

- `SalonClases`
- `SalonClasesEtiquetas`
- `SalonClasesTemas`
- `SalonClasesTipo`

### Python

- `sicpro_app_salon_clases/__init__.py`
- `sicpro_app_salon_clases/__manifest__.py`
- `sicpro_app_salon_clases/models/__init__.py`
- `sicpro_app_salon_clases/models/sicpro_app_salon_clases.py`
- `sicpro_app_salon_clases/models/sicpro_app_salon_clases_etiquetas.py`
- `sicpro_app_salon_clases/models/sicpro_app_salon_clases_temas.py`
- `sicpro_app_salon_clases/models/sicpro_app_salon_clases_tipo_tematica.py`

### XML

- `sicpro_app_salon_clases/security/security.xml`
- `sicpro_app_salon_clases/views/salon_clases_etiquetas_views.xml`
- `sicpro_app_salon_clases/views/salon_clases_menu_views.xml`
- `sicpro_app_salon_clases/views/salon_clases_temas_views.xml`
- `sicpro_app_salon_clases/views/salon_clases_tipo_views.xml`
- `sicpro_app_salon_clases/views/salon_clases_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_salon_clases/security/ir.model.access.csv`

---

## sicpro_app_servicios_internos

**Ruta:** `sicpro_app/sicpro_app_servicios_internos`

### Manifest

- **name:** `SICPRO: Servicios Internos`
- **version:** `19.0.0.0.1`
- **category:** `Trabajadores`
- **summary:** `Esta aplicación se encargará del control de los servicios mobiles y de datos asignados a los trabajadores`
- **description:** `Esta aplicación se encargará del control de los servicios mobiles y de datos asignados a los trabajadores`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `sicpro_app_trabajadores`
- `base`

### Modelos Python

- `ServiciosInternosCorreos`
- `ServiciosInternosFijos`
- `ServiciosInternosLineas`
- `ServiciosInternosNauta`
- `ServiciosInternosSolicitudes`
- `ServiciosInternosSolicitudesObservaciones`
- `Trabajadores`

### Wizards / TransientModel

- `SolicitudesCancelado`
- `SolicitudesRechazadoRevision`
- `SolicitudesRechazadoValidacion`

### Python

- `sicpro_app_servicios_internos/__init__.py`
- `sicpro_app_servicios_internos/__manifest__.py`
- `sicpro_app_servicios_internos/models/__init__.py`
- `sicpro_app_servicios_internos/models/sicpro_app_internos_correos.py`
- `sicpro_app_servicios_internos/models/sicpro_app_internos_fijos.py`
- `sicpro_app_servicios_internos/models/sicpro_app_internos_lineas.py`
- `sicpro_app_servicios_internos/models/sicpro_app_internos_nauta.py`
- `sicpro_app_servicios_internos/models/sicpro_app_internos_solicitudes.py`
- `sicpro_app_servicios_internos/models/sicpro_app_internos_solicitudes_observaciones.py`
- `sicpro_app_servicios_internos/models/sicpro_app_trabajadores.py`

### XML

- `sicpro_app_servicios_internos/data/ir_cron.xml`
- `sicpro_app_servicios_internos/data/mail_template.xml`
- `sicpro_app_servicios_internos/informes/informe_anexo1_views.xml`
- `sicpro_app_servicios_internos/informes/informe_anexo2_views.xml`
- `sicpro_app_servicios_internos/informes/informe_compromiso_nauta_views.xml`
- `sicpro_app_servicios_internos/informes/informe_planilla_unica_views.xml`
- `sicpro_app_servicios_internos/security/security.xml`
- `sicpro_app_servicios_internos/views/interno_correos_views.xml`
- `sicpro_app_servicios_internos/views/interno_fijos_views.xml`
- `sicpro_app_servicios_internos/views/interno_lineas_views.xml`
- `sicpro_app_servicios_internos/views/interno_menu_views.xml`
- `sicpro_app_servicios_internos/views/interno_nauta_views.xml`
- `sicpro_app_servicios_internos/views/interno_solicitudes_observaciones_views.xml`
- `sicpro_app_servicios_internos/views/interno_solicitudes_views.xml`
- `sicpro_app_servicios_internos/views/interno_trabajadores_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_servicios_internos/security/ir.model.access.csv`

---

## sicpro_app_solicitudes

**Ruta:** `sicpro_app/sicpro_app_solicitudes`

### Manifest

- **name:** `SICPRO: Solicitudes de Trabajo`
- **version:** `19.0.0.0.1`
- **category:** `Producción`
- **summary:** `Esta aplicación se encargara de la recepción de solicitudes de trabajo y da inicio al proceso de ejecución.`
- **description:** `Esta aplicación se encargara de la recepción de solicitudes de trabajo y da inicio al proceso de ejecución.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `calendar`
- `sicpro_app_clientes`
- `sicpro_app_trabajadores`
- `sicpro_app_administracion`

### Modelos Python

- `Company`
- `IrAttachment`
- `SolicitudesEstados`
- `SolicitudesEtiquetas`
- `SolicitudesOportunidades`
- `SolicitudesRechazadas`

### Wizards / TransientModel

- `SolicitudesAsignacionWizard`
- `SolicitudesMotivoWizard`
- `SolicitudesOportunidadesHorizontales`

### Python

- `sicpro_app_solicitudes/__init__.py`
- `sicpro_app_solicitudes/__manifest__.py`
- `sicpro_app_solicitudes/models/__init__.py`
- `sicpro_app_solicitudes/models/ir_attachment.py`
- `sicpro_app_solicitudes/models/res_company.py`
- `sicpro_app_solicitudes/models/sicpro_app_solicitudes_estado.py`
- `sicpro_app_solicitudes/models/sicpro_app_solicitudes_etiquetas.py`
- `sicpro_app_solicitudes/models/sicpro_app_solicitudes_oportunidades.py`
- `sicpro_app_solicitudes/models/sicpro_app_solicitudes_rechazo.py`
- `sicpro_app_solicitudes/wizard/__init__.py`
- `sicpro_app_solicitudes/wizard/sicpro_app_solicitudes_asignaciones_wizard.py`
- `sicpro_app_solicitudes/wizard/sicpro_app_solicitudes_rechazo_wizard.py`

### XML

- `sicpro_app_solicitudes/data/mail_template.xml`
- `sicpro_app_solicitudes/data/sicpro_app_solicitudes_estados.xml`
- `sicpro_app_solicitudes/data/sicpro_app_solicitudes_etiquetas.xml`
- `sicpro_app_solicitudes/data/sicpro_app_solicitudes_rechazadas.xml`
- `sicpro_app_solicitudes/informes/informe_modelo_solicitud_views.xml`
- `sicpro_app_solicitudes/security/security.xml`
- `sicpro_app_solicitudes/views/res_company.xml`
- `sicpro_app_solicitudes/views/solicitudes_ejecutor_views.xml`
- `sicpro_app_solicitudes/views/solicitudes_estados_views.xml`
- `sicpro_app_solicitudes/views/solicitudes_etiquetas_views.xml`
- `sicpro_app_solicitudes/views/solicitudes_grupos_views.xml`
- `sicpro_app_solicitudes/views/solicitudes_inversionistas_views.xml`
- `sicpro_app_solicitudes/views/solicitudes_menu_views.xml`
- `sicpro_app_solicitudes/views/solicitudes_negociacion_pg_views.xml`
- `sicpro_app_solicitudes/views/solicitudes_negociacion_views.xml`
- `sicpro_app_solicitudes/views/solicitudes_rechazo_views.xml`
- `sicpro_app_solicitudes/views/solicitudes_tablasreportes_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_solicitudes/security/ir.model.access.csv`

---

## sicpro_app_soporte

**Ruta:** `sicpro_app/sicpro_app_soporte`

### Manifest

- **name:** `SICPRO: Soporte`
- **version:** `19.0.0.0.1`
- **category:** `Soporte`
- **summary:** `Esta aplicación se encargara de la gestión del soporte técnico de la administración del sistema.`
- **description:** `Esta aplicación se encargara de la gestión del soporte técnico de la administración del sistema.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `sicpro_app_trabajadores`
- `sicpro_modulo_roles`
- `sicpro_app_administracion`

### Modelos Python

- `IrUiView`
- `SoporteAplicaciones`
- `SoporteBitacora`
- `SoporteCanales`
- `SoporteEquipos`
- `SoporteEstados`
- `SoporteEstadosAplicaciones`
- `SoporteEstadosVersiones`
- `SoporteEstadospaquetes`
- `SoporteEtiquetas`
- `SoporteFragmentosCodigos`
- `SoportePaquetes`
- `SoporteTicket`
- `SoporteTicketTareas`
- `SoporteTicketTodos`
- `SoporteTrabajadores`
- `SoporteVeriones`

### Python

- `sicpro_app_soporte/__init__.py`
- `sicpro_app_soporte/__manifest__.py`
- `sicpro_app_soporte/models/__init__.py`
- `sicpro_app_soporte/models/ir_ui_view.py`
- `sicpro_app_soporte/models/sicpro_app_soporte.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_aplicaciones.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_bitacora.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_canales.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_equipos.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_estados.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_estados_aplicaciones.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_estados_paquetes.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_estados_versiones.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_etiquetas.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_fragmentos_codigos.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_paquetes.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_tareas.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_todos.py`
- `sicpro_app_soporte/models/sicpro_app_soporte_versiones.py`
- `sicpro_app_soporte/models/sicpro_app_trabajadores.py`

### XML

- `sicpro_app_soporte/data/ir_sequence.xml`
- `sicpro_app_soporte/data/mail_template.xml`
- `sicpro_app_soporte/data/sicpro_app_soporte_canales.xml`
- `sicpro_app_soporte/data/sicpro_app_soporte_equipos.xml`
- `sicpro_app_soporte/data/sicpro_app_soporte_estados.xml`
- `sicpro_app_soporte/data/sicpro_app_soporte_estados_aplicaciones.xml`
- `sicpro_app_soporte/data/sicpro_app_soporte_estados_paquetes.xml`
- `sicpro_app_soporte/data/sicpro_app_soporte_estados_versiones.xml`
- `sicpro_app_soporte/data/sicpro_app_soporte_etiquetas.xml`
- `sicpro_app_soporte/security/security.xml`
- `sicpro_app_soporte/views/soporte_aplicaciones_view.xml`
- `sicpro_app_soporte/views/soporte_bitacora_view.xml`
- `sicpro_app_soporte/views/soporte_canales_view.xml`
- `sicpro_app_soporte/views/soporte_dashboard_view.xml`
- `sicpro_app_soporte/views/soporte_equipos_view.xml`
- `sicpro_app_soporte/views/soporte_estados_aplicaciones_view.xml`
- `sicpro_app_soporte/views/soporte_estados_paquetes_view.xml`
- `sicpro_app_soporte/views/soporte_estados_versiones_view.xml`
- `sicpro_app_soporte/views/soporte_estados_view.xml`
- `sicpro_app_soporte/views/soporte_etiquetas_view.xml`
- `sicpro_app_soporte/views/soporte_fragmentos_codigos_view.xml`
- `sicpro_app_soporte/views/soporte_paquetes_view.xml`
- `sicpro_app_soporte/views/soporte_ticket_menu.xml`
- `sicpro_app_soporte/views/soporte_ticket_todos_view.xml`
- `sicpro_app_soporte/views/soporte_ticket_view.xml`
- `sicpro_app_soporte/views/soporte_versiones_view.xml`
- `sicpro_app_soporte/views/trabajadores_view.xml`

### CSV / Seguridad / Datos

- `sicpro_app_soporte/security/ir.model.access.csv`

---

## sicpro_app_trabajadores

**Ruta:** `sicpro_app/sicpro_app_trabajadores`

### Manifest

- **name:** `SICPRO: Trabajadores`
- **version:** `19.0.0.0.1`
- **category:** `Trabajadores`
- **summary:** `Esta aplicación se encargará del control de los datos de los trabajadores.`
- **description:** `Esta aplicación se encargará del control de los datos de los trabajadores.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `resource`
- `calendar`
- `bus`
- `sicpro_app_administracion`
- `sicpro_modulo_nomencladores`

### Modelos Python

- `HrEmployeeAttachment`
- `Trabajadores`
- `TrabajadoresAccionesDisciplinarias`
- `TrabajadoresAreasAltasBajas`
- `TrabajadoresAreasTotales`
- `TrabajadoresCargos`
- `TrabajadoresCategorias`
- `TrabajadoresCategoriasDisciplinarias`
- `TrabajadoresClavesHorasLabor`
- `TrabajadoresCursos`
- `TrabajadoresCursosHabilidades`
- `TrabajadoresCursosNiveles`
- `TrabajadoresCursosTipos`
- `TrabajadoresDepartamentos`
- `TrabajadoresDocumentos`
- `TrabajadoresDocumentosPlantillas`
- `TrabajadoresDocumentosTipos`
- `TrabajadoresEducacion`
- `TrabajadoresEducacionCertificacion`
- `TrabajadoresEducacionTipos`
- `TrabajadoresEquipoTecnico`
- `TrabajadoresFamiliar`
- `TrabajadoresGeneral`
- `TrabajadoresIntrucciones`
- `TrabajadoresLocales`
- `TrabajadoresNexoFamiliar`
- `TrabajadoresProteccionTrabajador`
- `TrabajadoresSeguridadProteccion`
- `TrabajadoresTallas`
- `TrabajadoresVacunacion`
- `Trabajos`
- `Users`

### Python

- `sicpro_app_trabajadores/__init__.py`
- `sicpro_app_trabajadores/__manifest__.py`
- `sicpro_app_trabajadores/models/__init__.py`
- `sicpro_app_trabajadores/models/ir_attachment.py`
- `sicpro_app_trabajadores/models/res_users.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_areas.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_areas_altas_bajas.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_areas_totales.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_calendar.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_cargos.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_categorias.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_claves_horas.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_cursos.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_cursos_habilidades.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_cursos_niveles.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_cursos_tipos.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_disciplinarias_accion.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_disciplinarias_categoria.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_documentos.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_documentos_plantillas.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_documentos_tipos.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_educacion.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_educacion_certificacion.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_educacion_tipos.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_equipo_tecnico.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_familiar.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_intrucciones.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_locales.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_nexo_familiar.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_ocupacion.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_proteccion_trabajador.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_seguridad_proteccion.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_tallas.py`
- `sicpro_app_trabajadores/models/sicpro_app_trabajadores_vacunación.py`

### XML

- `sicpro_app_trabajadores/data/ir_cron.xml`
- `sicpro_app_trabajadores/data/mail_template.xml`
- `sicpro_app_trabajadores/data/sicpro_app_trabajadores_categorias.xml`
- `sicpro_app_trabajadores/data/sicpro_app_trabajadores_cursos_tipos.xml`
- `sicpro_app_trabajadores/data/sicpro_app_trabajadores_disiplinaria_categorias.xml`
- `sicpro_app_trabajadores/data/sicpro_app_trabajadores_documentos_tipos.xml`
- `sicpro_app_trabajadores/data/sicpro_app_trabajadores_educacion_certificacion.xml`
- `sicpro_app_trabajadores/data/sicpro_app_trabajadores_educacion_tipos.xml`
- `sicpro_app_trabajadores/data/sicpro_app_trabajadores_familiar.xml`
- `sicpro_app_trabajadores/data/sicpro_app_trabajadores_tallas.xml`
- `sicpro_app_trabajadores/informes/informe_medida_desciplinaria_views.xml`
- `sicpro_app_trabajadores/report/trabajadores_report_views.xml`
- `sicpro_app_trabajadores/security/security.xml`
- `sicpro_app_trabajadores/static/src/xml/cursos_templates.xml`
- `sicpro_app_trabajadores/static/src/xml/educacion_templates.xml`
- `sicpro_app_trabajadores/views/calendar_trabajadores_views.xml`
- `sicpro_app_trabajadores/views/res_user.xml`
- `sicpro_app_trabajadores/views/trabajadores_areas_altas_bajas_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_areas_totales_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_areas_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_cargos_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_categorias_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_claves_horas_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_cursos_habilidades_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_disciplinaria_categorias_view.xml`
- `sicpro_app_trabajadores/views/trabajadores_disciplinarias_acciones.xml`
- `sicpro_app_trabajadores/views/trabajadores_documentos_view.xml`
- `sicpro_app_trabajadores/views/trabajadores_educacion_tipos_certificacion.xml`
- `sicpro_app_trabajadores/views/trabajadores_educacion_tipos_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_educacion_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_equipo_tecnico_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_familiar_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_instruciones_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_menu_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_ocupacion_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_plantillas_documentos_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_seguridad_proteccion_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_seguridad_trabajador_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_tallas_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_tipo_documento_view.xml`
- `sicpro_app_trabajadores/views/trabajadores_vacunacion_views.xml`
- `sicpro_app_trabajadores/views/trabajadores_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_trabajadores/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_app_trabajadores/static/src/scss/cursos_educacion.scss`
- `sicpro_app_trabajadores/static/src/scss/hr.scss`
- `sicpro_app_trabajadores/static/src/scss/trabajadores.scss`
- `sicpro_app_trabajadores/static/src/scss/variables.scss`

---

## sicpro_app_transferencias_gastos

**Ruta:** `sicpro_app/sicpro_app_transferencias_gastos`

### Manifest

- **name:** `SICPRO: Transferencias de Gastos`
- **version:** `19.0.0.0.1`
- **category:** `Producción`
- **summary:** `Esta aplicación se encarga de gestión y control de las transferencias de gastos generados por los procesos claves de la ejecución.`
- **description:** `Esta aplicación se encarga de gestión y control de las transferencias de gastos generados por los procesos claves de la ejecución.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `base`
- `calendar`
- `sicpro_app_clientes`
- `sicpro_app_solicitudes`
- `sicpro_app_ordenes_trabajo`
- `sicpro_modulo_widget_buscador_one2many`

### Modelos Python

- `OrdenesTrabajo`
- `TransferenciasCuentasGastos`
- `TransferenciasGastos`
- `TransferenciasGastosAjustesHistorial`
- `TransferenciasGastosImportar`
- `TransferenciasGastosOrdenes`
- `TransferenciasGastosOrdenesEstados`
- `TransferenciasGastosOrdenesMorosidad`

### Wizards / TransientModel

- `TransferenciasGastosAjustes`
- `TransferenciasGastosCJ74Wizard`
- `TransferenciasGastosCertificarWizard`
- `TransferenciasGastosImportarWizardOrdenes`
- `TransferenciasOrdenesRechazo`

### Python

- `sicpro_app_transferencias_gastos/__init__.py`
- `sicpro_app_transferencias_gastos/__manifest__.py`
- `sicpro_app_transferencias_gastos/models/__init__.py`
- `sicpro_app_transferencias_gastos/models/sicpro_app_ordenes_trabajo.py`
- `sicpro_app_transferencias_gastos/models/sicpro_app_transferencias_ajustes_historial.py`
- `sicpro_app_transferencias_gastos/models/sicpro_app_transferencias_cuentas_gastos.py`
- `sicpro_app_transferencias_gastos/models/sicpro_app_transferencias_gastos.py`
- `sicpro_app_transferencias_gastos/models/sicpro_app_transferencias_gastos_importar.py`
- `sicpro_app_transferencias_gastos/models/sicpro_app_transferencias_ordenes_estados.py`
- `sicpro_app_transferencias_gastos/models/sicpro_app_transferencias_ordenes_gastos.py`
- `sicpro_app_transferencias_gastos/models/sicpro_app_transferencias_ordenes_morosidad.py`
- `sicpro_app_transferencias_gastos/wizard/__init__.py`
- `sicpro_app_transferencias_gastos/wizard/transferencias_ajustes_wizard.py`
- `sicpro_app_transferencias_gastos/wizard/transferencias_certificar_wizard.py`
- `sicpro_app_transferencias_gastos/wizard/transferencias_gastos_cj74_wizard.py`
- `sicpro_app_transferencias_gastos/wizard/transferencias_ordenes_rechazo_wizard.py`
- `sicpro_app_transferencias_gastos/wizard/transferencias_ordenes_wizard.py`

### XML

- `sicpro_app_transferencias_gastos/data/ir_cron.xml`
- `sicpro_app_transferencias_gastos/data/mail_template.xml`
- `sicpro_app_transferencias_gastos/data/sicpro_app_transferencias_cuentas_gastos.xml`
- `sicpro_app_transferencias_gastos/data/sicpro_app_transferencias_gastos_ordenes_estados.xml`
- `sicpro_app_transferencias_gastos/data/sicpro_app_transferencias_gastos_ordenes_morosidad.xml`
- `sicpro_app_transferencias_gastos/informes/dinamica_contabilizado_view.xml`
- `sicpro_app_transferencias_gastos/informes/dinamica_pendiente_contabilizar_view.xml`
- `sicpro_app_transferencias_gastos/informes/dinamica_pendiente_procesos_view.xml`
- `sicpro_app_transferencias_gastos/informes/dinamica_periodo_clase_coste_view.xml`
- `sicpro_app_transferencias_gastos/informes/informe_modelo_transferencia_gastos.xml`
- `sicpro_app_transferencias_gastos/security/security.xml`
- `sicpro_app_transferencias_gastos/static/src/xml/certificar_gastos_cj74.xml`
- `sicpro_app_transferencias_gastos/static/src/xml/transferir_subir_gastos_cj74.xml`
- `sicpro_app_transferencias_gastos/views/ordenes_trabajo_views.xml`
- `sicpro_app_transferencias_gastos/views/transferencias_ajustes_historial_views.xml`
- `sicpro_app_transferencias_gastos/views/transferencias_cuentas_gastos_views.xml`
- `sicpro_app_transferencias_gastos/views/transferencias_gastos_importar_views.xml`
- `sicpro_app_transferencias_gastos/views/transferencias_gastos_views.xml`
- `sicpro_app_transferencias_gastos/views/transferencias_menu_views.xml`
- `sicpro_app_transferencias_gastos/views/transferencias_ordenes_estados_views.xml`
- `sicpro_app_transferencias_gastos/views/transferencias_ordenes_gastos_views.xml`
- `sicpro_app_transferencias_gastos/views/transferencias_ordenes_morosidad_views.xml`
- `sicpro_app_transferencias_gastos/wizard/transferencias_ajustes_views.xml`
- `sicpro_app_transferencias_gastos/wizard/transferencias_certificar_views.xml`
- `sicpro_app_transferencias_gastos/wizard/transferencias_gastos_cj74_views.xml`
- `sicpro_app_transferencias_gastos/wizard/transferencias_ordenes_rechazo_views.xml`
- `sicpro_app_transferencias_gastos/wizard/transferencias_ordenes_views.xml`

### JavaScript / OWL

- `sicpro_app_transferencias_gastos/static/src/js/certificar_gastos_cj74.js`
- `sicpro_app_transferencias_gastos/static/src/js/transferir_subir_gastos_cj74.js`

### CSV / Seguridad / Datos

- `sicpro_app_transferencias_gastos/security/ir.model.access.csv`

---

## sicpro_app_transporte

**Ruta:** `sicpro_app/sicpro_app_transporte`

### Manifest

- **name:** `SICPRO: Transporte`
- **version:** `19.0.0.0.1`
- **category:** `Transporte`
- **summary:** `Esta aplicación se encargará de todo el control del parque automotor de la división.`
- **description:** `Esta aplicación se encargará de todo el control del parque automotor de la división.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `sicpro_modulo_nomencladores`
- `sicpro_app_trabajadores`
- `sicpro_modulo_widget_contador`
- `sicpro_app_administracion`

### Modelos Python

- `TransporteDistancias`
- `TransporteDistanciasRecorrido`
- `TransporteDistanciasSalida`
- `TransporteEstados`
- `TransporteGeneral`
- `TransporteModeloBrand`
- `TransportePiquera`
- `TransportePiqueraRecorridos`
- `TransporteTipoCombustible`
- `TransporteTrabajadores`

### Wizards / TransientModel

- `TransportePiqueraCanceladas`
- `TransportePiqueraRechazadas`

### Python

- `sicpro_app_transporte/__init__.py`
- `sicpro_app_transporte/__manifest__.py`
- `sicpro_app_transporte/models/__init__.py`
- `sicpro_app_transporte/models/sicpro_app_trabajadores.py`
- `sicpro_app_transporte/models/sicpro_app_transporte.py`
- `sicpro_app_transporte/models/sicpro_app_transporte_distancias.py`
- `sicpro_app_transporte/models/sicpro_app_transporte_estados.py`
- `sicpro_app_transporte/models/sicpro_app_transporte_marca.py`
- `sicpro_app_transporte/models/sicpro_app_transporte_piquera.py`
- `sicpro_app_transporte/models/sicpro_app_transporte_tipo_combustible.py`

### XML

- `sicpro_app_transporte/data/mail_template.xml`
- `sicpro_app_transporte/data/sicpro_app_transporte_estado.xml`
- `sicpro_app_transporte/data/sicpro_app_transporte_modelo.xml`
- `sicpro_app_transporte/informes/informe_costo_piquera.xml`
- `sicpro_app_transporte/informes/informe_modelo_m1.xml`
- `sicpro_app_transporte/security/security.xml`
- `sicpro_app_transporte/views/transporte_combustible_views.xml`
- `sicpro_app_transporte/views/transporte_distancias_views.xml`
- `sicpro_app_transporte/views/transporte_estado_views.xml`
- `sicpro_app_transporte/views/transporte_menu_views.xml`
- `sicpro_app_transporte/views/transporte_modelo_views.xml`
- `sicpro_app_transporte/views/transporte_piquera_view.xml`
- `sicpro_app_transporte/views/transporte_trabajadores.xml`
- `sicpro_app_transporte/views/transporte_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_transporte/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_app_transporte/static/src/css/informe_costo_piquera.scss`
- `sicpro_app_transporte/static/src/css/informe_modelo_m1.scss`

---

## sicpro_app_video_conferencias

**Ruta:** `sicpro_app/sicpro_app_video_conferencias`

### Manifest

- **name:** `SICPRO: Video Conferencias`
- **version:** `19.0.0.0.1`
- **category:** `Productividad`
- **summary:** `Esta aplicación se encarga de la gestión y programación de las videoconferencias mediante la plataforma de JITSI-ETECSA`
- **description:** `Esta aplicación se encarga de la gestión y programación de las videoconferencias mediante la plataforma de JITSI-ETECSA`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `web`
- `sicpro_app_administracion`

### Modelos Python

- `JitsiMeet`
- `JitsiMeetExternalParticipant`

### Python

- `sicpro_app_video_conferencias/__init__.py`
- `sicpro_app_video_conferencias/__manifest__.py`
- `sicpro_app_video_conferencias/models/__init__.py`
- `sicpro_app_video_conferencias/models/sicpro_app_videoconferencias.py`

### XML

- `sicpro_app_video_conferencias/data/ir_config_parameter.xml`
- `sicpro_app_video_conferencias/data/mail_template.xml`
- `sicpro_app_video_conferencias/security/security.xml`
- `sicpro_app_video_conferencias/views/video_conferencias_views.xml`

### CSV / Seguridad / Datos

- `sicpro_app_video_conferencias/security/ir.model.access.csv`

---

## sicpro_app_viveres

**Ruta:** `sicpro_app/sicpro_app_viveres`

### Manifest

- **name:** `SICPRO: Víveres`
- **version:** `19.0.0.0.1`
- **category:** `Trabajadores`
- **summary:** `Esta aplicación se encarga del control de la entrega de víveres a los trabajadores.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`
- `sicpro_modulo_nomencladores`
- `sicpro_app_trabajadores`

### Modelos Python

- `Trabajadores`
- `Viveres`
- `ViveresAreas`
- `ViveresAreasAltasBajas`
- `ViveresAreasEfectivo`
- `ViveresAreasEntregas`
- `ViveresAreasEntregasResumenes`
- `ViveresAreasFondo`
- `ViveresCierre`
- `ViveresProductos`
- `ViveresProductosComprados`
- `ViveresTrabajadoresEntregas`

### Wizards / TransientModel

- `ViveresTrabajadoresEntregaWizard`

### Python

- `sicpro_app_viveres/__init__.py`
- `sicpro_app_viveres/__manifest__.py`
- `sicpro_app_viveres/models/__init__.py`
- `sicpro_app_viveres/models/sicpro_app_trabajadores.py`
- `sicpro_app_viveres/models/sicpro_app_viveres.py`
- `sicpro_app_viveres/models/sicpro_app_viveres_areas.py`
- `sicpro_app_viveres/models/sicpro_app_viveres_areas_altas_bajas.py`
- `sicpro_app_viveres/models/sicpro_app_viveres_areas_efectivo.py`
- `sicpro_app_viveres/models/sicpro_app_viveres_areas_entregas.py`
- `sicpro_app_viveres/models/sicpro_app_viveres_areas_entregas_resumenes.py`
- `sicpro_app_viveres/models/sicpro_app_viveres_areas_fondo.py`
- `sicpro_app_viveres/models/sicpro_app_viveres_cierre.py`
- `sicpro_app_viveres/models/sicpro_app_viveres_productos.py`
- `sicpro_app_viveres/models/sicpro_app_viveres_productos_comprados.py`
- `sicpro_app_viveres/models/sicpro_app_viveres_trabajadores_entregas.py`
- `sicpro_app_viveres/wizard/__init__.py`
- `sicpro_app_viveres/wizard/viveres_trabajadores_entrega_wizard.py`

### XML

- `sicpro_app_viveres/data/mail_template.xml`
- `sicpro_app_viveres/data/sicpro_app_viveres_productos.xml`
- `sicpro_app_viveres/security/security.xml`
- `sicpro_app_viveres/static/src/xml/viveres_distribuir_productos.xml`
- `sicpro_app_viveres/views/viveres_areas_altas_bajas_views.xml`
- `sicpro_app_viveres/views/viveres_areas_efectivo_views.xml`
- `sicpro_app_viveres/views/viveres_areas_entregas_resumenes_views.xml`
- `sicpro_app_viveres/views/viveres_areas_entregas_views.xml`
- `sicpro_app_viveres/views/viveres_areas_fondo_views.xml`
- `sicpro_app_viveres/views/viveres_areas_views.xml`
- `sicpro_app_viveres/views/viveres_cierre_views.xml`
- `sicpro_app_viveres/views/viveres_menu_views.xml`
- `sicpro_app_viveres/views/viveres_productos_comprados_views.xml`
- `sicpro_app_viveres/views/viveres_productos_views.xml`
- `sicpro_app_viveres/views/viveres_trabajador_views.xml`
- `sicpro_app_viveres/views/viveres_trabajadores_entregas_views.xml`
- `sicpro_app_viveres/views/viveres_views.xml`
- `sicpro_app_viveres/wizard/viveres_trabajadores_entrega_wizard_views.xml`

### JavaScript / OWL

- `sicpro_app_viveres/static/src/js/viveres_distribuir_productos.js`

### CSV / Seguridad / Datos

- `sicpro_app_viveres/security/ir.model.access.csv`

---

## sicpro_modulo_actualiza_list_kanban

**Ruta:** `sicpro_app/sicpro_modulo_actualiza_list_kanban`

### Manifest

- **name:** `SICPRO: Actualiza vistas List/Kanban`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite desde un botón actualizar los datos de las vistas de listas y kanban`
- **description:** `Permite desde un botón actualizar los datos de las vistas de listas y kanban`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_actualiza_list_kanban/__init__.py`
- `sicpro_modulo_actualiza_list_kanban/__manifest__.py`

### XML

- `sicpro_modulo_actualiza_list_kanban/static/src/xml/control_panel.xml`
- `sicpro_modulo_actualiza_list_kanban/static/src/xml/refresher.xml`

### JavaScript / OWL

- `sicpro_modulo_actualiza_list_kanban/static/src/js/control_panel.esm.js`
- `sicpro_modulo_actualiza_list_kanban/static/src/js/refresher.esm.js`

### CSS / SCSS

- `sicpro_modulo_actualiza_list_kanban/static/src/scss/refresher.scss`

---

## sicpro_modulo_adjuntos_capacidad

**Ruta:** `sicpro_app/sicpro_modulo_adjuntos_capacidad`

### Manifest

- **name:** `SICPRO: Adjuntos Capacidad`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite la opción de visualizar el tamaño de los archivos adjuntos del SICPRO ERP`
- **description:** `Permite la opción de visualizar el tamaño de los archivos adjuntos del SICPRO ERP`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `IrAttachment`

### Python

- `sicpro_modulo_adjuntos_capacidad/__init__.py`
- `sicpro_modulo_adjuntos_capacidad/__manifest__.py`
- `sicpro_modulo_adjuntos_capacidad/models/__init__.py`
- `sicpro_modulo_adjuntos_capacidad/models/ir_attachment.py`

### XML

- `sicpro_modulo_adjuntos_capacidad/views/ir_attachment_views.xml`

---

## sicpro_modulo_adjuntos_descargar_todos

**Ruta:** `sicpro_app/sicpro_modulo_adjuntos_descargar_todos`

### Manifest

- **name:** `SICPRO: Descargar adjuntos como ZIP`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Descargue todos los archivos adjuntos como un único archivo ZIP desde cualquier modelo directamente desde la vista de lista`
- **description:** `Descargue todos los archivos adjuntos como un único archivo ZIP desde cualquier modelo directamente desde la vista de lista`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_adjuntos_descargar_todos/__init__.py`
- `sicpro_modulo_adjuntos_descargar_todos/__manifest__.py`

### JavaScript / OWL

- `sicpro_modulo_adjuntos_descargar_todos/static/src/list_controller.js`

---

## sicpro_modulo_api_conector

**Ruta:** `sicpro_app/sicpro_modulo_api_conector`

### Manifest

- **name:** `SICPRO: API Conector`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Este módulo se encarga de generar la configuración para la conexión de las aplicaciones con apis externas`
- **description:** `Este módulo se encarga de generar la configuración para la conexión de las aplicaciones con apis externas`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `ApiConector`
- `ApiConectorHistorial`

### Python

- `sicpro_modulo_api_conector/__init__.py`
- `sicpro_modulo_api_conector/__manifest__.py`
- `sicpro_modulo_api_conector/models/__init__.py`
- `sicpro_modulo_api_conector/models/sicpro_api_conector.py`
- `sicpro_modulo_api_conector/models/sicpro_api_conector_historial.py`

### XML

- `sicpro_modulo_api_conector/views/conector_menu_views.xml`
- `sicpro_modulo_api_conector/views/conector_rest_api_historial_views.xml`
- `sicpro_modulo_api_conector/views/conector_rest_api_views.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_api_conector/security/ir.model.access.csv`

---

## sicpro_modulo_api_conector_transporte_sipetc

**Ruta:** `sicpro_app/sicpro_modulo_api_conector_transporte_sipetc`

### Manifest

- **name:** `SICPRO: API Conector (SIPETC)`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Este módulo se encarga de generar la configuración para la conexión de la aplicación de Transporte`
- **description:** `Este módulo se encarga de generar la configuración para la conexión de la aplicación de Transporte`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`
- `sicpro_app_transporte`
- `sicpro_app_trabajadores`
- `sicpro_modulo_api_conector`

### Modelos Python

- `ApiConector`

### Python

- `sicpro_modulo_api_conector_transporte_sipetc/__init__.py`
- `sicpro_modulo_api_conector_transporte_sipetc/__manifest__.py`
- `sicpro_modulo_api_conector_transporte_sipetc/models/__init__.py`
- `sicpro_modulo_api_conector_transporte_sipetc/models/sicpro_api_conector.py`

### XML

- `sicpro_modulo_api_conector_transporte_sipetc/data/ir_cron.xml`
- `sicpro_modulo_api_conector_transporte_sipetc/data/mail_template.xml`
- `sicpro_modulo_api_conector_transporte_sipetc/views/conector_rest_api_views.xml`

---

## sicpro_modulo_audio_video

**Ruta:** `sicpro_app/sicpro_modulo_audio_video`

### Manifest

- **name:** `SICPRO: Audio y Video`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Agrega la función de incorporar archivos de audio y video al campo de html`
- **description:** `Agrega la función de incorporar archivos de audio y video al campo de html`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `html_editor`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_audio_video/__init__.py`
- `sicpro_modulo_audio_video/__manifest__.py`

### XML

- `sicpro_modulo_audio_video/static/src/xml/audio_dialog_template.xml`
- `sicpro_modulo_audio_video/static/src/xml/video_dialog_template.xml`

### JavaScript / OWL

- `sicpro_modulo_audio_video/static/src/js/audio_dialog.js`
- `sicpro_modulo_audio_video/static/src/js/audio_plugin.js`
- `sicpro_modulo_audio_video/static/src/js/video_dialog.js`
- `sicpro_modulo_audio_video/static/src/js/video_plugin.js`

---

## sicpro_modulo_auditorias

**Ruta:** `sicpro_app/sicpro_modulo_auditorias`

### Manifest

- **name:** `SICPRO: Registros de Auditoria`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Auditoría de acciones y peticiones HTTP`
- **description:** `Auditoría de acciones y peticiones HTTP`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `AuditlogHTTPRequest`
- `AuditlogHTTPSession`
- `AuditlogLog`
- `AuditlogLogLine`
- `AuditlogLogLineView`
- `AuditlogRule`

### Wizards / TransientModel

- `AuditlogAutovacuum`

### Python

- `sicpro_modulo_auditorias/__init__.py`
- `sicpro_modulo_auditorias/__manifest__.py`
- `sicpro_modulo_auditorias/models/__init__.py`
- `sicpro_modulo_auditorias/models/auditlog_http_request.py`
- `sicpro_modulo_auditorias/models/auditlog_http_session.py`
- `sicpro_modulo_auditorias/models/auditlog_log.py`
- `sicpro_modulo_auditorias/models/auditlog_log_line.py`
- `sicpro_modulo_auditorias/models/auditlog_log_line_view.py`
- `sicpro_modulo_auditorias/models/auditlog_rule.py`
- `sicpro_modulo_auditorias/wizards/__init__.py`
- `sicpro_modulo_auditorias/wizards/autovacuum.py`

### XML

- `sicpro_modulo_auditorias/data/ir_cron.xml`
- `sicpro_modulo_auditorias/security/res_groups.xml`
- `sicpro_modulo_auditorias/views/auditlog_http_request_views.xml`
- `sicpro_modulo_auditorias/views/auditlog_http_session_views.xml`
- `sicpro_modulo_auditorias/views/auditlog_log_line_views.xml`
- `sicpro_modulo_auditorias/views/auditlog_log_views.xml`
- `sicpro_modulo_auditorias/views/auditlog_rule_views.xml`
- `sicpro_modulo_auditorias/views/menu.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_auditorias/security/ir.model.access.csv`

---

## sicpro_modulo_automatizacion_scripts_python_sql

**Ruta:** `sicpro_app/sicpro_modulo_automatizacion_scripts_python_sql`

### Manifest

- **name:** `SICPRO: Script python/sql`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite correr scripts automatizados de python y consultas sql`
- **description:** `Permite correr scripts automatizados de python y consultas sql`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `execute_script`

### Python

- `sicpro_modulo_automatizacion_scripts_python_sql/__init__.py`
- `sicpro_modulo_automatizacion_scripts_python_sql/__manifest__.py`
- `sicpro_modulo_automatizacion_scripts_python_sql/models/__init__.py`
- `sicpro_modulo_automatizacion_scripts_python_sql/models/execute_script.py`

### XML

- `sicpro_modulo_automatizacion_scripts_python_sql/views/execute_script_view.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_automatizacion_scripts_python_sql/security/ir.model.access.csv`

---

## sicpro_modulo_backup_server

**Ruta:** `sicpro_app/sicpro_modulo_backup_server`

### Manifest

- **name:** `SICPRO: Backup Server Local y Remoto`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Este módulo se encarga de generar las salvas programadas del sistema en el propio servidor`
- **description:** `Este módulo se encarga de generar las salvas programadas del sistema en el propio servidor`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `sicpro_app_administracion`

### Modelos Python

- `SicproBackupLocal`
- `SicproBackupLocalDetalles`
- `SicproBackupRemoteServer`

### Wizards / TransientModel

- `SicproBackupEliminacion`
- `SicproBackupMensajes`

### Python

- `sicpro_modulo_backup_server/__init__.py`
- `sicpro_modulo_backup_server/__manifest__.py`
- `sicpro_modulo_backup_server/controllers/__init__.py`
- `sicpro_modulo_backup_server/controllers/controllers.py`
- `sicpro_modulo_backup_server/models/__init__.py`
- `sicpro_modulo_backup_server/models/lib/check_connectivity.py`
- `sicpro_modulo_backup_server/models/lib/manage_backup_crons.py`
- `sicpro_modulo_backup_server/models/lib/saas_client_backup.py`
- `sicpro_modulo_backup_server/models/sicpro_backup_local.py`
- `sicpro_modulo_backup_server/models/sicpro_backup_local_detalles.py`
- `sicpro_modulo_backup_server/models/sicpro_backup_remote_server.py`
- `sicpro_modulo_backup_server/wizards/__init__.py`
- `sicpro_modulo_backup_server/wizards/sicpro_backup_eliminacion.py`
- `sicpro_modulo_backup_server/wizards/sicpro_backup_mensaje_wizard.py`

### XML

- `sicpro_modulo_backup_server/data/ir_cron.xml`
- `sicpro_modulo_backup_server/data/ir_sequence.xml`
- `sicpro_modulo_backup_server/data/mail_template.xml`
- `sicpro_modulo_backup_server/views/backup_local.xml`
- `sicpro_modulo_backup_server/views/backup_remote_server.xml`
- `sicpro_modulo_backup_server/views/menuitems.xml`
- `sicpro_modulo_backup_server/wizards/backup_custom_message_wizard_view.xml`
- `sicpro_modulo_backup_server/wizards/backup_deletion_confirmation_view.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_backup_server/security/ir.model.access.csv`

---

## sicpro_modulo_boton_editar

**Ruta:** `sicpro_app/sicpro_modulo_boton_editar`

### Manifest

- **name:** `SICPRO: Botón Editar`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Agrega el botón de editar a todas las vistas del sistema`
- **description:** `Agrega el botón de editar a todas las vistas del sistema`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_boton_editar/__init__.py`
- `sicpro_modulo_boton_editar/__manifest__.py`

### XML

- `sicpro_modulo_boton_editar/static/src/views/form/form_controller.xml`

### JavaScript / OWL

- `sicpro_modulo_boton_editar/static/src/views/form/form_controller.js`

---

## sicpro_modulo_boton_guardar

**Ruta:** `sicpro_app/sicpro_modulo_boton_guardar`

### Manifest

- **name:** `SICPRO: Botón Guardar`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Agrega el botón de guardar y cancelar a todas las vistas del sistema`
- **description:** `Agrega el botón de guardar y cancelar a todas las vistas del sistema`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_boton_guardar/__init__.py`
- `sicpro_modulo_boton_guardar/__manifest__.py`

### XML

- `sicpro_modulo_boton_guardar/static/src/views/form/form_status_indicator.xml`

---

## sicpro_modulo_certificados_digitales

**Ruta:** `sicpro_app/sicpro_modulo_certificados_digitales`

### Manifest

- **name:** `SICPRO: Administrar Certificados Digitales`
- **version:** `19.0.0.0.1`
- **category:** `Administración`
- **summary:** `Controla los certificados digitales utilizados por el sistema SICPRO ERP`
- **description:** `Controla los certificados digitales utilizados por el sistema`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `AdministrarCertificadosDigitales`

### Python

- `sicpro_modulo_certificados_digitales/__init__.py`
- `sicpro_modulo_certificados_digitales/__manifest__.py`
- `sicpro_modulo_certificados_digitales/models/__init__.py`
- `sicpro_modulo_certificados_digitales/models/sicpro_modulo_certificados_digitales.py`

### XML

- `sicpro_modulo_certificados_digitales/views/certificados_digitales_views.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_certificados_digitales/security/ir.model.access.csv`

---

## sicpro_modulo_fullscreen

**Ruta:** `sicpro_app/sicpro_modulo_fullscreen`

### Manifest

- **name:** `SICPRO: Vista FullScreen`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite la visualización del sistema en el navegador a pantalla completa`
- **description:** `Permite la visualización del sistema en el navegador a pantalla completa`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_fullscreen/__init__.py`
- `sicpro_modulo_fullscreen/__manifest__.py`

### XML

- `sicpro_modulo_fullscreen/static/src/xml/sicpro_modulo_fullscreen.xml`

### JavaScript / OWL

- `sicpro_modulo_fullscreen/static/src/js/sicpro_modulo_fullscreen.js`

---

## sicpro_modulo_generador_qr

**Ruta:** `sicpro_app/sicpro_modulo_generador_qr`

### Manifest

- **name:** `SICPRO: Generador QR`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite generar códigos QR desde la administración`
- **description:** `Permite generar códigos QR desde la administración`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `QrCodeGenerator`

### Python

- `sicpro_modulo_generador_qr/__init__.py`
- `sicpro_modulo_generador_qr/__manifest__.py`
- `sicpro_modulo_generador_qr/models/__init__.py`
- `sicpro_modulo_generador_qr/models/qr_code.py`

### XML

- `sicpro_modulo_generador_qr/views/qr_code_views.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_generador_qr/security/ir.model.access.csv`

---

## sicpro_modulo_groupby_expand_collapse

**Ruta:** `sicpro_app/sicpro_modulo_groupby_expand_collapse`

### Manifest

- **name:** `SICPRO: Expandir Grupos Vistas de Lista`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Este módulo se encarga de poder expandir los grupos en la vista de árbol o lista`
- **description:** `Este módulo se encarga de poder expandir los grupos en la vista de árbol o lista`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_groupby_expand_collapse/__init__.py`
- `sicpro_modulo_groupby_expand_collapse/__manifest__.py`

### XML

- `sicpro_modulo_groupby_expand_collapse/static/src/xml/expand_collapse_buttons.xml`

### JavaScript / OWL

- `sicpro_modulo_groupby_expand_collapse/static/src/js/groupby_expand_collapse.js`

### CSS / SCSS

- `sicpro_modulo_groupby_expand_collapse/static/src/css/groupby_expand_collapse.css`

---

## sicpro_modulo_historial_aplicaciones

**Ruta:** `sicpro_app/sicpro_modulo_historial_aplicaciones`

### Manifest

- **name:** `SICPRO: Historial de Aplicaciones`
- **version:** `19.0.0.0.1`
- **category:** `Administración`
- **summary:** `Visualización del historial de instalación, desinstalación y actualización de los módulos`
- **description:** `Visualización del historial de instalación, desinstalación y actualización de los módulos`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `IrModuleModule`
- `ModuloHistorial`

### Python

- `sicpro_modulo_historial_aplicaciones/__init__.py`
- `sicpro_modulo_historial_aplicaciones/__manifest__.py`
- `sicpro_modulo_historial_aplicaciones/models/__init__.py`
- `sicpro_modulo_historial_aplicaciones/models/sicpro_modulo_historial.py`

### XML

- `sicpro_modulo_historial_aplicaciones/views/historial_aplicaciones_view.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_historial_aplicaciones/security/ir.model.access.csv`

---

## sicpro_modulo_historial_cron

**Ruta:** `sicpro_app/sicpro_modulo_historial_cron`

### Manifest

- **name:** `SICPRO: Historial de Ejecución Cron`
- **version:** `19.0.0.0.1`
- **category:** `Administración`
- **summary:** `Registra historial de ejecuciones de cron y envía alertas a roles configurados.`
- **description:** `Registra historial de ejecuciones de cron y envía alertas a roles configurados.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `sicpro_app_administracion`

### Modelos Python

- `IrCron`
- `IrCronHistory`

### Python

- `sicpro_modulo_historial_cron/__init__.py`
- `sicpro_modulo_historial_cron/__manifest__.py`
- `sicpro_modulo_historial_cron/models/__init__.py`
- `sicpro_modulo_historial_cron/models/ir_cron.py`
- `sicpro_modulo_historial_cron/models/ir_cron_history.py`

### XML

- `sicpro_modulo_historial_cron/data/mail_template.xml`
- `sicpro_modulo_historial_cron/views/ir_cron_history_views.xml`
- `sicpro_modulo_historial_cron/views/ir_cron_views.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_historial_cron/security/ir.model.access.csv`

---

## sicpro_modulo_historial_xmlrpc

**Ruta:** `sicpro_app/sicpro_modulo_historial_xmlrpc`

### Manifest

- **name:** `SICPRO: Historial de solicitudes XMLRPC`
- **version:** `19.0.0.0.1`
- **category:** `Administración`
- **summary:** `Se encarga del registro de solicitudes XML-RPC`
- **description:** `Se encarga del registro de solicitudes XML-RPC.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `base`

### Modelos Python

- `XmlRpcLog`

### Python

- `sicpro_modulo_historial_xmlrpc/__init__.py`
- `sicpro_modulo_historial_xmlrpc/__manifest__.py`
- `sicpro_modulo_historial_xmlrpc/models/__init__.py`
- `sicpro_modulo_historial_xmlrpc/models/service.py`
- `sicpro_modulo_historial_xmlrpc/models/xml_rpc_log.py`

### XML

- `sicpro_modulo_historial_xmlrpc/views/xmlrpc_views.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_historial_xmlrpc/security/ir.model.access.csv`

---

## sicpro_modulo_imagenes

**Ruta:** `sicpro_app/sicpro_modulo_imagenes`

### Manifest

- **name:** `SICPRO: Trabajos con Imágenes`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Este módulo se encarga de expandir todo lo relacionado con las imágenes del sistema`
- **description:** `Este módulo se encarga de expandir todo lo relacionado con las imágenes del sistema`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_imagenes/__init__.py`
- `sicpro_modulo_imagenes/__manifest__.py`

### XML

- `sicpro_modulo_imagenes/static/src/xml/widget_image_preview.xml`

### JavaScript / OWL

- `sicpro_modulo_imagenes/static/src/js/image_preview_widget.js`

---

## sicpro_modulo_importar_app

**Ruta:** `sicpro_app/sicpro_modulo_importar_app`

### Manifest

- **name:** `SICPRO: Importar Aplicaciones`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite instalar módulos de SICPRO ERP directamente desde un archivo ZIP a través de la interfaz de usuario.`
- **description:** `Permite instalar módulos de SICPRO ERP directamente desde un archivo ZIP a través de la interfaz de usuario.`
- **license:** `LGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Modelos Python

- `IrModule`

### Wizards / TransientModel

- `ModuleIntegrationWizard`

### Python

- `sicpro_modulo_importar_app/__init__.py`
- `sicpro_modulo_importar_app/__manifest__.py`
- `sicpro_modulo_importar_app/manager/__init__.py`
- `sicpro_modulo_importar_app/manager/utils.py`
- `sicpro_modulo_importar_app/models/__init__.py`
- `sicpro_modulo_importar_app/models/ir_module.py`
- `sicpro_modulo_importar_app/wizard/__init__.py`
- `sicpro_modulo_importar_app/wizard/addon_import.py`

### XML

- `sicpro_modulo_importar_app/views/apps.xml`
- `sicpro_modulo_importar_app/wizard/addon_import.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_importar_app/security/ir.model.access.csv`

---

## sicpro_modulo_ldap_local

**Ruta:** `sicpro_app/sicpro_modulo_ldap_local`

### Manifest

- **name:** `SICPRO: Usuario LDAP a local`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Aplicación para crear los usuarios directamente desde el LDAP empresarial`
- **description:** `Aplicación para crear los usuarios directamente desde el LDAP empresarial`
- **license:** `LGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_modulo_ldap_query`
- `sicpro_app_administracion`

### Modelos Python

- `Users`

### Python

- `sicpro_modulo_ldap_local/__init__.py`
- `sicpro_modulo_ldap_local/__manifest__.py`
- `sicpro_modulo_ldap_local/models/__init__.py`
- `sicpro_modulo_ldap_local/models/res_users.py`

### XML

- `sicpro_modulo_ldap_local/views/res_users_view.xml`

---

## sicpro_modulo_ldap_local_clientes

**Ruta:** `sicpro_app/sicpro_modulo_ldap_local_clientes`

### Manifest

- **name:** `SICPRO: Usuario LDAP a Cliente local`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Aplicación para crear los clientes directamente desde él LDAP empresarial.`
- **description:** `Aplicación para crear los clientes directamente desde él LDAP empresarial.`
- **license:** `LGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_modulo_ldap_query`
- `sicpro_app_clientes`
- `sicpro_app_administracion`

### Modelos Python

- `AppClientes`

### Python

- `sicpro_modulo_ldap_local_clientes/__init__.py`
- `sicpro_modulo_ldap_local_clientes/__manifest__.py`
- `sicpro_modulo_ldap_local_clientes/models/__init__.py`
- `sicpro_modulo_ldap_local_clientes/models/sicpro_app_clientes.py`

### XML

- `sicpro_modulo_ldap_local_clientes/views/clientes_views.xml`

---

## sicpro_modulo_ldap_query

**Ruta:** `sicpro_app/sicpro_modulo_ldap_query`

### Manifest

- **name:** `SICPRO: Consultas Dinámicas al LDAP`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Este módulo permite la realización de consultas al ldap empresarial`
- **description:** `Este módulo permite la realización de consultas al ldap empresarial`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `base`
- `auth_ldap`
- `sicpro_modulo_ldap_ssl`
- `sicpro_app_contactos`
- `sicpro_modulo_nomencladores`

### Modelos Python

- `SicproLdapHistorial`
- `SicproLdapRegistros`

### Python

- `sicpro_modulo_ldap_query/__init__.py`
- `sicpro_modulo_ldap_query/__manifest__.py`
- `sicpro_modulo_ldap_query/models/__init__.py`
- `sicpro_modulo_ldap_query/models/sicpro_app_modulo_ldap_historial.py`
- `sicpro_modulo_ldap_query/models/sicpro_modulo_ldap_registros.py`

### XML

- `sicpro_modulo_ldap_query/data/ir_cron.xml`
- `sicpro_modulo_ldap_query/data/mail_template.xml`
- `sicpro_modulo_ldap_query/views/ldap_historial_views.xml`
- `sicpro_modulo_ldap_query/views/ldap_query_menu_views.xml`
- `sicpro_modulo_ldap_query/views/ldap_registros_views.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_ldap_query/security/ir.model.access.csv`

---

## sicpro_modulo_ldap_servicios_internos

**Ruta:** `sicpro_app/sicpro_modulo_ldap_servicios_internos`

### Manifest

- **name:** `SICPRO: LDAP a Servicios Internos`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Aplicación para actualizar los datos de los servicios internos con el LDAP empresarial`
- **description:** `Aplicación para actualizar los datos de los servicios internos con el LDAP empresaria`
- **license:** `LGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`
- `sicpro_modulo_ldap_query`
- `sicpro_app_servicios_internos`

### Modelos Python

- `ServiciosInternosCorreos`

### Python

- `sicpro_modulo_ldap_servicios_internos/__init__.py`
- `sicpro_modulo_ldap_servicios_internos/__manifest__.py`
- `sicpro_modulo_ldap_servicios_internos/models/__init__.py`
- `sicpro_modulo_ldap_servicios_internos/models/sicpro_app_internos_correos.py`

### XML

- `sicpro_modulo_ldap_servicios_internos/data/ir_cron.xml`
- `sicpro_modulo_ldap_servicios_internos/data/mail_template.xml`

---

## sicpro_modulo_ldap_ssl

**Ruta:** `sicpro_app/sicpro_modulo_ldap_ssl`

### Manifest

- **name:** `SICPRO: Conexión mediante LDAP SSL`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Este módulo permite la autentificación via ldap ssl, permitiendo la validación del certificado de seguridad`
- **description:** `Este módulo permite la autentificación via ldap ssl, permitiendo la validación del certificado de seguridad`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `base`
- `auth_ldap`

### Modelos Python

- `CompanyLDAP`

### Python

- `sicpro_modulo_ldap_ssl/__init__.py`
- `sicpro_modulo_ldap_ssl/__manifest__.py`
- `sicpro_modulo_ldap_ssl/models/__init__.py`
- `sicpro_modulo_ldap_ssl/models/res_company_ldap.py`

### XML

- `sicpro_modulo_ldap_ssl/data/res_company_ldap.xml`
- `sicpro_modulo_ldap_ssl/views/res_company_ldap_views.xml`

---

## sicpro_modulo_marcadores

**Ruta:** `sicpro_app/sicpro_modulo_marcadores`

### Manifest

- **name:** `SICPRO: Marcadores`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Crea pestaña de marcadores para agregar las vistas más utilizadas en la barra de tareas.`
- **description:** `Crea pestaña de marcadores para agregar las vistas más utilizadas en la barra de tareas.`
- **license:** `LGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `web`
- `sicpro_app_administracion`

### Modelos Python

- `MenuMarcadores`
- `ResCompany`
- `ResUsers`

### Wizards / TransientModel

- `ResConfigSettings`

### Python

- `sicpro_modulo_marcadores/__init__.py`
- `sicpro_modulo_marcadores/__manifest__.py`
- `sicpro_modulo_marcadores/controllers/__init__.py`
- `sicpro_modulo_marcadores/controllers/main.py`
- `sicpro_modulo_marcadores/models/__init__.py`
- `sicpro_modulo_marcadores/models/menu_marcadores.py`
- `sicpro_modulo_marcadores/models/res_company.py`
- `sicpro_modulo_marcadores/models/res_config_settings.py`
- `sicpro_modulo_marcadores/models/res_users.py`

### XML

- `sicpro_modulo_marcadores/static/src/components/add_bookmark/add_bookmark.xml`
- `sicpro_modulo_marcadores/static/src/components/bookmark/bookmark.xml`
- `sicpro_modulo_marcadores/static/src/components/main_menu/main_menu.xml`
- `sicpro_modulo_marcadores/static/src/components/navbar/navbar.xml`
- `sicpro_modulo_marcadores/static/src/components/widget_announcement/widget_announcement.xml`
- `sicpro_modulo_marcadores/static/src/components/widget_hour/widget_hour.xml`
- `sicpro_modulo_marcadores/static/src/webclient/navbar/navbar.xml`
- `sicpro_modulo_marcadores/views/menu_bookmark_views.xml`
- `sicpro_modulo_marcadores/views/res_config_setting_views.xml`

### JavaScript / OWL

- `sicpro_modulo_marcadores/static/src/components/add_bookmark/add_bookmark.js`
- `sicpro_modulo_marcadores/static/src/components/bookmark/bookmark.js`
- `sicpro_modulo_marcadores/static/src/components/main_menu/main_menu.js`
- `sicpro_modulo_marcadores/static/src/components/navbar/navbar.js`
- `sicpro_modulo_marcadores/static/src/components/widget_announcement/widget_announcement.js`
- `sicpro_modulo_marcadores/static/src/components/widget_hour/widget_hour.js`
- `sicpro_modulo_marcadores/static/src/webclient/navbar/navbar.js`

### CSV / Seguridad / Datos

- `sicpro_modulo_marcadores/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_modulo_marcadores/static/src/components/main_menu/main_menu.scss`
- `sicpro_modulo_marcadores/static/src/components/navbar/navbar.scss`
- `sicpro_modulo_marcadores/static/src/components/widget_announcement/widget_announcement.scss`
- `sicpro_modulo_marcadores/static/src/components/widget_hour/widget_hour.scss`
- `sicpro_modulo_marcadores/static/src/webclient/navbar/navbar.scss`

---

## sicpro_modulo_mod_avanzados

**Ruta:** `sicpro_app/sicpro_modulo_mod_avanzados`

### Manifest

- **name:** `SICPRO: Personalización Avanzada`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Este módulo permite personalizar SICPRO ERP.`
- **description:** `Este módulo permite personalizar SICPRO ERP`
- **license:** `LGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base_setup`
- `base_import`
- `base_import_module`
- `mail`
- `sicpro_app_administracion`

### Modelos Python

- `IrHttp`
- `IrModelFields`
- `IrModuleAddonsPath`
- `IrModuleModule`
- `IrUiMenu`
- `MailThread`
- `View`
- `WebEnvironmentRibbonBackend`

### Wizards / TransientModel

- `BaseModuleUpdate`
- `ResConfigSettings`

### Python

- `sicpro_modulo_mod_avanzados/__init__.py`
- `sicpro_modulo_mod_avanzados/__manifest__.py`
- `sicpro_modulo_mod_avanzados/models/__init__.py`
- `sicpro_modulo_mod_avanzados/models/ir_http.py`
- `sicpro_modulo_mod_avanzados/models/ir_model_fields.py`
- `sicpro_modulo_mod_avanzados/models/ir_module_addons_path.py`
- `sicpro_modulo_mod_avanzados/models/ir_module_module.py`
- `sicpro_modulo_mod_avanzados/models/ir_ui_menu.py`
- `sicpro_modulo_mod_avanzados/models/ir_ui_view.py`
- `sicpro_modulo_mod_avanzados/models/mail_thread.py`
- `sicpro_modulo_mod_avanzados/models/res_config_settings.py`
- `sicpro_modulo_mod_avanzados/models/web_environment_ribbon_backend.py`
- `sicpro_modulo_mod_avanzados/wizard/__init__.py`
- `sicpro_modulo_mod_avanzados/wizard/base_module_update.py`

### XML

- `sicpro_modulo_mod_avanzados/data/ir_config_parameter.xml`
- `sicpro_modulo_mod_avanzados/data/res_company.xml`
- `sicpro_modulo_mod_avanzados/static/description/switch_lang_menu/switch_lang_menu.xml`
- `sicpro_modulo_mod_avanzados/static/src/webclient/user_menu.xml`
- `sicpro_modulo_mod_avanzados/static/src/xml/debug_templates.xml`
- `sicpro_modulo_mod_avanzados/static/src/xml/res_config_edition.xml`
- `sicpro_modulo_mod_avanzados/views/app_odoo_customize_views.xml`
- `sicpro_modulo_mod_avanzados/views/ir_actions_act_window_views.xml`
- `sicpro_modulo_mod_avanzados/views/ir_model_data_views.xml`
- `sicpro_modulo_mod_avanzados/views/ir_model_fields_views.xml`
- `sicpro_modulo_mod_avanzados/views/ir_model_views.xml`
- `sicpro_modulo_mod_avanzados/views/ir_module_addons_path_views.xml`
- `sicpro_modulo_mod_avanzados/views/ir_module_category_views.xml`
- `sicpro_modulo_mod_avanzados/views/ir_module_module_views.xml`
- `sicpro_modulo_mod_avanzados/views/ir_sequence_views.xml`
- `sicpro_modulo_mod_avanzados/views/ir_ui_menu_views.xml`
- `sicpro_modulo_mod_avanzados/views/ir_ui_view_views.xml`
- `sicpro_modulo_mod_avanzados/views/ir_views.xml`
- `sicpro_modulo_mod_avanzados/views/res_config_settings_views.xml`

### JavaScript / OWL

- `sicpro_modulo_mod_avanzados/static/description/switch_lang_menu/switch_lang_menu.js`
- `sicpro_modulo_mod_avanzados/static/src/js/base_import_list_renderer.js`
- `sicpro_modulo_mod_avanzados/static/src/js/dialog.js`
- `sicpro_modulo_mod_avanzados/static/src/js/navbar.js`
- `sicpro_modulo_mod_avanzados/static/src/js/ribbon.js`
- `sicpro_modulo_mod_avanzados/static/src/js/user_menu.js`
- `sicpro_modulo_mod_avanzados/static/src/webclient/webclient.js`

### CSV / Seguridad / Datos

- `sicpro_modulo_mod_avanzados/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_modulo_mod_avanzados/static/src/scss/app.scss`
- `sicpro_modulo_mod_avanzados/static/src/scss/dialog.scss`
- `sicpro_modulo_mod_avanzados/static/src/scss/ribbon.scss`

---

## sicpro_modulo_modelo_vistas

**Ruta:** `sicpro_app/sicpro_modulo_modelo_vistas`

### Manifest

- **name:** `SICPRO: Vistas de los modelos de datos`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Este módulo permite la consulta de vistas dinámicas a los modelos de datos`
- **description:** `Este módulo permite la consulta de vistas dinámicas a los modelos de datos`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `base`

### Modelos Python

- `IrModel`

### Wizards / TransientModel

- `ModelosVistas`

### Python

- `sicpro_modulo_modelo_vistas/__init__.py`
- `sicpro_modulo_modelo_vistas/__manifest__.py`
- `sicpro_modulo_modelo_vistas/models/__init__.py`
- `sicpro_modulo_modelo_vistas/models/ir_model.py`
- `sicpro_modulo_modelo_vistas/wizard/__init__.py`
- `sicpro_modulo_modelo_vistas/wizard/modelo_vista.py`

### XML

- `sicpro_modulo_modelo_vistas/views/ir_model_view.xml`
- `sicpro_modulo_modelo_vistas/wizard/modelos_vistas_views.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_modelo_vistas/security/ir.model.access.csv`

---

## sicpro_modulo_monto_texto

**Ruta:** `sicpro_app/sicpro_modulo_monto_texto`

### Manifest

- **name:** `SICPRO: Monto a Texto`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Módulo para convertir el presupuesto a texto`
- **description:** `Módulo para convertir el presupuesto a texto`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_monto_texto/__init__.py`
- `sicpro_modulo_monto_texto/__manifest__.py`
- `sicpro_modulo_monto_texto/models/__init__.py`
- `sicpro_modulo_monto_texto/models/monto2texto.py`

---

## sicpro_modulo_nomencladores

**Ruta:** `sicpro_app/sicpro_modulo_nomencladores`

### Manifest

- **name:** `SICPRO: Nomencladores`
- **version:** `19.0.0.0.1`
- **category:** `Administración`
- **summary:** `Este módulo agrega todas las bases de nomencladores que serán utilizados`
- **description:** `Este módulo agrega todas las bases de nomencladores que serán utilizados`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `resource`
- `sicpro_app_administracion`

### Modelos Python

- `EstadosCuentasContables`
- `EstadosMeses`
- `EstadosProblemasEjecucion`
- `EstadosTerritorios`
- `EstadosTrimestres`
- `Municipality`
- `NomencladorAnios`
- `NomencladorAreasEmpresa`
- `NomencladorCentroCosto`
- `NomencladorCentroPlanificacion`
- `NomencladorDepartamentos`
- `NomencladorEmplazamientos`
- `NomencladorEspecialidad`
- `NomencladorLocales`
- `Partner`
- `State`

### Python

- `sicpro_modulo_nomencladores/__init__.py`
- `sicpro_modulo_nomencladores/__manifest__.py`
- `sicpro_modulo_nomencladores/models/__init__.py`
- `sicpro_modulo_nomencladores/models/res_municipality.py`
- `sicpro_modulo_nomencladores/models/res_partner.py`
- `sicpro_modulo_nomencladores/models/res_state.py`
- `sicpro_modulo_nomencladores/models/sicpro_nomeclador_problemas_ejecucion.py`
- `sicpro_modulo_nomencladores/models/sicpro_nomenclador_anios.py`
- `sicpro_modulo_nomencladores/models/sicpro_nomenclador_areas_empresa.py`
- `sicpro_modulo_nomencladores/models/sicpro_nomenclador_centro_costo.py`
- `sicpro_modulo_nomencladores/models/sicpro_nomenclador_centro_planificacion.py`
- `sicpro_modulo_nomencladores/models/sicpro_nomenclador_cuentas_contables.py`
- `sicpro_modulo_nomencladores/models/sicpro_nomenclador_departamento.py`
- `sicpro_modulo_nomencladores/models/sicpro_nomenclador_emplazamiento.py`
- `sicpro_modulo_nomencladores/models/sicpro_nomenclador_especialidad.py`
- `sicpro_modulo_nomencladores/models/sicpro_nomenclador_local.py`
- `sicpro_modulo_nomencladores/models/sicpro_nomenclador_meses.py`
- `sicpro_modulo_nomencladores/models/sicpro_nomenclador_territorios.py`
- `sicpro_modulo_nomencladores/models/sicpro_nomenclador_trimestre.py`

### XML

- `sicpro_modulo_nomencladores/data/res_country_state.xml`
- `sicpro_modulo_nomencladores/data/res_municipality.xml`
- `sicpro_modulo_nomencladores/data/sicpro_nomenclador_anios.xml`
- `sicpro_modulo_nomencladores/data/sicpro_nomenclador_areas_empresa.xml`
- `sicpro_modulo_nomencladores/data/sicpro_nomenclador_centro_planificacion.xml`
- `sicpro_modulo_nomencladores/data/sicpro_nomenclador_emplazamientos.xml`
- `sicpro_modulo_nomencladores/data/sicpro_nomenclador_especialidad.xml`
- `sicpro_modulo_nomencladores/data/sicpro_nomenclador_meses.xml`
- `sicpro_modulo_nomencladores/data/sicpro_nomenclador_territorios.xml`
- `sicpro_modulo_nomencladores/data/sicpro_nomenclador_trimestre.xml`
- `sicpro_modulo_nomencladores/security/security.xml`
- `sicpro_modulo_nomencladores/views/anios_views.xml`
- `sicpro_modulo_nomencladores/views/areas_empresa_views.xml`
- `sicpro_modulo_nomencladores/views/centro_costo_views.xml`
- `sicpro_modulo_nomencladores/views/centro_planificacion_views.xml`
- `sicpro_modulo_nomencladores/views/cuentas_contables_views.xml`
- `sicpro_modulo_nomencladores/views/departamentos_views.xml`
- `sicpro_modulo_nomencladores/views/emplazamiento_views.xml`
- `sicpro_modulo_nomencladores/views/especialidades.views.xml`
- `sicpro_modulo_nomencladores/views/locales_cc_views.xml`
- `sicpro_modulo_nomencladores/views/meses_views.xml`
- `sicpro_modulo_nomencladores/views/nomencladores_views.xml`
- `sicpro_modulo_nomencladores/views/res_municipality.xml`
- `sicpro_modulo_nomencladores/views/res_state.xml`
- `sicpro_modulo_nomencladores/views/territorios_views.xml`
- `sicpro_modulo_nomencladores/views/trimestres_views.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_nomencladores/security/ir.model.access.csv`

---

## sicpro_modulo_nomencladores_iconos

**Ruta:** `sicpro_app/sicpro_modulo_nomencladores_iconos`

### Manifest

- **name:** `SICPRO: Nomenclador de Iconos`
- **version:** `19.0.0.0.1`
- **category:** `Administración`
- **summary:** `Este módulo agrega la vista de los nomencladores de iconos`
- **description:** `Este módulo agrega la vista de los nomencladores de iconos`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`
- `sicpro_modulo_nomencladores`

### Modelos Python

- `NomencladorIconos`

### Python

- `sicpro_modulo_nomencladores_iconos/__init__.py`
- `sicpro_modulo_nomencladores_iconos/__manifest__.py`
- `sicpro_modulo_nomencladores_iconos/models/__init__.py`
- `sicpro_modulo_nomencladores_iconos/models/sicpro_nomenclador_iconos.py`

### XML

- `sicpro_modulo_nomencladores_iconos/data/sicpro_nomenclador_iconos_fa.xml`
- `sicpro_modulo_nomencladores_iconos/data/sicpro_nomenclador_iconos_fab.xml`
- `sicpro_modulo_nomencladores_iconos/data/sicpro_nomenclador_iconos_far.xml`
- `sicpro_modulo_nomencladores_iconos/data/sicpro_nomenclador_iconos_fas.xml`
- `sicpro_modulo_nomencladores_iconos/views/iconos_views.xml`
- `sicpro_modulo_nomencladores_iconos/views/nomencladores_menu_views.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_nomencladores_iconos/security/ir.model.access.csv`

---

## sicpro_modulo_nomencladores_sindicato

**Ruta:** `sicpro_app/sicpro_modulo_nomencladores_sindicato`

### Manifest

- **name:** `SICPRO: Nomenclador del sindicato`
- **version:** `19.0.0.0.1`
- **category:** `Administración`
- **summary:** `Este módulo agrega todas las bases del nomenclador de las secciones sindicales de la DVPE`
- **description:** `Este módulo agrega todas las bases del nomenclador de las secciones sindicales de la DVPE`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`
- `sicpro_app_trabajadores`
- `sicpro_modulo_nomencladores`

### Modelos Python

- `Departamentos`
- `NomencladorSindicato`
- `TrabajadoresGeneral`

### Python

- `sicpro_modulo_nomencladores_sindicato/__init__.py`
- `sicpro_modulo_nomencladores_sindicato/__manifest__.py`
- `sicpro_modulo_nomencladores_sindicato/models/__init__.py`
- `sicpro_modulo_nomencladores_sindicato/models/sicpro_app_trabajadores.py`
- `sicpro_modulo_nomencladores_sindicato/models/sicpro_app_trabajadores_areas.py`
- `sicpro_modulo_nomencladores_sindicato/models/sicpro_nomenclador_sindicato.py`

### XML

- `sicpro_modulo_nomencladores_sindicato/views/nomencladores_menu_views.xml`
- `sicpro_modulo_nomencladores_sindicato/views/sindicato_views.xml`
- `sicpro_modulo_nomencladores_sindicato/views/trabajadores_areas_views.xml`
- `sicpro_modulo_nomencladores_sindicato/views/trabajadores_views.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_nomencladores_sindicato/security/ir.model.access.csv`

---

## sicpro_modulo_panel_busqueda

**Ruta:** `sicpro_app/sicpro_modulo_panel_busqueda`

### Manifest

- **name:** `SICPRO: Barra Lateral de Búsqueda`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Barra Lateral de Búsqueda`
- **description:** `Barra Lateral de Búsqueda`
- **license:** `LGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_panel_busqueda/__init__.py`
- `sicpro_modulo_panel_busqueda/__manifest__.py`

### XML

- `sicpro_modulo_panel_busqueda/static/src/xml/search_panel_toggle.xml`
- `sicpro_modulo_panel_busqueda/views/ir_actions_act_window_views.xml`
- `sicpro_modulo_panel_busqueda/views/ir_actions_actions_views.xml`
- `sicpro_modulo_panel_busqueda/views/ir_actions_report_views.xml`
- `sicpro_modulo_panel_busqueda/views/ir_actions_server_views.xml`
- `sicpro_modulo_panel_busqueda/views/ir_attachment_views.xml`
- `sicpro_modulo_panel_busqueda/views/ir_default_views.xml`
- `sicpro_modulo_panel_busqueda/views/ir_model_access_views.xml`
- `sicpro_modulo_panel_busqueda/views/ir_model_constraint_views.xml`
- `sicpro_modulo_panel_busqueda/views/ir_model_fields_views.xml`
- `sicpro_modulo_panel_busqueda/views/ir_ui_menu_views.xml`
- `sicpro_modulo_panel_busqueda/views/ir_ui_view_views.xml`
- `sicpro_modulo_panel_busqueda/views/res_groups_views.xml`

### JavaScript / OWL

- `sicpro_modulo_panel_busqueda/static/src/js/search_panel_toggle.js`

### CSS / SCSS

- `sicpro_modulo_panel_busqueda/static/src/css/search_panel_toggle.scss`

---

## sicpro_modulo_paquetes_python

**Ruta:** `sicpro_app/sicpro_modulo_paquetes_python`

### Manifest

- **name:** `SICPRO: Paquetes Python`
- **version:** `19.0.0.1`
- **category:** `Administración`
- **summary:** `Módulo para visualizar los paquetes de python instalados en el servidor`
- **description:** `Módulo para visualizar los paquetes de python instalados en el servidor`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `PythonPaquetesInstalados`

### Wizards / TransientModel

- `ResConfigSettings`

### Python

- `sicpro_modulo_paquetes_python/__init__.py`
- `sicpro_modulo_paquetes_python/__manifest__.py`
- `sicpro_modulo_paquetes_python/models/__init__.py`
- `sicpro_modulo_paquetes_python/models/res_config_settings.py`
- `sicpro_modulo_paquetes_python/models/sicpro_modulo_paquetes_python.py`

### XML

- `sicpro_modulo_paquetes_python/views/res_config_view.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_paquetes_python/security/ir.model.access.csv`

---

## sicpro_modulo_querydb

**Ruta:** `sicpro_app/sicpro_modulo_querydb`

### Manifest

- **name:** `SICPRO: Base de Datos Query`
- **version:** `19.0.0.1`
- **category:** `Administración`
- **summary:** `Permite el acceso a las bases de datos PostgreSQL mediantes consulta query`
- **description:** `Permite el acceso a las bases de datos PostgreSQL mediantes consulta query`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `sicpro_app_administracion`

### Modelos Python

- `QueryDeluxe`

### Wizards / TransientModel

- `PdfOrientation`

### Python

- `sicpro_modulo_querydb/__init__.py`
- `sicpro_modulo_querydb/__manifest__.py`
- `sicpro_modulo_querydb/models/__init__.py`
- `sicpro_modulo_querydb/models/querydeluxe.py`
- `sicpro_modulo_querydb/wizard/__init__.py`
- `sicpro_modulo_querydb/wizard/pdforientation.py`

### XML

- `sicpro_modulo_querydb/data/querydeluxe.xml`
- `sicpro_modulo_querydb/report/print_pdf.xml`
- `sicpro_modulo_querydb/security/security.xml`
- `sicpro_modulo_querydb/views/querydeluxe.xml`
- `sicpro_modulo_querydb/wizard/pdforientation.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_querydb/security/ir.model.access.csv`

---

## sicpro_modulo_roles

**Ruta:** `sicpro_app/sicpro_modulo_roles`

### Manifest

- **name:** `SICPRO: Roles`
- **version:** `19.0.0.0.1`
- **category:** `Administration`
- **summary:** `Gestiona los roles de accesos de los usuarios del sistema`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`

### Modelos Python

- `ResGroups`
- `ResUsers`
- `ResUsersRole`
- `ResUsersRoleLine`

### Wizards / TransientModel

- `GroupGroupsIntoRole`
- `WizardCreateRoleFromUser`

### Python

- `sicpro_modulo_roles/__init__.py`
- `sicpro_modulo_roles/__manifest__.py`
- `sicpro_modulo_roles/models/__init__.py`
- `sicpro_modulo_roles/models/res_groups.py`
- `sicpro_modulo_roles/models/role.py`
- `sicpro_modulo_roles/models/user.py`
- `sicpro_modulo_roles/wizards/__init__.py`
- `sicpro_modulo_roles/wizards/create_from_user.py`
- `sicpro_modulo_roles/wizards/wizard_groups_into_role.py`

### XML

- `sicpro_modulo_roles/data/ir_cron.xml`
- `sicpro_modulo_roles/data/ir_module_category.xml`
- `sicpro_modulo_roles/views/group.xml`
- `sicpro_modulo_roles/views/role.xml`
- `sicpro_modulo_roles/views/user.xml`
- `sicpro_modulo_roles/wizards/create_from_user.xml`
- `sicpro_modulo_roles/wizards/wizard_groups_into_role.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_roles/security/ir.model.access.csv`

---

## sicpro_modulo_sequence_romanos

**Ruta:** `sicpro_app/sicpro_modulo_sequence_romanos`

### Manifest

- **name:** `SICPRO: Secuencias con romanos`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite la opción que la secuencia la de en números romanos.`
- **description:** `Permite la opción que la secuencia la de en números romanos.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `IrSequence`

### Python

- `sicpro_modulo_sequence_romanos/__init__.py`
- `sicpro_modulo_sequence_romanos/__manifest__.py`
- `sicpro_modulo_sequence_romanos/models/__init__.py`
- `sicpro_modulo_sequence_romanos/models/ir_sequence.py`

### XML

- `sicpro_modulo_sequence_romanos/views/ir_sequence_views.xml`

---

## sicpro_modulo_servidor_info

**Ruta:** `sicpro_app/sicpro_modulo_servidor_info`

### Manifest

- **name:** `SICPRO: Servidor Info`
- **version:** `19.0.0.0.1`
- **category:** `Administración`
- **summary:** `Módulo para controlar los principales parámetros de uso del servidor del sistema SICPRO ERP`
- **description:** `Módulo para controlar los principales parámetros de uso del servidor del sistema SICPRO ERP`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `IrHttp`

### Wizards / TransientModel

- `ServerInfoSettings`

### Python

- `sicpro_modulo_servidor_info/__init__.py`
- `sicpro_modulo_servidor_info/__manifest__.py`
- `sicpro_modulo_servidor_info/models/__init__.py`
- `sicpro_modulo_servidor_info/models/server_info.py`

### XML

- `sicpro_modulo_servidor_info/.idea/inspectionProfiles/profiles_settings.xml`
- `sicpro_modulo_servidor_info/.idea/misc.xml`
- `sicpro_modulo_servidor_info/.idea/modules.xml`
- `sicpro_modulo_servidor_info/.idea/vcs.xml`
- `sicpro_modulo_servidor_info/static/src/components/server_info/auto_update.xml`
- `sicpro_modulo_servidor_info/views/fields.xml`

### JavaScript / OWL

- `sicpro_modulo_servidor_info/static/src/components/server_info/auto_update.js`

---

## sicpro_modulo_tema_agrupar

**Ruta:** `sicpro_app/sicpro_modulo_tema_agrupar`

### Manifest

- **name:** `SICPRO: Expande/Contrae grupos`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Le permite expandir y contraer grupos creados y agrupar los datos por un determinado campo para vistas de lista y kanban.`
- **description:** `Le permite expandir y contraer grupos creados y agrupar los datos por un determinado campo para vistas de lista y kanban.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_tema_agrupar/__init__.py`
- `sicpro_modulo_tema_agrupar/__manifest__.py`

### XML

- `sicpro_modulo_tema_agrupar/static/src/search/collapse_all/collapse_all.xml`
- `sicpro_modulo_tema_agrupar/static/src/search/expand_all/expand_all.xml`

### JavaScript / OWL

- `sicpro_modulo_tema_agrupar/static/src/search/collapse_all/collapse_all.js`
- `sicpro_modulo_tema_agrupar/static/src/search/expand_all/expand_all.js`

---

## sicpro_modulo_tema_auto_actualizar

**Ruta:** `sicpro_app/sicpro_modulo_tema_auto_actualizar`

### Manifest

- **name:** `SICPRO: Actualizar vistas`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Actualizar automáticamente vistas de lista o kanban`
- **description:** `Active el botón de actualización automática para recargar la vista cada30 segundos. La actualización recargará y actualizará los datos de la vista.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Modelos Python

- `IrHttp`

### Python

- `sicpro_modulo_tema_auto_actualizar/__init__.py`
- `sicpro_modulo_tema_auto_actualizar/__manifest__.py`
- `sicpro_modulo_tema_auto_actualizar/models/__init__.py`
- `sicpro_modulo_tema_auto_actualizar/models/ir_http.py`

### XML

- `sicpro_modulo_tema_auto_actualizar/static/src/search/control_panel.xml`

### JavaScript / OWL

- `sicpro_modulo_tema_auto_actualizar/static/src/search/control_panel.js`

---

## sicpro_modulo_tema_barra

**Ruta:** `sicpro_app/sicpro_modulo_tema_barra`

### Manifest

- **name:** `SICPRO: Barra de aplicaciones`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Agrega una barra lateral a la pantalla principal.`
- **description:** `Este módulo agrega una barra lateral a la pantalla principal. La barra lateral tiene una listade todas las aplicaciones instaladas.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `base_setup`
- `web`
- `sicpro_app_administracion`

### Modelos Python

- `ResUsers`

### Python

- `sicpro_modulo_tema_barra/__init__.py`
- `sicpro_modulo_tema_barra/__manifest__.py`
- `sicpro_modulo_tema_barra/models/__init__.py`
- `sicpro_modulo_tema_barra/models/res_users.py`

### XML

- `sicpro_modulo_tema_barra/static/src/webclient/appsbar/appsbar.xml`
- `sicpro_modulo_tema_barra/static/src/webclient/webclient.xml`
- `sicpro_modulo_tema_barra/templates/webclient.xml`
- `sicpro_modulo_tema_barra/views/res_users.xml`

### JavaScript / OWL

- `sicpro_modulo_tema_barra/static/src/webclient/appsbar/appsbar.js`
- `sicpro_modulo_tema_barra/static/src/webclient/menus/app_menu_service.js`
- `sicpro_modulo_tema_barra/static/src/webclient/webclient.js`

### CSS / SCSS

- `sicpro_modulo_tema_barra/static/src/scss/mixins.scss`
- `sicpro_modulo_tema_barra/static/src/scss/variables.dark.scss`
- `sicpro_modulo_tema_barra/static/src/scss/variables.scss`
- `sicpro_modulo_tema_barra/static/src/webclient/appsbar/appsbar.scss`
- `sicpro_modulo_tema_barra/static/src/webclient/webclient.scss`

---

## sicpro_modulo_tema_chatter

**Ruta:** `sicpro_app/sicpro_modulo_tema_chatter`

### Manifest

- **name:** `SICPRO: Chatter`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite seleccionar la posición donde desea el chatter.`
- **description:** `Permite seleccionar la posición donde desea el chatter.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `mail`
- `sicpro_app_administracion`

### Modelos Python

- `ResUsers`

### Python

- `sicpro_modulo_tema_chatter/__init__.py`
- `sicpro_modulo_tema_chatter/__manifest__.py`
- `sicpro_modulo_tema_chatter/models/__init__.py`
- `sicpro_modulo_tema_chatter/models/res_users.py`

### XML

- `sicpro_modulo_tema_chatter/views/res_users_views.xml`
- `sicpro_modulo_tema_chatter/views/web.xml`

### JavaScript / OWL

- `sicpro_modulo_tema_chatter/static/src/js/web_chatter_position.esm.js`

### CSS / SCSS

- `sicpro_modulo_tema_chatter/static/src/scss/chatter_custom.scss`

---

## sicpro_modulo_tema_colores

**Ruta:** `sicpro_app/sicpro_modulo_tema_colores`

### Manifest

- **name:** `SICPRO: Colores`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Personaliza los colores de SICPRO ERP`
- **description:** `Este módulo le ofrece opciones para personalizar los colores del tema.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `base_setup`
- `sicpro_app_administracion`

### Modelos Python

- `ColorAssetsEditor`

### Wizards / TransientModel

- `ResConfigSettings`

### Python

- `sicpro_modulo_tema_colores/__init__.py`
- `sicpro_modulo_tema_colores/__manifest__.py`
- `sicpro_modulo_tema_colores/models/__init__.py`
- `sicpro_modulo_tema_colores/models/color_assets_editor.py`
- `sicpro_modulo_tema_colores/models/res_config_settings.py`

### XML

- `sicpro_modulo_tema_colores/templates/webclient.xml`
- `sicpro_modulo_tema_colores/views/res_config_settings.xml`

### CSS / SCSS

- `sicpro_modulo_tema_colores/static/src/scss/colors.scss`
- `sicpro_modulo_tema_colores/static/src/scss/colors_dark.scss`
- `sicpro_modulo_tema_colores/static/src/scss/colors_light.scss`

---

## sicpro_modulo_tema_dialogos

**Ruta:** `sicpro_app/sicpro_modulo_tema_dialogos`

### Manifest

- **name:** `SICPRO: Cuadros de diálogos Wizard`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Agrega opciones para los diálogos.`
- **description:** `Este módulo agrega una opción a los cuadros de diálogo para expandirlos al modo de pantalla completa.Cada usuario puede consultar el estado inicial de los diálogos en sus preferencias.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Modelos Python

- `IrHttp`
- `ResUsers`

### Python

- `sicpro_modulo_tema_dialogos/__init__.py`
- `sicpro_modulo_tema_dialogos/__manifest__.py`
- `sicpro_modulo_tema_dialogos/models/__init__.py`
- `sicpro_modulo_tema_dialogos/models/ir_http.py`
- `sicpro_modulo_tema_dialogos/models/res_users.py`

### XML

- `sicpro_modulo_tema_dialogos/static/src/core/dialog/dialog.xml`
- `sicpro_modulo_tema_dialogos/views/res_users.xml`

### JavaScript / OWL

- `sicpro_modulo_tema_dialogos/static/src/core/dialog/dialog.js`
- `sicpro_modulo_tema_dialogos/static/src/views/view_dialogs/select_create_dialog.js`

### CSS / SCSS

- `sicpro_modulo_tema_dialogos/static/src/core/dialog/dialog.scss`
- `sicpro_modulo_tema_dialogos/static/src/scss/variables.scss`

---

## sicpro_modulo_tema_favicon

**Ruta:** `sicpro_app/sicpro_modulo_tema_favicon`

### Manifest

- **name:** `SICPRO: Favicon`
- **version:** `19.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite incorporar el icono del sistema SICPRO ERP`
- **description:** `Permite incorporar el icono del sistema SICPRO ERP`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `web`
- `sicpro_app_administracion`

### Modelos Python

- `ResCompany`

### Python

- `sicpro_modulo_tema_favicon/__init__.py`
- `sicpro_modulo_tema_favicon/__manifest__.py`
- `sicpro_modulo_tema_favicon/models/__init__.py`
- `sicpro_modulo_tema_favicon/models/res_company.py`

### XML

- `sicpro_modulo_tema_favicon/data/res_company.xml`
- `sicpro_modulo_tema_favicon/views/res_company_views.xml`
- `sicpro_modulo_tema_favicon/views/templates.xml`

---

## sicpro_modulo_tema_visual

**Ruta:** `sicpro_app/sicpro_modulo_tema_visual`

### Manifest

- **name:** `SICPRO: Tema Visual`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Opciones del tema visual`
- **description:** `Este módulo ofrece un diseño compatible con dispositivos móviles para SICPRO ERP. Además, permite al usuario definir algunas preferencias de diseño.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`
- `sicpro_modulo_tema_agrupar`
- `sicpro_modulo_tema_chatter`
- `sicpro_modulo_tema_dialogos`
- `sicpro_modulo_tema_barra`
- `sicpro_modulo_tema_colores`
- `sicpro_modulo_tema_auto_actualizar`
- `sicpro_modulo_tema_favicon`

### Modelos Python

- `IrHttp`

### Wizards / TransientModel

- `ResConfigSettings`

### Python

- `sicpro_modulo_tema_visual/__init__.py`
- `sicpro_modulo_tema_visual/__manifest__.py`
- `sicpro_modulo_tema_visual/models/__init__.py`
- `sicpro_modulo_tema_visual/models/ir_http.py`
- `sicpro_modulo_tema_visual/models/res_config_settings.py`

### XML

- `sicpro_modulo_tema_visual/static/src/template/template_circulo_color.xml`
- `sicpro_modulo_tema_visual/static/src/webclient/navbar/navbar.xml`
- `sicpro_modulo_tema_visual/views/res_config_settings.xml`

### JavaScript / OWL

- `sicpro_modulo_tema_visual/static/src/webclient/appsmenu/appsmenu.js`
- `sicpro_modulo_tema_visual/static/src/webclient/navbar/navbar.js`

### CSS / SCSS

- `sicpro_modulo_tema_visual/static/src/scss/colors.scss`
- `sicpro_modulo_tema_visual/static/src/scss/variables.scss`
- `sicpro_modulo_tema_visual/static/src/views/form/form.scss`
- `sicpro_modulo_tema_visual/static/src/webclient/appsmenu/appsmenu.scss`
- `sicpro_modulo_tema_visual/static/src/webclient/navbar/navbar.scss`

---

## sicpro_modulo_test_desarrollo

**Ruta:** `sicpro_app/sicpro_modulo_test_desarrollo`

### Manifest

- **name:** `SICPRO: Test para Desarrollo`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Módulo para facilitar la prueba de funciones`
- **description:** `Módulo para facilitar la prueba de funciones`
- **license:** `LGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `SicproException`
- `SicproTest`

### Python

- `sicpro_modulo_test_desarrollo/__init__.py`
- `sicpro_modulo_test_desarrollo/__manifest__.py`
- `sicpro_modulo_test_desarrollo/models/__init__.py`
- `sicpro_modulo_test_desarrollo/models/sicpro_modulo_exception.py`
- `sicpro_modulo_test_desarrollo/models/sicpro_modulo_test.py`

### XML

- `sicpro_modulo_test_desarrollo/security/security.xml`
- `sicpro_modulo_test_desarrollo/views/test_excepciones_view.xml`
- `sicpro_modulo_test_desarrollo/views/test_views.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_test_desarrollo/security/ir.model.access.csv`

---

## sicpro_modulo_timeout

**Ruta:** `sicpro_app/sicpro_modulo_timeout`

### Manifest

- **name:** `SICPRO: Timeout`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `El módulo se encarga de cerrar la session después del tiempo predeterminado por la configuración`
- **description:** `El módulo se encarga de cerrar la session después del tiempo predeterminado por la configuración`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`

### Modelos Python

- `IrConfigParameter`
- `IrHttp`
- `ResUsers`

### Python

- `sicpro_modulo_timeout/__init__.py`
- `sicpro_modulo_timeout/__manifest__.py`
- `sicpro_modulo_timeout/models/__init__.py`
- `sicpro_modulo_timeout/models/ir_config_parameter.py`
- `sicpro_modulo_timeout/models/ir_http.py`
- `sicpro_modulo_timeout/models/res_users.py`

### XML

- `sicpro_modulo_timeout/data/ir_config_parameter.xml`

---

## sicpro_modulo_url_sicproerp

**Ruta:** `sicpro_app/sicpro_modulo_url_sicproerp`

### Manifest

- **name:** `SICPRO: Url SICPRO`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Modifica la url de SICPRO ERP`
- **description:** `Modifica la url de SICPRO ERP`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Modelos Python

- `IrConfigParameter`

### Python

- `sicpro_modulo_url_sicproerp/__init__.py`
- `sicpro_modulo_url_sicproerp/__manifest__.py`
- `sicpro_modulo_url_sicproerp/models/__init__.py`
- `sicpro_modulo_url_sicproerp/models/url.py`

### XML

- `sicpro_modulo_url_sicproerp/data/ir_config_parameter.xml`
- `sicpro_modulo_url_sicproerp/views/ir_config_parameter_views.xml`

### JavaScript / OWL

- `sicpro_modulo_url_sicproerp/static/src/views/web_url_view_ir_config_inherit_form.js`

---

## sicpro_modulo_usuario_desactivar

**Ruta:** `sicpro_app/sicpro_modulo_usuario_desactivar`

### Manifest

- **name:** `SICPRO: Desactivar Usuarios`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Aplicación para la desactivación del usuario del sistema, mediante reglas de controles de accesos y LDAP empresarial`
- **description:** `Aplicación para la desactivación del usuario del sistema, mediante reglas de controles de accesos y LDAP empresarial`
- **license:** `LGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `sicpro_app_administracion`
- `sicpro_modulo_ldap_query`
- `sicpro_app_soporte`
- `sicpro_modulo_roles`

### Modelos Python

- `DesactivarUsersRoles`
- `DesactivarUsuario`
- `DesactivarUsuarioDias`
- `PlantillaSoporteBitacora`

### Python

- `sicpro_modulo_usuario_desactivar/__init__.py`
- `sicpro_modulo_usuario_desactivar/__manifest__.py`
- `sicpro_modulo_usuario_desactivar/models/__init__.py`
- `sicpro_modulo_usuario_desactivar/models/roles.py`
- `sicpro_modulo_usuario_desactivar/models/sicpro_app_soporte_bitacora.py`
- `sicpro_modulo_usuario_desactivar/models/sicpro_modulo_usuario_desactivar.py`
- `sicpro_modulo_usuario_desactivar/models/sicpro_modulo_usuario_desactivar_dias.py`

### XML

- `sicpro_modulo_usuario_desactivar/data/ir_cron.xml`
- `sicpro_modulo_usuario_desactivar/data/mail_template.xml`
- `sicpro_modulo_usuario_desactivar/data/sicpro_app_modulo_usuario_desactivar.xml`
- `sicpro_modulo_usuario_desactivar/views/roles_views.xml`
- `sicpro_modulo_usuario_desactivar/views/solicitud_bitacora_views.xml`
- `sicpro_modulo_usuario_desactivar/views/usuario_desactivar_menu_views.xml`
- `sicpro_modulo_usuario_desactivar/views/usuario_desactivar_views.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_usuario_desactivar/security/ir.model.access.csv`

---

## sicpro_modulo_usuario_registro

**Ruta:** `sicpro_app/sicpro_modulo_usuario_registro`

### Manifest

- **name:** `SICPRO: Registros de Usuario`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Detalles del usuario de inicio de sesión y dirección IP`
- **description:** `Este módulo registra la información de inicio de sesión del usuario`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Modelos Python

- `LoginRegistroUsuario`
- `LoginUserReport`
- `LoginUsuarios`
- `RegistroIP`
- `RegistroMAC`
- `RegistroUsuarios`

### Wizards / TransientModel

- `PassUserBackup`

### Python

- `sicpro_modulo_usuario_registro/__init__.py`
- `sicpro_modulo_usuario_registro/__manifest__.py`
- `sicpro_modulo_usuario_registro/controllers/__init__.py`
- `sicpro_modulo_usuario_registro/controllers/main.py`
- `sicpro_modulo_usuario_registro/models/__init__.py`
- `sicpro_modulo_usuario_registro/models/sicpro_modulo_registro_ips.py`
- `sicpro_modulo_usuario_registro/models/sicpro_modulo_registro_reporte.py`
- `sicpro_modulo_usuario_registro/models/sicpro_modulo_registro_usuarios.py`
- `sicpro_modulo_usuario_registro/wizard/__init__.py`
- `sicpro_modulo_usuario_registro/wizard/pass_user_backup_wizard.py`

### XML

- `sicpro_modulo_usuario_registro/data/mail_template.xml`
- `sicpro_modulo_usuario_registro/views/registro_ips_view.xml`
- `sicpro_modulo_usuario_registro/views/registro_usuarios_reporte.xml`
- `sicpro_modulo_usuario_registro/views/registro_usuarios_reporte_template.xml`
- `sicpro_modulo_usuario_registro/views/registro_usuarios_reporte_wizard.xml`
- `sicpro_modulo_usuario_registro/views/registro_usuarios_views.xml`
- `sicpro_modulo_usuario_registro/views/res_user_views.xml`
- `sicpro_modulo_usuario_registro/wizard/pass_user_backup_wizard_views.xml`

### CSV / Seguridad / Datos

- `sicpro_modulo_usuario_registro/security/ir.model.access.csv`

---

## sicpro_modulo_usuario_simular

**Ruta:** `sicpro_app/sicpro_modulo_usuario_simular`

### Manifest

- **name:** `SICPRO: Simulación de Usuarios`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Aplicación para simulación de sesión`
- **description:** `Aplicación para simulación de sesión de los usuarios`
- **license:** `LGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Modelos Python

- `ResGroups`
- `UserSelection`

### Python

- `sicpro_modulo_usuario_simular/__init__.py`
- `sicpro_modulo_usuario_simular/__manifest__.py`
- `sicpro_modulo_usuario_simular/controllers/__init__.py`
- `sicpro_modulo_usuario_simular/controllers/login_as_any_user.py`
- `sicpro_modulo_usuario_simular/models/__init__.py`
- `sicpro_modulo_usuario_simular/models/res_groups.py`
- `sicpro_modulo_usuario_simular/models/user_selection.py`
- `sicpro_modulo_usuario_simular/session.py`

### XML

- `sicpro_modulo_usuario_simular/static/src/xml/systray_button_templates.xml`
- `sicpro_modulo_usuario_simular/views/user_selection_views.xml`

### JavaScript / OWL

- `sicpro_modulo_usuario_simular/static/src/js/systray_button.js`

### CSV / Seguridad / Datos

- `sicpro_modulo_usuario_simular/security/ir.model.access.csv`

---

## sicpro_modulo_vista_lista_ancho

**Ruta:** `sicpro_app/sicpro_modulo_vista_lista_ancho`

### Manifest

- **name:** `SICPRO: Ancho de Columnas`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite recordar el ancho que se le da a las columnas en la vista de lista`
- **description:** `Permite recordar el ancho que se le da a las columnas en la vista de lista`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_vista_lista_ancho/__init__.py`
- `sicpro_modulo_vista_lista_ancho/__manifest__.py`

### JavaScript / OWL

- `sicpro_modulo_vista_lista_ancho/static/src/js/list_renderer.esm.js`

### CSS / SCSS

- `sicpro_modulo_vista_lista_ancho/static/src/scss/main.scss`

---

## sicpro_modulo_vistas_split

**Ruta:** `sicpro_app/sicpro_modulo_vistas_split`

### Manifest

- **name:** `SICPRO: Vistas Split`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite a los usuarios ver la lista y la vista de formulario de un registro seleccionado en paralelo. Admite diseños divididos horizontales y verticales.`
- **description:** `Permite a los usuarios ver la lista y la vista de formulario de un registro seleccionado en paralelo. Admite diseños divididos horizontales y verticales.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_vistas_split/__init__.py`
- `sicpro_modulo_vistas_split/__manifest__.py`

### XML

- `sicpro_modulo_vistas_split/static/src/xml/split_view.xml`

### JavaScript / OWL

- `sicpro_modulo_vistas_split/static/src/js/split_view_controller.js`

### CSS / SCSS

- `sicpro_modulo_vistas_split/static/src/scss/split_view.scss`

---

## sicpro_modulo_web

**Ruta:** `sicpro_app/sicpro_modulo_web`

### Manifest

- **name:** `SICPRO: Web Página Inicial`
- **version:** `19.0.0.0.1`
- **category:** `Website`
- **summary:** `Muestra la pagina informativa inicial para SICPRO ERP`
- **description:** `Muestra la pagina informativa inicial para SICPRO ERP`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `base_setup`
- `web`
- `sicpro_modulo_nomencladores_iconos`
- `sicpro_app_administracion`
- `sicpro_app_trabajadores`
- `sicpro_app_solicitudes`
- `sicpro_app_ordenes_trabajo`
- `sicpro_app_transferencias_gastos`

### Modelos Python

- `SicproWebAvisoMantenimiento`
- `SicproWebEquipo`
- `SicproWebEvolution`
- `SicproWebFAQ`
- `SicproWebGaleria`
- `SicproWebManuales`
- `SicproWebTrabajadores`
- `SicproWebVersion`
- `SicproWebVersionLine`

### Python

- `sicpro_modulo_web/__init__.py`
- `sicpro_modulo_web/__manifest__.py`
- `sicpro_modulo_web/controllers/__init__.py`
- `sicpro_modulo_web/controllers/mail.py`
- `sicpro_modulo_web/controllers/main.py`
- `sicpro_modulo_web/models/__init__.py`
- `sicpro_modulo_web/models/sicpro_modulo_web_aviso_mantenimiento.py`
- `sicpro_modulo_web/models/sicpro_modulo_web_equipo.py`
- `sicpro_modulo_web/models/sicpro_modulo_web_evolucion.py`
- `sicpro_modulo_web/models/sicpro_modulo_web_galeria.py`
- `sicpro_modulo_web/models/sicpro_modulo_web_manuales.py`
- `sicpro_modulo_web/models/sicpro_modulo_web_preguntas.py`
- `sicpro_modulo_web/models/sicpro_modulo_web_trabajadores.py`
- `sicpro_modulo_web/models/sicpro_modulo_web_version.py`

### XML

- `sicpro_modulo_web/data/sicpro_modulo_web_aviso_mantenimiento.xml`
- `sicpro_modulo_web/templates/inicio_template.xml`
- `sicpro_modulo_web/views/aviso_mantenimiento_views.xml`
- `sicpro_modulo_web/views/equipo_views.xml`
- `sicpro_modulo_web/views/evolucion_views.xml`
- `sicpro_modulo_web/views/galerias_views.xml`
- `sicpro_modulo_web/views/manuales_views.xml`
- `sicpro_modulo_web/views/modulo_web_menu_views.xml`
- `sicpro_modulo_web/views/preguntas_views.xml`
- `sicpro_modulo_web/views/trabajadores_views.xml`
- `sicpro_modulo_web/views/version_views.xml`

### JavaScript / OWL

- `sicpro_modulo_web/static/src/js/aos.js`
- `sicpro_modulo_web/static/src/js/bootstrap.bundle.min.js`
- `sicpro_modulo_web/static/src/js/directorio.js`

### CSV / Seguridad / Datos

- `sicpro_modulo_web/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_modulo_web/static/src/css/animacion.css`
- `sicpro_modulo_web/static/src/css/aos.css`
- `sicpro_modulo_web/static/src/css/style.css`

---

## sicpro_modulo_web_base_datos

**Ruta:** `sicpro_app/sicpro_modulo_web_base_datos`

### Manifest

- **name:** `SICPRO: Web Gestor de Base de Datos`
- **version:** `19.0.0.0.1`
- **category:** `Website`
- **summary:** `Se encarga de gestionar el proceso de salva y restaura del sistema SICPRO ERP.`
- **description:** `Se encarga de gestionar el proceso de salva y restaura del sistema SICPRO ERP.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `base`
- `web`

### Python

- `sicpro_modulo_web_base_datos/__init__.py`
- `sicpro_modulo_web_base_datos/__manifest__.py`
- `sicpro_modulo_web_base_datos/controllers/__init__.py`
- `sicpro_modulo_web_base_datos/controllers/database.py`

### XML

- `sicpro_modulo_web_base_datos/views/web_base_datos.xml`

---

## sicpro_modulo_web_catalogo

**Ruta:** `sicpro_app/sicpro_modulo_web_catalogo`

### Manifest

- **name:** `SICPRO: Catálogo Público de Módulos`
- **version:** `19.0.0.0.1`
- **category:** `Website`
- **summary:** `Portal público y transparente del ecosistema de aplicaciones instaladas en SICPRO ERP`
- **description:** `Portal público y transparente del ecosistema de aplicaciones instaladas en SICPRO ERP`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_modulo_web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_web_catalogo/__init__.py`
- `sicpro_modulo_web_catalogo/__manifest__.py`
- `sicpro_modulo_web_catalogo/controllers/__init__.py`
- `sicpro_modulo_web_catalogo/controllers/main.py`

### XML

- `sicpro_modulo_web_catalogo/static/src/xml/base_import.xml`
- `sicpro_modulo_web_catalogo/views/website_templates.xml`

### JavaScript / OWL

- `sicpro_modulo_web_catalogo/static/src/js/import_menu_patch.js`

### CSS / SCSS

- `sicpro_modulo_web_catalogo/static/src/css/web_administracion.scss`

---

## sicpro_modulo_web_debug

**Ruta:** `sicpro_app/sicpro_modulo_web_debug`

### Manifest

- **name:** `SICPRO: Web Debug`
- **version:** `19.0.0.0.1`
- **category:** `Website`
- **summary:** `Aplicación para entrar en el modo desarrollo de SICPRO ERP`
- **description:** `Aplicación para entrar en el modo desarrollo de SICPRO ERP`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_web_debug/__init__.py`
- `sicpro_modulo_web_debug/__manifest__.py`

### XML

- `sicpro_modulo_web_debug/static/src/xml/web_debug.xml`

### JavaScript / OWL

- `sicpro_modulo_web_debug/static/src/js/web_debug.js`

---

## sicpro_modulo_web_debug_xml

**Ruta:** `sicpro_app/sicpro_modulo_web_debug_xml`

### Manifest

- **name:** `SICPRO: Web Debug XML`
- **version:** `19.0.0.0.1`
- **category:** `Website`
- **summary:** `Aplicación debug para inspeccionar los archivos XML en él modo desarrollo de SICPRO ERP`
- **description:** `Aplicación debug para inspeccionar los archivos XML en él modo desarrollo de SICPRO ERP`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_web_debug_xml/__init__.py`
- `sicpro_modulo_web_debug_xml/__manifest__.py`

### JavaScript / OWL

- `sicpro_modulo_web_debug_xml/static/src/js/xml_inspector.js`

### CSS / SCSS

- `sicpro_modulo_web_debug_xml/static/src/css/xml_inspector.css`

---

## sicpro_modulo_web_error

**Ruta:** `sicpro_app/sicpro_modulo_web_error`

### Manifest

- **name:** `SICPRO: Web Error`
- **version:** `19.0.0.0.1`
- **category:** `Website`
- **summary:** `El módulo se encarga de las configuraciones de los errores (400, 404, 403, 500)`
- **description:** `El módulo se encarga de las configuraciones de los errores (400, 404, 403, 500)`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `http_routing`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_web_error/__init__.py`
- `sicpro_modulo_web_error/__manifest__.py`

### XML

- `sicpro_modulo_web_error/view/templates.xml`

### CSS / SCSS

- `sicpro_modulo_web_error/static/src/css/style.css`

---

## sicpro_modulo_web_login

**Ruta:** `sicpro_app/sicpro_modulo_web_login`

### Manifest

- **name:** `SICPRO: Web Login SICPRO ERP`
- **version:** `19.0.0.0.1`
- **category:** `Website`
- **summary:** `Crear una nueva configuración del login para SICPRO ERP`
- **description:** `Crear una nueva configuración del login para SICPRO ERP`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `base_setup`
- `web`
- `sicpro_modulo_web`
- `sicpro_app_administracion`

### Modelos Python

- `SicproMantenimiento`

### Python

- `sicpro_modulo_web_login/__init__.py`
- `sicpro_modulo_web_login/__manifest__.py`
- `sicpro_modulo_web_login/controllers/__init__.py`
- `sicpro_modulo_web_login/controllers/main.py`
- `sicpro_modulo_web_login/models/__init__.py`
- `sicpro_modulo_web_login/models/sicpro_web_mantenimiento.py`

### XML

- `sicpro_modulo_web_login/data/sicpro_modulo_web_mantenimiento.xml`
- `sicpro_modulo_web_login/static/src/xml/user_switch.xml`
- `sicpro_modulo_web_login/templates/login_template.xml`
- `sicpro_modulo_web_login/templates/mantenimiento_template.xml`
- `sicpro_modulo_web_login/views/mantenimiento_views.xml`
- `sicpro_modulo_web_login/views/modulo_web_login_menu_views.xml`

### JavaScript / OWL

- `sicpro_modulo_web_login/static/src/js/login_particles.min.js.js`
- `sicpro_modulo_web_login/static/src/js/login_scripts.js`
- `sicpro_modulo_web_login/static/src/js/mantenimiento_contador.js`
- `sicpro_modulo_web_login/static/src/js/mantenimiento_login.js`

### CSV / Seguridad / Datos

- `sicpro_modulo_web_login/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_modulo_web_login/static/src/css/style_login.css`
- `sicpro_modulo_web_login/static/src/css/style_mantenimiento.css`

---

## sicpro_modulo_web_registro

**Ruta:** `sicpro_app/sicpro_modulo_web_registro`

### Manifest

- **name:** `SICPRO: Web Registro Usuario`
- **version:** `19.0.0.0.1`
- **category:** `Website`
- **summary:** `Muestra la página para realizar el registro de usuario al sistema`
- **description:** `Muestra la página para realizar el registro de usuario al sistema`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `http_routing`
- `sicpro_modulo_web`
- `sicpro_app_trabajadores`
- `sicpro_modulo_web_login`
- `sicpro_modulo_roles`
- `sicpro_modulo_ldap_local`
- `sicpro_app_clientes`
- `sicpro_app_administracion`

### Modelos Python

- `PlanillaAccesoRoles`
- `ResUsersWebRoles`
- `SicproWebRoles`
- `SolicitudAccesoRoles`
- `SolicitudesUsuarios`

### Wizards / TransientModel

- `SolicitudAccesoRechazar`

### Python

- `sicpro_modulo_web_registro/__init__.py`
- `sicpro_modulo_web_registro/__manifest__.py`
- `sicpro_modulo_web_registro/controllers/__init__.py`
- `sicpro_modulo_web_registro/controllers/main.py`
- `sicpro_modulo_web_registro/models/__init__.py`
- `sicpro_modulo_web_registro/models/res_users.py`
- `sicpro_modulo_web_registro/models/sicpro_modulo_roles.py`
- `sicpro_modulo_web_registro/models/sicpro_modulo_solicitud_acceso.py`
- `sicpro_modulo_web_registro/models/sicpro_modulo_solicitud_roles.py`
- `sicpro_modulo_web_registro/models/sicpro_modulo_web_registro_roles.py`

### XML

- `sicpro_modulo_web_registro/data/mail_template.xml`
- `sicpro_modulo_web_registro/informes/informe_planilla_acceso_views.xml`
- `sicpro_modulo_web_registro/templates/login_template.xml`
- `sicpro_modulo_web_registro/templates/registro_template.xml`
- `sicpro_modulo_web_registro/templates/web_template.xml`
- `sicpro_modulo_web_registro/views/modulo_web_menu_views.xml`
- `sicpro_modulo_web_registro/views/registro_roles_views.xml`
- `sicpro_modulo_web_registro/views/res_users_views.xml`
- `sicpro_modulo_web_registro/views/roles_views.xml`
- `sicpro_modulo_web_registro/views/sequency.xml`
- `sicpro_modulo_web_registro/views/solicitud_roles_views.xml`

### JavaScript / OWL

- `sicpro_modulo_web_registro/static/src/js/web_registro_actions.js`

### CSV / Seguridad / Datos

- `sicpro_modulo_web_registro/security/ir.model.access.csv`

### CSS / SCSS

- `sicpro_modulo_web_registro/static/src/css/style.css`

---

## sicpro_modulo_web_registro_soporte_bitacora

**Ruta:** `sicpro_app/sicpro_modulo_web_registro_soporte_bitacora`

### Manifest

- **name:** `SICPRO: Registro/Soporte/Bitácora`
- **version:** `19.0.0.1`
- **category:** `Técnico`
- **summary:** `El módulo se encarga de actualizar los tickets de soporte y la bitácora del usuario`
- **description:** `El módulo se encarga de actualizar los tickets de soporte y la bitácora del usuario`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `sicpro_modulo_roles`
- `sicpro_modulo_web_registro`
- `sicpro_app_soporte`

### Modelos Python

- `PlantillaAccesoRoles`
- `PlantillaSoporteBitacora`
- `SoporteTicket`

### Python

- `sicpro_modulo_web_registro_soporte_bitacora/__init__.py`
- `sicpro_modulo_web_registro_soporte_bitacora/__manifest__.py`
- `sicpro_modulo_web_registro_soporte_bitacora/models/__init__.py`
- `sicpro_modulo_web_registro_soporte_bitacora/models/sicpro_app_soporte.py`
- `sicpro_modulo_web_registro_soporte_bitacora/models/sicpro_app_soporte_bitacora.py`
- `sicpro_modulo_web_registro_soporte_bitacora/models/sicpro_modulo_solicitud_acceso.py`

### XML

- `sicpro_modulo_web_registro_soporte_bitacora/view/solicitud_bitacora_views.xml`
- `sicpro_modulo_web_registro_soporte_bitacora/view/solicitud_roles_views.xml`
- `sicpro_modulo_web_registro_soporte_bitacora/view/solicitud_soporte_views.xml`

---

## sicpro_modulo_widget_audio

**Ruta:** `sicpro_app/sicpro_modulo_widget_audio`

### Manifest

- **name:** `SICPRO: Widget de Audio`
- **version:** `19.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite la reproducción de audio en el sistema`
- **description:** `Permite la reproducción de audio en el sistema`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `web`

### Python

- `sicpro_modulo_widget_audio/__init__.py`
- `sicpro_modulo_widget_audio/__manifest__.py`

### XML

- `sicpro_modulo_widget_audio/static/src/xml/ks_audio.xml`

### JavaScript / OWL

- `sicpro_modulo_widget_audio/static/src/js/ks_audio.js`

### CSS / SCSS

- `sicpro_modulo_widget_audio/static/src/css/ks_audio.css`

---

## sicpro_modulo_widget_buscador_one2many

**Ruta:** `sicpro_app/sicpro_modulo_widget_buscador_one2many`

### Manifest

- **name:** `SICPRO: Widget Buscador One2many`
- **version:** `19.0.0.1`
- **category:** `Técnico`
- **summary:** `Función de búsqueda rápida para campos One2many en SICPRO ERP`
- **description:** `Función de búsqueda rápida para campos One2many en SICPRO ERP`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_widget_buscador_one2many/__init__.py`
- `sicpro_modulo_widget_buscador_one2many/__manifest__.py`

### XML

- `sicpro_modulo_widget_buscador_one2many/static/src/xml/one2manysearch.xml`

### JavaScript / OWL

- `sicpro_modulo_widget_buscador_one2many/static/src/js/one2manySearch.js`

### CSS / SCSS

- `sicpro_modulo_widget_buscador_one2many/static/src/css/header.css`

---

## sicpro_modulo_widget_ckeditor

**Ruta:** `sicpro_app/sicpro_modulo_widget_ckeditor`

### Manifest

- **name:** `SICPRO: Widget CKEditor`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite crear nuevo contenido en campos text/html usando el moderno editor WYSIWYG`
- **description:** `Permite crear nuevo contenido en campos text/html usando el moderno editor WYSIWYG`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_widget_ckeditor/__init__.py`
- `sicpro_modulo_widget_ckeditor/__manifest__.py`

### XML

- `sicpro_modulo_widget_ckeditor/static/src/widgets/ckeditor_widget.xml`

### JavaScript / OWL

- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/af.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/af.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ar.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ar.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ast.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ast.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/az.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/az.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/be.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/be.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/bg.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/bg.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/bn.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/bn.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/bs.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/bs.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ca.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ca.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/cs.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/cs.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/da.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/da.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/de-ch.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/de-ch.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/de.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/de.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/el.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/el.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/en-au.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/en-au.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/en-gb.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/en-gb.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/en.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/en.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/eo.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/eo.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/es-co.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/es-co.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/es.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/es.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/et.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/et.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/eu.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/eu.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/fa.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/fa.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/fi.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/fi.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/fr.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/fr.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/gl.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/gl.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/gu.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/gu.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/he.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/he.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/hi.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/hi.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/hr.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/hr.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/hu.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/hu.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/hy.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/hy.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/id.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/id.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/it.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/it.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ja.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ja.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/jv.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/jv.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/kk.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/kk.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/km.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/km.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/kn.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/kn.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ko.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ko.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ku.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ku.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/lt.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/lt.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/lv.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/lv.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ms.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ms.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/nb.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/nb.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ne.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ne.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/nl.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/nl.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/no.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/no.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/oc.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/oc.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/pl.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/pl.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/pt-br.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/pt-br.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/pt.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/pt.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ro.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ro.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ru.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ru.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/si.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/si.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/sk.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/sk.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/sl.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/sl.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/sq.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/sq.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/sr-latn.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/sr-latn.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/sr.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/sr.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/sv.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/sv.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/th.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/th.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ti.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ti.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/tk.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/tk.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/tr.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/tr.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/tt.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/tt.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ug.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ug.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/uk.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/uk.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ur.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/ur.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/uz.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/uz.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/vi.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/vi.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/zh-cn.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/zh-cn.umd.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/zh.js`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/zh.umd.js`
- `sicpro_modulo_widget_ckeditor/static/src/widgets/UploadAdapter.js`
- `sicpro_modulo_widget_ckeditor/static/src/widgets/UploadAdapterPlugin.js`
- `sicpro_modulo_widget_ckeditor/static/src/widgets/ckeditor_widget.js`

### CSS / SCSS

- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5-content.css`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5-editor.css`
- `sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5.css`
- `sicpro_modulo_widget_ckeditor/static/src/widgets/ckeditor_widget.scss`

---

## sicpro_modulo_widget_colorpicker

**Ruta:** `sicpro_app/sicpro_modulo_widget_colorpicker`

### Manifest

- **name:** `SICPRO: Widget Color Picker`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite agregar nuevo widget de color a la vista.`
- **description:** `Permite agregar nuevo widget de color a la vista.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_widget_colorpicker/__init__.py`
- `sicpro_modulo_widget_colorpicker/__manifest__.py`

### XML

- `sicpro_modulo_widget_colorpicker/static/src/js/color_picker_field.xml`

### JavaScript / OWL

- `sicpro_modulo_widget_colorpicker/static/src/js/color_picker_field.js`
- `sicpro_modulo_widget_colorpicker/static/src/lib/pickr/pickr.min.js`

### CSS / SCSS

- `sicpro_modulo_widget_colorpicker/static/src/css/widget.css`
- `sicpro_modulo_widget_colorpicker/static/src/lib/pickr/classic.min.css`

---

## sicpro_modulo_widget_colorpickerbar

**Ruta:** `sicpro_app/sicpro_modulo_widget_colorpickerbar`

### Manifest

- **name:** `SICPRO: Widget Color Picker Bar`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite agregar nuevo widget de color a la vista en formato de cuadros de selección.`
- **description:** `Permite agregar nuevo widget de color a la vista en formato de cuadros de selección.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `base`
- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_widget_colorpickerbar/__init__.py`
- `sicpro_modulo_widget_colorpickerbar/__manifest__.py`

### XML

- `sicpro_modulo_widget_colorpickerbar/static/src/owl/color-picker.xml`

### JavaScript / OWL

- `sicpro_modulo_widget_colorpickerbar/static/src/owl/color-picker.js`

---

## sicpro_modulo_widget_contador

**Ruta:** `sicpro_app/sicpro_modulo_widget_contador`

### Manifest

- **name:** `SICPRO: Contador de Números`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite controlar, subir y bajar valores mediante botones`
- **description:** `Permite controlar, subir y bajar valores mediante botones`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `web`

### Python

- `sicpro_modulo_widget_contador/__init__.py`
- `sicpro_modulo_widget_contador/__manifest__.py`

### XML

- `sicpro_modulo_widget_contador/demo/ir_cron.xml`
- `sicpro_modulo_widget_contador/demo/res_users_view.xml`
- `sicpro_modulo_widget_contador/static/src/xml/numeric_step.xml`

### JavaScript / OWL

- `sicpro_modulo_widget_contador/static/src/js/numeric_step.esm.js`

### CSS / SCSS

- `sicpro_modulo_widget_contador/static/src/css/numeric_step.scss`

---

## sicpro_modulo_widget_datepicker

**Ruta:** `sicpro_app/sicpro_modulo_widget_datepicker`

### Manifest

- **name:** `SICPRO: Multiples Fechas`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite la selección de multiples fechas en un solo campo y modificar la traducción de los meses, semanas y días del formato de calendario.`
- **description:** `Permite la selección de multiples fechas en un solo campo y modificar la traducción de los meses, semanas y días del formato de calendario.`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `base`

### Python

- `sicpro_modulo_widget_datepicker/__init__.py`
- `sicpro_modulo_widget_datepicker/__manifest__.py`

### XML

- `sicpro_modulo_widget_datepicker/static/src/xml/datepicker_widget.xml`

### JavaScript / OWL

- `sicpro_modulo_widget_datepicker/static/src/js/datepicker_widget.js`

### CSS / SCSS

- `sicpro_modulo_widget_datepicker/static/src/css/datepicker_widget.css`

---

## sicpro_modulo_widget_json

**Ruta:** `sicpro_app/sicpro_modulo_widget_json`

### Manifest

- **name:** `SICPRO: Widget JSON`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite visualizar y editar información en formato JSON`
- **description:** `Permite visualizar y editar información en formato JSON`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_widget_json/__init__.py`
- `sicpro_modulo_widget_json/__manifest__.py`

### XML

- `sicpro_modulo_widget_json/static/src/components/json_widget/json_widget.xml`

### JavaScript / OWL

- `sicpro_modulo_widget_json/static/src/components/json_widget/json_widget.js`

---

## sicpro_modulo_widget_m2o_info

**Ruta:** `sicpro_app/sicpro_modulo_widget_m2o_info`

### Manifest

- **name:** `SICPRO: Widget Many2One Info`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Muestra lista de búsqueda de un many2one`
- **description:** `Muestra lista de búsqueda de un many2one`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `web`
- `sicpro_app_administracion`

### Python

- `sicpro_modulo_widget_m2o_info/__init__.py`
- `sicpro_modulo_widget_m2o_info/__manifest__.py`
- `sicpro_modulo_widget_m2o_info/tools/__init__.py`
- `sicpro_modulo_widget_m2o_info/tools/utils.py`

### XML

- `sicpro_modulo_widget_m2o_info/static/src/xml/popover_template.xml`

### JavaScript / OWL

- `sicpro_modulo_widget_m2o_info/static/src/js/form_renderer.js`
- `sicpro_modulo_widget_m2o_info/static/src/js/m2o_info_widget.js`

### CSS / SCSS

- `sicpro_modulo_widget_m2o_info/static/src/scss/m2o_info_widget.scss`

---

## sicpro_modulo_widget_time_delta

**Ruta:** `sicpro_app/sicpro_modulo_widget_time_delta`

### Manifest

- **name:** `SICPRO: Formato a Fechas`
- **version:** `19.0.0.0.1`
- **category:** `Técnico`
- **summary:** `Permite agregar nuevo estilo de formato a las fechas`
- **description:** `Permite agregar nuevo estilo de formato a las fechas`
- **license:** `AGPL-3`
- **application:** `True`
- **installable:** `True`

**Dependencias:**

- `sicpro_app_administracion`
- `base`
- `web`

### Python

- `sicpro_modulo_widget_time_delta/__init__.py`
- `sicpro_modulo_widget_time_delta/__manifest__.py`

### XML

- `sicpro_modulo_widget_time_delta/static/src/js/timedelta_field.xml`
- `sicpro_modulo_widget_time_delta/static/src/xml/qweb_template.xml`

### JavaScript / OWL

- `sicpro_modulo_widget_time_delta/static/src/js/timedelta_field.js`
- `sicpro_modulo_widget_time_delta/static/src/lib/duration-humanize/humanize-duration.js`
- `sicpro_modulo_widget_time_delta/static/src/lib/duration-picker/jquery-duration-picker.js`
- `sicpro_modulo_widget_time_delta/static/src/lib/jquery.js`

### CSS / SCSS

- `sicpro_modulo_widget_time_delta/static/src/css/timedelta_field.css`
- `sicpro_modulo_widget_time_delta/static/src/lib/duration-picker/jquery-duration-picker.css`

---

