import os
import mimetypes

from django.http import StreamingHttpResponse
from django.views import View
from django.views.generic import TemplateView


class StreamingResponseView(View):
    file_name = None
    http_method = 'get'

    def get_generator(self):
        raise NotImplementedError('The method is not implemented')

    def get_filename(self):
        return self.file_name

    def __get_response(self, *args, **kwargs):
        self.__is_not_used(*args, **kwargs)

        generator = self.get_generator()
        if generator is None:
            raise RuntimeError('File generator was not got')

        file_name = getattr(generator, 'name', None) or self.get_filename()
        if not isinstance(file_name, str) or len(file_name) == 0:
            raise RuntimeError('File name was not found')

        file_size = getattr(generator, 'size', None)

        mimetype = mimetypes.guess_type(os.path.basename(file_name))[0]
        response = StreamingHttpResponse(generator, content_type=mimetype)
        if file_size is not None:
            response['Content-Length'] = file_size
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
        return response

    def get(self, *args, **kwargs):
        return self.__get_response(*args, **kwargs)

    def __is_not_used(self, *args, **kwargs):
        pass


class IndexView(TemplateView):
    template_name = 'Dashboard/index.html'
