from ..output import OutPut


class PeeWeeOutPut(OutPut):
    field_type_map = {
        "VARCHAR": "CharField",
        "INT": "IntegerField",
        "TINYINT": "SmallIntegerField",
        "CHAR": "CharField",
        "DATE": "DateField",
        "DATETIME": "DateTimeField"
    }

    def emit_table(self) -> str:
        ret_str = ""
        for table_name, table_dict in self.sql_table_dict.items():
            if self.lower_case:
                table_name = table_name.lower()

            self.reset_indent()
            ret_str = self.emit_table_cls(table_name)
            self.forward_indent()
            for col in table_dict["cols"]:
                ret_str += self.emit_row(col)
            ret_str += self.emit_table_meta(table_name)
            self.backward_indent()
        return ret_str

    def emit_row(self, row_dict: dict) -> str:
        default = None
        if "default" in row_dict:
            default = row_dict["default"]

        key = self.strip_func(row_dict["field_name"])
        if row_dict["field_type"] == "TINYINT" and row_dict["field_length"] == 1:
            field_type = "BooleanField"
            if default:
                default = repr(bool(row_dict["default"]))
        else:
            field_type = self.field_type_map[row_dict["field_type"]]
        ret_str = self.indent + "%s = peewee.%s(%s" % (key, field_type, self.br)
        # max_length
        if field_type == "CharField" and "field_length" in self.field_type_map:
            ret_str += self.next_indent + "max_length=%s,%s" % (row_dict["field_length"], self.br)
        # verbose_name
        if "comment" in row_dict:
            ret_str += self.next_indent + "verbose_name=\"%s\",%s" % (row_dict["comment"], self.br)
        # null
        if "null" in row_dict:
            ret_str += self.next_indent + "null=\"%s\",%s" % (repr(bool(row_dict["null"])), self.br)
        # default
        if default is not None:
            ret_str += self.next_indent + "default=%s,%s" % (default, self.br)
        # db_column
        ret_str += self.next_indent + "db_column=\"%s\")%s" % (key, self.br*2)
        return ret_str

    def emit_table_cls(self, table_name):
        table_name = self.strip_table_func(table_name)
        ret_str = "class %s(%s):\n" % (table_name, self.base_model_name)
        return ret_str

    def emit_table_meta(self, table_name):
        ret_str = "%sclass Meta:%s" % (self.indent, self.br)
        ret_str += "%s%s = %s%s" % (self.next_indent, "table_name", table_name, self.br)
        ret_str += "%s%s = %s%s" % (self.next_indent, "database", "db", self.br)
        return ret_str