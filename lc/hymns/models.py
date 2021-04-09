from django.db import models

class TextBlock(models.Model):
    """Фрагмент последования /
        последование /
        богослужебная книга /
        полка книг"""
    parent_block    = models.ForeignKey('self', default=None, null=True, on_delete=models.CASCADE)
    name_long       = models.CharField(max_length=256, null=True, default=None)
    name_short      = models.CharField(max_length=32, null=True, default=None)
    path_long       = models.TextField(null=True, default=None)
    path_short      = models.TextField(null=True, default=None)
    order_id        = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.name_long

    def path_long(self):
        return self.path_long

    def update_path(self):
        self.path_long = parent_block.path_long() + "/" + self.path_long


class Paragraph(models.Model):
    """Абзац богослужебной книги"""
    txt             = models.TextField(null=True, default=None)
    txt_simplified  = models.TextField(null=True, default=None)
    parent_block    = models.ForeignKey(TextBlock, default=None, null=True, on_delete=models.CASCADE)
    order_id        = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.txt