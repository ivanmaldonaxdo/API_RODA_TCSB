from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings

class OverwriteStorage(FileSystemStorage):
    '''
    Cambia el comportamiento predeterminado de Django y realiza sobrescritura de
    del nombre o ruta del archivo.
    '''
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name