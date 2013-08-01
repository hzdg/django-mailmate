from django.core.mail.backends.filebased import EmailBackend
import email
import mimetypes
import os


class CleanEmailBackend(EmailBackend):
    """ Takes email messages and splits there parts into clean messages """

    '''
            Example
            --------

            .. code-block:: python

            #settings.py
            EMAIL_BACKEND = 'mailmate.backends.CleanEmailBackend'
            EMAIL_FILE_PATH = os.path.join(PROJECT_DIR, '../tmp', 'app-messages')

            Any email that is sent will be put in the project directorys tmp dir
            under the apps-messages directory. It will have three files for
            every email.

            A log with the whole email in it, a html file if there is a html
            template and a txt file for a txt template.
    '''

    def _write_file(self, contents, ext):
        filename, old_ext = os.path.splitext(self._get_filename())
        output_filename = u'%s%s' % (filename, ext)
        fp = open(output_filename, 'w')
        fp.write(contents)
        fp.close()

    def _write_message(self, message, content_type='text/plain'):
        if message.is_multipart():
            for m in message.get_payload():
                self._write_message(m)
        else:
            content_type = message.get_content_type()
            ext = '.txt' if content_type == 'text/plain' else mimetypes.guess_extension(content_type)
            if ext:
                self._write_file(message.get_payload(decode=True), ext)

    def close(self):
        if self.stream is not None:
            message = email.message_from_file(open(self._get_filename(), 'r'))
            self._write_message(message)
        super(CleanEmailBackend, self).close()
