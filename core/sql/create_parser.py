from pyparsing import (
    Literal,
    Word,
    delimitedList,
    alphas,
    alphanums,
    OneOrMore,
    ZeroOrMore,
    CharsNotIn,
    replaceWith,
    QuotedString,
    nums,
    Optional,
    sglQuotedString,
    quotedString,
    removeQuotes,
)

from pyparsing import pyparsing_common
from core.sql.parser import TableParser, d_table


def field_act(s, loc, tok):
    # print("s", s, "loc", loc, "tok", tok)
    print(tok)
    return [tok]


# tablename
word = Word(alphas, alphanums + "_")
keyword = ("`" + word + "`") | word
keyword = keyword.setParseAction(TableParser.remove_quotes)
string_literal = quotedString.setParseAction(removeQuotes)
number = pyparsing_common.number()

# column
type_ = Literal("CHAR") | Literal("VARCHAR") | Literal("TINYTEXT") | Literal("TEXT") | Literal("MEDIUMTEXT") | \
        Literal("LONGTEXT") | Literal("TINYINT") | Literal("SMALLINT") | Literal("MEDIUMINT") | Literal("INT") | \
        Literal("BIGINT") | Literal("FLOAT") | Literal("DOUBLE") | Literal("DECIMAL") | Literal("DATE") | Literal("DATETIME") | \
        Literal("TIMESTAMP") | Literal("TIME") | Literal("ENUM") | Literal("SET") | Literal("BLOB")
enclosing_int = "(" + number + ")"
enclosing_keyword = "(" + OneOrMore(keyword) + ")"
nullable = Literal("NOT NULL") | Literal("NULL")
default = Literal("DEFAULT") + (string_literal | number)
comment = Literal("COMMENT") + string_literal
auto_inc = Literal("AUTO_INCREMENT")

enclosing_int.setParseAction(TableParser.parse_field_length)
keyword.setParseAction(TableParser.parse_field_name)
type_.setParseAction(TableParser.parse_field_type)
nullable.setParseAction(TableParser.parse_nullable)
auto_inc.setParseAction(TableParser.parse_auto_inc)
default.setParseAction(TableParser.parse_default_value)
comment.setParseAction(TableParser.parse_comment)
col_stm = keyword + type_ + Optional(enclosing_int) + Optional(nullable) + Optional(auto_inc) + Optional(default) + Optional(comment)
col_stm.setParseAction(TableParser.parse_col)

# key
using_stm = Literal("USING") + word
key = Optional(Literal("PRIMARY")) + Literal("KEY") + Optional(keyword) + enclosing_keyword
key.setParseAction(TableParser.parse_table_attr)
key_stm = key + Optional(using_stm)

cols_def = delimitedList(col_stm | key_stm)

# table
origin_keyword = ("`" + word + "`") | word
single_table_def = OneOrMore(origin_keyword) + "=" + (origin_keyword | string_literal | number)
single_table_def.setParseAction(TableParser.parse_table_def)
table_def = OneOrMore(single_table_def)


table_name = ("`" + word + "`") | word
table_name = table_name.setParseAction(TableParser.remove_quotes)
table_name.setParseAction(TableParser.parse_table)
create_table_def = (
    Literal("CREATE")
    + "TABLE"
    + table_name.setResultsName("tablename")
    + "("
    + cols_def.setResultsName("columns")
    + ")"
    + table_def.setResultsName("tabledef")
    + ";"
)

statement_def = create_table_def
defs = OneOrMore(statement_def)
