from django.db import models

CHOICES_ASSUNTO = [
    ('', 'Selecione um assunto'),
    ('descontos', 'Descontos'),
    ('consultoria', 'Consultoria'),
    ('elogios', 'Elogios'),
    ('reclamações', 'Reclamações'),
    ('outros', 'Outros'),
]


class Contact(models.Model):
    assunto = models.CharField(
        choices=CHOICES_ASSUNTO, default="", max_length=100
    )
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mensagem = models.TextField(max_length=1000)

    class Meta:
        db_table = 'contato'
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"

    def __str__(self):
        return self.nome
