from import_export.widgets import Widget


# Taken from https://github.com/django-import-export/django-import-export/issues/525#issuecomment-303046691
class ChoicesWidget(Widget):
    """
    Widget that uses choice display values in place of database values
    """

    # pylint:disable=unused-argument
    def __init__(self, choices, *args, **kwargs):
        """
        Creates a self.choices dict with a key, display value, and value,
        db value, e.g. {'Chocolate': 'CHOC'}
        """
        self.choices = dict(choices)
        self.revert_choices = dict((v, k) for k, v in self.choices.items())

    def clean(self, value, row=None, *args, **kwargs):
        """Returns the db value given the display value"""
        return self.revert_choices.get(value, value) if value else None

    def render(self, value, obj=None):
        """Returns the display value given the db value"""
        return self.choices.get(value, '')

