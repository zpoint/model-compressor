
class OutPut(object):
    def __init__(self, sql_table_dict: dict, lower_case=True, strip_func=None, indent="    ",
                 base_model_name="BaseModel"):
        self.sql_table_dict = sql_table_dict
        self.lower_case = lower_case
        self.strip_func = strip_func if strip_func else self.strip_func
        self.br = "\n"
        self.indent = indent
        self.current_indent = self.next_indent = ""
        self.base_model_name = base_model_name
        self.key_list = list()
        self.pk = None

    def emit_row(self, row_dict: dict) -> str:
        """
        :param row_dict: {'field_name': 'C_ID', 'field_type': 'INT', 'field_length': 64, 'null': False,
        'auto_inc': True, 'comment': '自增主键'}
        :return: str
        """
        raise NotImplementedError

    def emit_table(self) -> str:
        raise NotImplementedError

    def strip_func(self, key: str) -> str:
        if self.lower_case:
            key = key.lower()
        if key.startswith("c_"):
            key = key[2:]
        return key

    def forward_indent(self):
        if not self.next_indent:
            self.next_indent = self.indent
        self.current_indent = self.next_indent
        self.next_indent = self.current_indent + self.indent

    def backward_indent(self):
        self.current_indent = self.current_indent[:-len(self.indent)]
        self.next_indent = self.next_indent[:-len(self.indent)]

    def reset_indent(self):
        self.current_indent = self.next_indent = ""

    @staticmethod
    def strip_table_func(key: str) -> str:
        if key.startswith("t_"):
            key = key[2:]
        ret_key = ""
        key = key.split("_")
        for each in key:
            ret_key += each[0].upper()
            ret_key += each[1:]
        return ret_key

    def get_pk(self, table_dict):
        if "pk" in table_dict and table_dict["pk"]:
            self.pk = self.strip_func(table_dict["pk"])
            return
        self.pk = None
