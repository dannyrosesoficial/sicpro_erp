# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

# curl -X POST -F 'master_pwd=abcd' -F 'name=xyz' -F 'backup_format=zip' -o /path/xyz.zip http://localhost:8069/web/database/backup
import requests
import argparse
import os
import datetime
import psycopg2
import subprocess
from urllib.parse import urlparse
import json


class BackupStorage():
    def __init__(self):
        self.client_url = ""
        self.ssh_obj = None
        self.saas_ssh_obj = None
        self.msg = ""
        self.filename = ""
        self.backup_time = None
        self.backup_file_path = ""
        self.remote_backup_file_path = ""
        self.temp_backup_file_path = ""
        
    def init_parser(self):
        """
            Método para inicializar el analizador de argumentos de línea de comando,
            y devolver el objeto analizador.
        """
        parser = argparse.ArgumentParser(description='Process some arguments.')
        parser.add_argument('--mpswd', action='store',
                            help='Master password Odoo')
        parser.add_argument('--url', action='store',
                            help='saas client url')
        parser.add_argument('--dbname', action='store',
                            help='name of database to backup')
        parser.add_argument('--maindb', action='store',
                            help='name of main database')
        parser.add_argument('--dbuser', action='store',
                            help='username of main database')
        parser.add_argument('--dbpassword', action='store',
                            help='password of main database')
        parser.add_argument('--processid', action='store',
                            help='process id')
        parser.add_argument('--bkploc', action='store',
                            help='backup location local, dedicated, s3')
        parser.add_argument('--path', action='store',
                            help='Backup Path')
        parser.add_argument('--backup_format', action='store',
                            help='Backup Type')
        
        parser.add_argument('--rhost', action='store',
                    help='Remote Hostname')
        parser.add_argument('--rport', action='store',
                    help='Remote Port')
        parser.add_argument('--ruser', action='store',
                    help='Remote User')
        parser.add_argument('--rpass', action='store',
                    help='Remote Password')
        
        parser.add_argument('--temp_bkp_path', action='store',
                    help='Temporary Backup Directory')
        
        # Argumentos relacionados con el módulo SaaS Kit Backup
        parser.add_argument('--is_remote_client', action='store',
                    help='Is Remote SaaS Client')
        

        return parser
    
    def database_entry(self, main_db, db_user, db_password, db_name, file_name, process_id, file_path, url, backup_date_time, status, message, kwargs={}):
        """
            Método para insertar detalles de la copia de seguridad creada en la base de datos.
        """
        try:
            if db_user == "False" or db_password == "False":
                connection = psycopg2.connect(database=main_db)
            else:
                connection = psycopg2.connect(user=db_user, password=db_password, host="127.0.0.1", port="5432", database=main_db)
        except Exception as e:
            print(e)
            print('Exited')
            exit(0)

        try:
            file_path = file_path.replace('//', '/')
            url = url.replace('//', '/')
            # Connect to database
            QUERY = "INSERT INTO sicpro_backup_local_detalles (name, file_name, backup_process_id, file_path, url, backup_date_time, status, message) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            RECORD = (db_name, file_name, process_id, file_path, url, backup_date_time, status, message)
            cursor = connection.cursor()
            print("Información del servidor PostgreSQL")
            print(connection.get_dsn_parameters(), "\n")
            cursor.execute(QUERY, RECORD)
            connection.commit()
            count = cursor.rowcount
            print(count, "Registro insertado")
        except Exception as e:
            print(e)
        finally: 
            if connection:
                cursor.close()
                connection.close()
                print("Conexión Postgresql cerrada")
    
    def login_backup_remote(self, args):
        """
            Method to login to remote backup server.
        """
        try:
            import paramiko
            ssh_obj = paramiko.SSHClient()
            ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_obj.connect(hostname=args.rhost, username=args.ruser, password=args.rpass,port=args.rport)
            self.ssh_obj = ssh_obj
        except ImportError:
            raise Exception("Módulo paramiko no encontrado. Instálelo usando pip: pip3 install paramiko")
        except Exception as e:
            print("No se pudo conectar al servidor de respaldo remoto.", e)
            raise Exception("No se pudo conectar al servidor de respaldo remoto.")
            
    def execute_on_remote_shell(self, ssh_obj,command):
        """
            Método para ejecutar comandos en el shell del servidor remoto.
        """
        response = dict()
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = ssh_obj.exec_command(command)
            print("ejecutar_on_remote_shell fuera: ")
            res = ssh_stdout.readlines()
            print(res)
            print("ejecutar_on_remote_shell error: ")
            err = ssh_stderr.readlines()
            print(err)
            if err:
                raise Exception(err)
            response['status'] = True
            response['result'] = res
            return response
        except Exception as e:
            print("+++ERROR++",command)
            print("++++++++++ERROR++++",e)
            response['status'] = False
            response['message'] = str(e)
            return response
    
    def check_remote_backup_path(self, args, backup_dir):
        """
            Método para verificar la ruta de copia de seguridad remota.
        """
        response = dict(status=False)
        try:
            self.login_backup_remote(args)
            cmd = "ls %s"%(backup_dir)
            check_path = self.execute_on_remote_shell(self.ssh_obj ,cmd)
            if check_path and not check_path.get('status'):
                print("Error al comprobar la ruta del directorio remoto - ", check_path.get('message'))
                raise Exception("Error al comprobar la ruta del directorio remoto - "+check_path.get('message'))
            if check_path and not check_path.get('result'):
                cmd = "mkdir -p %s; chmod -R 777 %s"%(backup_dir, backup_dir)
                upd_permission = self.execute_on_remote_shell(self.ssh_obj,cmd)
                if upd_permission and not upd_permission.get('status'):
                    print("Error al crear directorio y actualizar permisos - ", check_path.get('message'))
                    raise Exception("No se puede crear un directorio remoto ni actualizar permisos.")
            response.update(status=True)
        except Exception as e:
            print("Error: crear directorio de respaldo")
            response.update(message=e)
        return response
    
    def create_client_url(self, url):
        """
            Método para crear la URL del cliente para crear las copias de seguridad.
        """
        client_url = ""
        if urlparse(url).scheme not in ['http','https']:
            client_url = 'http://' + url + \
                ('/' if url[-1] != '/' else '')
        else:
            client_url = url + ('/' if url[-1] != '/' else '')
        
        client_url += 'saas/database/backup'
        return client_url
    
    
    def store_backup_file(self, args, kwargs):
        """
            Method to store backup file on the local server in the mentioned path.
        """
        res = dict(status=False)
        data = {
            'master_pwd': args.mpswd,
            'name': args.dbname,
            'backup_format': args.backup_format or "zip"
        }
        
        client_url = self.client_url
        backup_dir = kwargs.get('backup_dir')
        try:
            filename = None
            backup_time = None
            backup_file_path = None
            with requests.post(client_url, data=data, stream=True) as response:
                response.raise_for_status()
                filename = response.headers.get('Backup-Filename', '')
                backup_time = response.headers.get('Backup-Time', datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S"))
                backup_file_path = os.path.join(backup_dir, filename)

                if response.headers.get('Content-Disposition'):
                    with open(backup_file_path, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                else:
                    raise Exception(response.content.decode())

            msg = 'Copia de seguridad de la base de datos exitosa en ' + str(backup_time)
            res.update(status=True, filename=filename, backup_time=backup_time, backup_file_path=backup_file_path)
        except Exception as e:
            res.update(message=e)
        
        return res

    def manage_backup_files(self, args):
        """
            Método para administrar los archivos de respaldo en un servidor local, en un servidor remoto o en cualquier servidor en la nube
        """
        vals = dict()
        backup_dir = os.path.join(args.path, 'backups')
        response = dict(status=False)
        self.client_url = self.create_client_url(args.url)
        try:
            vals.update(backup_dir=backup_dir)
            backup_location = args.bkploc
            if hasattr(self,'_create_%s_backup'%backup_location):## if you want to update dictionary then you can define this function _call_{backup_location}_backup_script
                response = getattr(self,'_create_%s_backup'%backup_location)(args, vals)
                
            msg = 'Copia de seguridad de la base de datos exitosa en ' + str(self.backup_time)
            self.database_entry(args.maindb, args.dbuser, args.dbpassword, args.dbname, self.filename, args.processid, backup_dir+'/', self.backup_file_path, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status="Success", message=msg)
            response.update(status=True, message=msg)
        except Exception as e:
            msg = 'Falló en ' + str(self.backup_time or datetime.datetime.now()) + ' ' + str(e)
            self.database_entry(args.maindb, args.dbuser, args.dbpassword, args.dbname, self.filename, args.processid, backup_dir+'/', self.backup_file_path if self.backup_file_path else self.remote_backup_file_path if self.remote_backup_file_path else '', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status="Failure", message=msg)
            response.update(status=False, message=msg)
        return response

    def _create_local_backup(self, args, vals):
        """
            Método para crear una copia de seguridad en el servidor local.
            Copia el archivo de copia de seguridad local al servidor saas remoto.
        """
        response = dict(status=False)
        temp_backup_dir = None
        backup_dir = vals.get('backup_dir')
        if not os.path.exists(backup_dir) and not eval(args.is_remote_client if args.is_remote_client else 'False'):
            os.makedirs(backup_dir)
            
        if args.is_remote_client and eval(args.is_remote_client):
            temp_backup_dir = args.temp_bkp_path
            vals.update(backup_dir=temp_backup_dir)
                
        backup_store_res = self.store_backup_file(args, vals)
        if backup_store_res and not backup_store_res.get('status'):
            raise Exception(backup_store_res.get('message'))

        self.filename = backup_store_res.get('filename')
        self.backup_time = backup_store_res.get('backup_time')
        self.backup_file_path = backup_store_res.get('backup_file_path')
        
        if args.is_remote_client and eval(args.is_remote_client):
            self.backup_file_path = os.path.join(backup_dir, self.filename)
            self.temp_bkp_file_path = backup_store_res.get('backup_file_path')
            response = self._create_saas_remote_backup(args)
            
        return response
    
    def _create_remote_backup(self, args, vals):
        """
            Método para crear la copia de seguridad temporal de la base de datos en el servidor principal y almacenarla en el servidor remoto.
            El archivo temporal de copia de seguridad de la base de datos se eliminará después de almacenarlo en el servidor remoto.
        """
        response = dict(status=False)
        backup_dir = vals.get('backup_dir')
        temp_backup_dir = args.temp_bkp_path
        vals.update(backup_dir=temp_backup_dir)
        check_path_res = self.check_remote_backup_path(args, backup_dir)
        if check_path_res and not check_path_res.get('status'):
            raise Exception(check_path_res.get('message'))
        backup_store_res = self.store_backup_file(args, vals)
        if backup_store_res and not backup_store_res.get('status'):
            raise Exception(backup_store_res.get('message'))

        self.filename = backup_store_res.get('filename')
        self.backup_time = backup_store_res.get('backup_time')
        self.temp_backup_file_path = backup_store_res.get('backup_file_path')
        self.remote_backup_file_path = os.path.join(backup_dir, self.filename)
        self.backup_file_path = self.remote_backup_file_path
        
        sftp = self.ssh_obj.open_sftp()
        sftp.put(self.temp_backup_file_path, self.remote_backup_file_path)
        sftp.close()
        
        cmd = f"ls -f {self.remote_backup_file_path}"

        # Checking if the backup file is successfully copied to remote server
        check_file_exist = self.execute_on_remote_shell(self.ssh_obj,cmd)
        if check_file_exist and check_file_exist.get("status"):
            print("\nArchivo de copia de seguridad copiado correctamente en el servidor remoto.")
            print("ruta_del_archivo_de_copia_de_copia de seguridad remota --->", self.remote_backup_file_path)
            
            # DELETE the temporary backup file from the Main Server
            if os.path.exists(self.temp_backup_file_path):
                os.remove(self.temp_backup_file_path)
                print("\nArchivo de copia de seguridad eliminado exitosamente del servidor principal.")
            
            response.update(status=True)
            return response
        else:
            print("\nEl archivo de copia de seguridad no se movió correctamente al servidor remoto.")
            raise Exception("El archivo de copia de seguridad no se pudo mover al servidor remoto.")
    
    def login_saas_remote(self, remote):
        """
            Método para iniciar sesión en el servidor SaaS remoto mediante SSH.
        """
        try:
            import paramiko
            ssh_obj = paramiko.SSHClient()
            ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_obj.connect(hostname=remote.get('host'), username=remote.get('user'), password=remote.get('password'),port=remote.get('port'))
            self.saas_ssh_obj = ssh_obj
        except ImportError:
            raise Exception("Módulo paramiko no encontrado. Instálelo usando pip: pip3 install paramiko")
        except Exception as e:
            print("Couldn't connect remote SaaS server: ", e)
            raise Exception("Couldn't connect to remote SaaS server.")
    
    
    def _create_saas_remote_backup(self, args):
        """
            Este método está diseñado para lograr la compatibilidad con el módulo SaaS Kit Backup.
            Este método copiará el archivo de copia de seguridad local al servidor saas remoto.
            El archivo de copia de seguridad temporal se eliminará después de almacenarlo en el servidor saas remoto.
        """
        saas_url = 'http://localhost:8069/remote/server/creds'
        saas_data = {
            'sicpro_backup_local_id': int(args.processid)
        }
        response = dict(status=False)
        try:
            # Obtener las credenciales del servidor host del servidor saas remoto
            with requests.post(saas_url, data=saas_data, stream=True) as saas_response:
                saas_response.raise_for_status()
                resp = json.loads((saas_response.content).decode())
                
                # Carga del archivo de copia de seguridad desde el servidor principal al servidor saas remoto
                self.login_saas_remote(resp.get('host_server'))
                if self.saas_ssh_obj:
                    saas_sftp = self.saas_ssh_obj.open_sftp()
                    saas_sftp.put(self.temp_bkp_file_path, self.backup_file_path)

                    # Eliminar la copia de seguridad temporal en el servidor principal
                    if os.path.exists(self.temp_bkp_file_path):
                        os.remove(self.temp_bkp_file_path)
                    saas_sftp.close()
                    print("Archivo de copia de seguridad local copiado correctamente en el servidor SaaS remoto")

            response.update(status=True)
        except Exception as e:
            print("Excepción al copiar la copia de seguridad local al servidor saas remoto")
            raise Exception("El archivo de copia de seguridad local no se pudo mover al servidor saas remoto.")
        return response

if __name__ == '__main__':
    backup_storage = BackupStorage()
    parser = backup_storage.init_parser()
    args = parser.parse_args()
    print(backup_storage.manage_backup_files(args))


