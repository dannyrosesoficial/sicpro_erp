
Uso
=====

Para enviar una notificación al usuario solo necesita llamar a uno de los nuevos métodos definidos en res.users:

.. code-block:: python

   self.env.user.notify_success(message='El mensaje a enviar')

   self.env.user.notify_danger(message='El mensaje a enviar')

   self.env.user.notify_warning(message='El mensaje a enviar')

   self.env.user.notify_info(message='El mensaje a enviar')

   self.env.user.notify_default(message='El mensaje a enviar')
