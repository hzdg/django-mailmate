from django.core.mail.backends.filebased import EmailBackend
import email

class CleanEmailBackend(EmailBackend):
    """ Takes email messages and splits there parts into clean messages """

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

