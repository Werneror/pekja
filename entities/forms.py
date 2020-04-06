from django import forms
import inspect
import parse
from parse.parser import Parser


class ToolForm(forms.ModelForm):

    parse_class_name = forms.ChoiceField(choices=(), label='输出解析类')

    # 必须重写__init__方法，这样才能每次实例化表单时重新获取选项
    def __init__(self, *args, **kwargs):
        super(ToolForm, self).__init__(*args, **kwargs)
        self.fields['parse_class_name'].choices = ToolForm.get_parse_class_choices()

    @classmethod
    def get_parse_class_choices(cls):
        parse_class_list = [m[0] for m in inspect.getmembers(parse, inspect.isclass)
                            if issubclass(m[1], Parser) and m[0] != 'Parser']
        return tuple([(class_name, class_name) for class_name in parse_class_list])
