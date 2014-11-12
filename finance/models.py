from django.db import models
from django.utils.translation import ugettext_lazy as _


class Ticker(models.Model):
    """ Model to store Company name and it's assosiated ticker name, which
        would be used by our API to extract relevent data."""
    
    company_name = models.CharField(max_length=256)
    ticker = models.CharField(max_length=32)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('ticker')
        verbose_name_plural = _('tickers')
        db_table = 'ticker'

    def get_name(self):
        return '{0}'.format(self.company_name)
    
    def __unicode__(self):
        return "{0}".format(self.ticker)
