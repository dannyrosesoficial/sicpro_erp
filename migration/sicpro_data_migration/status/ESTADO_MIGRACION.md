# SICPRO ERP — Estado General de Migración Odoo 15 → Odoo 19

**Última actualización:** 2026-09-17
**Origen:** Odoo 15 / PostgreSQL 13 / sicpro_produccion
**Destino:** Odoo 19 / PostgreSQL 17 / sicpro
**Estado:** INVENTARIO Y ANÁLISIS — MIGRACIÓN DE DATOS NO INICIADA

## Metodología

INVENTARIO → COMPARACIÓN → DEPENDENCIAS → MAPEO DE IDs → TRANSFORMACIONES → DRY-RUN → REPORTE → APROBACIÓN → MIGRACIÓN → VALIDACIÓN

## Reglas principales

- Preservar IDs de Odoo 15 cuando estén libres en Odoo 19.
- Si existe conflicto, asignar nuevo ID y registrar el mapping.
- Actualizar todas las referencias hacia IDs remapeados.
- No eliminar registros exclusivos del target.
- No sobrescribir metadata técnica de Odoo 19.
- No migrar gamification.*.
- No migrar automáticamente datos de módulos eliminados.
- Mantener el origen Odoo 15 intacto.
- No modificar sicpro durante inventario y análisis.
- Toda transformación debe quedar documentada y validada antes de ejecutarse.

## Inventario global COMPLETADO

### Tablas

- Odoo 15: 715
- Odoo 19: 676
- Comunes: 480
- Solo Odoo 15: 235
- Solo Odoo 19: 196

### ir_model

- Odoo 15: 594
- Odoo 19: 594
- Modelos comunes: 432
- Mismo ID: 16
- ID diferente: 416
- Solo Odoo 15: 162
- Solo Odoo 19: 162

Regla crítica: los IDs de ir_model de Odoo 15 no deben utilizarse como referencias técnicas en Odoo 19.

### ir_model_fields

- Odoo 15: 12123
- Odoo 19: 11770
- Comunes: 8373
- Sin diferencias estructurales relevantes: 8114
- Solo Odoo 15: 3750
- Solo Odoo 19: 3397
- Cambios de tipo: 20
- Cambios de relación: 12
- Cambios de store: 42
- Cambios de required: 25
- Cambios de readonly: 181

### Foreign Keys

- Odoo 15: 1560
- Odoo 19: 1898
- Comunes: 1034
- Solo Odoo 15: 526
- Solo Odoo 19: 864

## Evidencias

Inventario físico:

- 98 archivos
- 94 con datos
- 4 vacíos

Archivo maestro:

status/INVENTARIO_EVIDENCIAS.txt

Archivos vacíos:

- compare/scope/ir_attachment_model_mapping_15_19.txt
- compare/scope/roles_19_detail.txt
- compare/scope/role_users_mapping.txt
- inventory/table_row_estimates_15.txt

Los archivos vacíos no se consideran análisis completados hasta determinar si representan un resultado válido o una prueba incompleta.

## res.company

ESTADO: ANALIZADO

- 11 compañías relevantes para usuarios vinculados a trabajadores.
- Los company_id de esos usuarios coinciden por ID entre origen y destino.
- No se requiere remapeo de compañía para ese conjunto.

## res.partner

ESTADO: EN CURSO

- Origen: 537 partners.
- Los 537 están referenciados.
- Target: conjunto técnico inicial de Odoo 19.
- Existen conflictos de identidad en los IDs iniciales.
- Ya existen análisis de identidad, referencias FK, usuarios, compañías y candidatos de correspondencia.

Evidencias principales:

- compare/partners/partner_identity_15.txt
- compare/partners/partner_fk_usage_15.txt
- compare/partners/partners_functional_15.txt
- compare/partners/users_partners_companies_15.txt
- compare/scope/partner_identity_candidates.csv
- compare/scope/partner_identity_review.csv
- compare/scope/partners_id_conflicts_1_15.txt

PENDIENTE:

- cerrar mapping definitivo partner_id_15 → partner_id_19
- parent_id
- commercial_partner_id
- relaciones con res_users
- relaciones con modelos SICPRO

## res.users

ESTADO: ANALIZADO / CIERRE PENDIENTE

- Origen: 485 usuarios.
- 235 vinculados a trabajadores.
- 250 sin trabajador.
- Los 235 usuarios vinculados a trabajadores fueron localizados con mismo ID y login en el análisis realizado.

No insertar ni remapear esos usuarios sin nueva evidencia de conflicto.

Pendiente:

- partner_id
- company_id
- grupos
- roles
- relaciones adicionales
- usuarios sin trabajador
- usuarios técnicos

## Trabajadores

ESTADO: PENDIENTE

- Origen: 1499 trabajadores.
- 235 asociados a usuarios.
- 49 utilizados como autores de ANIR.
- Target sicpro_app_trabajadores vacío.

Debe construirse:

trabajador_id_15 → trabajador_id_19

Primero identidad y conflictos; después relaciones dependientes.

## Roles y grupos

ESTADO: ANALIZADO / TRANSFORMACIÓN PENDIENTE

Odoo 15:

- sicpro_modulo_roles: 131
- sicpro_modulo_roles_line: 2866

Odoo 19:

- res.users.role
- res.users.role.line

Existe transformación estructural.

Ya analizados:

- roles
- grupos
- XML IDs
- contexto de grupos
- uso de roles
- usuarios
- partners

Pendiente:

- mapping definitivo de roles
- mapping definitivo de grupos
- mapping de usuarios a roles

## Attachments

ESTADO: ANÁLISIS AVANZADO

- Total origen: 35842
- Con res_model + res_id: 25894
- Sin propietario explícito: 9948

Casos ya analizados:

- trabajadores
- oportunidades
- partners
- credenciales
- soporte
- reuniones
- administración
- transporte
- repositorio
- especialidades
- instrucciones
- gestor documental
- compañías
- metadata técnica
- gamification

Caso confirmado:

sicpro.app.solicitudes.tabla.oportunidades → sicpro.app.solicitudes.oportunidades

Los 1422 attachments de la tabla auxiliar fueron validados mediante la relación con oportunidades principales.

NO MIGRAR:

- gamification.*
- ir.ui.view
- ir.ui.menu
- módulos eliminados sin reemplazo demostrado
- attachments huérfanos sin regla de recuperación

Módulos eliminados identificados:

- sicpro.app.contratos
- sicpro.app.contratos.proveedores
- sicpro.modulo.web.plugins
- sicpro.modulo.web.about

No se utilizarán búsquedas aproximadas para sustituir estos propietarios.

## sicpro.app.repo / ANIR

ESTADO: ANALIZADO

- 32 registros
- 1 raíz ANIR
- 11 carpetas
- 20 documentos
- 30 relaciones documento/attachment
- 49 trabajadores autores
- 65 relaciones de autores

Mapping de nomencladores confirmado:

tipo:
4 → 4

idioma:
77 → 83

stage:
1 → 1
3 → 3

Target sicpro_app_repo vacío.

Pendiente resolver trabajadores para poder migrar autores.

## Modelos históricos de Odoo 15

Se identificaron 85 modelos SICPRO registrados históricamente en Odoo 15 que no están presentes actualmente en el código 19.

- 83 poseen tabla física.
- 2 no poseen tabla física.

Entre ellos existen familias históricas de:

- contratos
- beneficiarios
- cuentas
- proveedores
- oportunidades
- auditorías
- roles
- plantillas de acceso
- backups
- correo
- dashboard
- mapas
- API
- web

Su existencia no implica migración automática.

Cada familia debe clasificarse como:

MIGRAR / TRANSFORMAR / REEMPLAZAR / HISTÓRICO / NO MIGRAR / REVISIÓN MANUAL

## Transformaciones confirmadas

- sicpro.modulo.roles → res.users.role
- sicpro.modulo.roles_line → res.users.role.line
- sicpro.app.salon.clases.documentacion → ir.attachment
- sicpro.app.solicitudes.tabla.oportunidades → sicpro.app.solicitudes.oportunidades para attachments
- sicpro.app.ordenes.trabajo.cliente_id → campo related
- sicpro.app.ordenes.trabajo.sap_cliente_id → many2one a char
- sicpro.app.ordenes.trabajo.sap_especialidad_id → many2one a char
- sicpro.app.ordenes.trabajo.sap_as_valor → monetary a float
- campos SAP específicos date/monetary → char
- sicpro.app.transferencias.gastos.ordenes.name → orden_id

## Backup

Base destino:

sicpro

Copia previa:

sicpro_pre_migracion

Dump:

/opt/odoo/sicpro_erp/backup/migracion/sicpro_pre_migracion.dump

La migración real todavía no ha comenzado.

## Estado de fases

- Inventario físico: COMPLETADO
- ir_model: COMPLETADO
- ir_model_fields: COMPLETADO
- Foreign Keys: COMPLETADO
- Comparación de tablas: COMPLETADO
- Comparación de modelos: COMPLETADO
- Comparación de campos: COMPLETADO
- Matriz modelos/tablas: COMPLETADO
- res.company: ANALIZADO
- res.partner: EN CURSO
- res.users: ANALIZADO / CIERRE PENDIENTE
- Trabajadores: PENDIENTE
- Roles/grupos: ANALIZADO / TRANSFORMACIÓN PENDIENTE
- Attachments: ANÁLISIS AVANZADO
- ANIR: ANALIZADO
- Mapping global de IDs: PENDIENTE
- Reglas de transformación: EN CURSO
- Dry-run: NO INICIADO
- Migración real: NO INICIADA
- Validación final: NO INICIADA

## Próxima tarea

Cerrar res.partner.

Objetivo:

partner_id_15 → partner_id_19

Debe quedar resuelto antes de construir el mapping global y antes de migrar usuarios, trabajadores y relaciones dependientes.

## Regla de continuidad

Antes de cada prueba:

1. Leer este archivo.
2. Revisar INVENTARIO_EVIDENCIAS.txt.
3. Revisar las evidencias existentes.
4. No repetir análisis ya completados.
5. Ejecutar solamente la siguiente prueba necesaria.
6. Guardar el resultado.
7. Actualizar este archivo cuando cambie materialmente el estado.
8. No modificar sicpro durante inventario y análisis.
9. No ejecutar SQL destructivo sin diagnóstico, backup y aprobación explícita.
10. No convertir inferencias en mappings aprobados.
