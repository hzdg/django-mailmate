from mailmate import TemplatedEmailMessage


def test_template():
    class Email(TemplatedEmailMessage):
        template_name = 'body.txt'

    assert Email(extra_context={'name': 'world'}).body.strip() == 'hello world'
