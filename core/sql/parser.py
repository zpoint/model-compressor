"""
parse table creation to syntax tree

help:
https://stackoverflow.com/questions/1394998/parsing-sql-with-python

"""

d_table: dict = dict()
d_curr: dict = dict()


class TableParser(object):
    @staticmethod
    def parse_table(s, loc, tok):
        global d_table, d_curr
        tok = TableParser.remove_quotes(s, loc, tok)
        if tok not in d_table:
            d_table[tok] = dict()
            d_curr = d_table[tok]
        return tok

    @staticmethod
    def parse_col(s, loc, tok):
        if "cols" not in d_curr:
            d_curr["cols"] = list()
        ret_dict = dict()
        for i in tok:
            ret_dict.update(i)
        d_curr["cols"].append(ret_dict)
        return ret_dict

    @staticmethod
    def parse_field_name(s, loc, tok):
        tok = TableParser.remove_quotes(s, loc, tok)
        return {"field_name": tok}

    @staticmethod
    def parse_field_type(s, loc, tok):
        return {"field_type": tok[0]}

    @staticmethod
    def parse_field_length(s, loc, tok):
        tok = TableParser.get_int(s, loc, tok)
        return {"field_length": tok}

    @staticmethod
    def parse_nullable(s, loc, tok):
        if tok == "NULL":
            null = True
        else:
            null = False
        return {"null": null}

    @staticmethod
    def parse_default_value(s, loc, tok):
        return {"default": tok[1]}

    @staticmethod
    def parse_comment(s, loc, tok):
        return {"comment": "".join(tok[1])}

    @staticmethod
    def parse_auto_inc(s, loc, tok):
        return {"auto_inc": True}

    @staticmethod
    def parse_table_attr(s, loc, tok):
        return {"table_attr": tok}

    @staticmethod
    def get_int(s, loc, tok):
        if tok[0] == "(":
            return tok[1]
        return tok[0]

    @staticmethod
    def remove_quotes(s, loc, tok):
        if tok[0] in ("'", '"', "`"):
            return "".join(tok[1:-1])
        return "".join(tok)

    @staticmethod
    def parse_table_def(s, loc, tok):
        origin_tok = tok
        tok = list(tok)
        equal_index = tok.index("=")
        left = tok[equal_index-1]
        right = tok[equal_index+1]
        d_curr[left] = right
        return origin_tok
