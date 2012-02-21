from django.core.mail.backends.filebased import EmailBackend
import email

class CleanEmailBackend(EmailBackend):
    """ Takes email messages and splits there parts into clean messages """

    '''
            Example
            --------

            .. code-block:: python

            #settings.py
            EMAIL_BACKEND = 'emailtools.backend.CleanEmailBackend'
            EMAIL_FILE_PATH = os.path.join(PROJECT_DIR, '../tmp', 'app-messages')

            Any email that is sent will be put in the project directorys tmp dir
            under the apps-messages directory. It will have three files for 
            every email. 

            A log with the whole email in it, a html file if there is a html 
            template and a txt file for a txt template.
    '''

    def close(self):

        if self.stream is not None:
            messages = email.message_from_file(open(self._get_filename(), 'r'))

            for message in messages.get_payload():
                content_type = message.get_content_type()

                if content_type == 'text/html':
                    body = message.get_payload(decode=True)
                    file_suffix = 'html'

                elif content_type == 'text/plain':
                    body = message.as_string()
                    file_suffix = 'txt'

                output = open(self._get_filename().replace('log', file_suffix), 'w')
                output.write(body)

        super(CleanEmailBackend, self).close()

