=====================
Parámetros generales del diccionario para la firma digital
=====================

            dct = {
                # Alineado: int si 0 entonces precomputar el tamaño de la firma, pero los primeros datos falsos se
                # firmarán, ! = 0 número de hexbytes (00) reservado para firma, debe ser igual o globo que la
                # representación hexadecimal de la firma Probablemente 16384 será suficiente ...
                "aligned": 0,

                # Sigflags: int predeterminado: 3 1,2,3 - banderas para acroform
                "sigflags": 3,

                # SIGFLAGSFT: int predeterminado: 132 - Banderas para el widget de anotación desde PDF 12.5.3
                "sigflagsft": 132,

                # SigPage: int predeterminado: 0 - página en la que debe aparecer firma
                "sigpage": 0,
                # "sigbutton": True,

                # Sigfield: cadena predeterminada: Signature1
                "sigfield": "Signature1",

                # auto_sigfield: bool predeterminado: falso, Falso - No verifique los conflictos de nombres de Sigfield
                # Verdadero: adjuntar e incrementar sufijo a Sigfield cuando un campo Por el nombre de Sigfield ya
                # existe en acroformas
                "auto_sigfield": True,

                # SigandCertify: bool predeterminado: falso, Falso - firmar solo documento,
                # Verdadero: firmar y certificar documento
                #"sigandcertify": True,

                # SignatureBox: Box | Ninguno predeterminado: Ninguno - Dónde colocar la imagen/cadena de firma en la
                # página seleccionada. Las coordenadas se basan en la esquina inferior izquierda de la anotación
                "signaturebox": (380, 1300, 600, 20),

                # signature: cadena Si el cuadro no es ninguno, entonces debería ser una cadena codificable Latin1.
                #"signature": "Firmado digitalmente por",

                # SignForm: bool predeterminado: falso, Falso: no complete el campo de firma de un formulario existente
                # Verdadero: adjunte la firma al campo SIG preexistente por él.
                # El nombre proporcionado por Sigfield en acroform. Usar con Signature o Signature_img, llenará la firma
                # Widget de Field, ignorando SignatureBox.
                "signForm": False,

                # signature_img: string | pil_image si el cuadro no es ninguno y la cadena es ninguna, entonces debería
                # ser instancia de imagen de pil o nombre de archivo de imagen o Matriz de imagen de bytes.
                #"signature_img": img,

                # signature_img_distort: bool predeterminado: verdadero, Verdadero: no mantenga la relación de aspecto
                # de la imagen, llene la Caja limitante completa, distorsionando la imagen. Esto se establece en
                # verdadero para que coincida con el comportamiento de versiones anteriores de Endesive,
                # Falso - Mantener la relación de aspecto de la imagen al ajustar Imagen en el cuadro delimitador
                # "signature_img_distort": "",

                # signature_img_centred: bool predeterminado: verdadero,
                # Verdadero: imágenes centrales dentro del cuadro delimitador cuando La relación de aspecto de la imagen
                # no coincide con la del cuadro delimitador, Falso: no centren la imagen, colóquela en él inferior
                # izquierda de la caja delimitadora
                #"signature_img_centred": False,

                # signature_appearance: dict si el cuadro no es ninguno, entonces rinde una apariencia de firma que es
                # configurado por el dict. Ver a continuación para la configuración.
                "signature_appearance": {
            #'background': False,
            #'icon': '/opt/odoo/sicpro_erp/firma/firma.png',
            #'outline': [0.2, 0.3, 0.5],
            #'border': 2,
            'labels': True,
            'display': 'CN,DN,date,contact,reason,location'.split(','),
             'software': 'SICPRO ERP',
            },

                # signature_manual: Lista Si el cuadro no es ninguno, entonces rinde una firma creada manualmente
                # APEPACIDAD Uso de las directivas contenidas en esta lista.
                # "signature_manual": "",

                # manual_fonts: fuentes de dict requeridos por la apariencia de firma manual
                # "manual_fonts": "",

                # manual_images: imágenes de dict requeridas por la apariencia de firma manual
                # "manual_images": "",

                # contact: Cadena Información requerida sobre la persona que firma el documento
                "contact": "Daniel Barrero Reyes",

                # location: Cadena Información requerida sobre la ubicación de la persona que firma el documento
                "location": "CUBA",

                # signingdate: Cadena Información requerida sobre el tiempo de firma, por ejemplo, ahora.
                "signingdate": fecha,

                # reason: Cadena Información requerida sobre la razón para firmar el documento
                "reason": "Firmado con SICPRO ERP. DVPE - ETECSA",

                # Contraseña: Cadena requerida Si el documento está protegido con contraseña, firmarlo también requiere
                # de la contraseña
                "password": password,

                # text: Atributos de texto de dict wrapText = True, FontSize: 12, Textalign: 'Left', LinePacing: 1.2
                #"text": {'wraptext': True, 'fontsize': 8, 'textalign': 'left', 'linespacing': 1.2, },

                # application: Cadena Nombre opcional de la aplicación en un signo avanzado Diálogo de propiedades
                # de Ature en Acrobat Reader
                "application": 'Firmado con SICPRO ERP',
            }


dct1 = {
                "aligned": 0,
                "sigflags": 3,
                "sigflagsft": 132,
                "sigpage": pagina_firma,
                "auto_sigfield": True,
                "signaturebox": coordenadas,
                "signform": False,
                "sigfield": "Signature",
                "text": {'wraptext': True, 'fontsize': 18, 'textalign': 'left', 'linespacing': 1.2, },
                "signature_appearance": {
                    #'background': [0.75, 0.8, 0.95],
                    'icon': img_firma,
                    #s'outline': [0.2, 0.3, 0.5],
                    #'border': 2,
                    'labels': False,
                    'display': 'contact,date'.split(','),
                },
                "contact": contacto,
                "location": "Cuba",
                "signingdate": fecha,
                "reason": "Firmado con SICPRO ERP. DVPE - ETECSA",
                "password": password,
            }

