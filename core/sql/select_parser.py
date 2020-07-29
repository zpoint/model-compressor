#!/usr/bin/python

# sql2dot.py
#
#  Creates table graphics by parsing SQL table DML commands and
#  generating DOT language output.
#
#  Adapted from a post at https://energyblog.blogspot.com/2006/04/blog-post_20.html.
#  https://noahgilmore.com/blog/pyparsing-trees/
#
sampleSQL = """CREATE TABLE `t_verify_people_device` 
(
`c_id` INT(64) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `c_company_id` varchar(32) NOT NULL COMMENT '企业Id',
  `c_fields` varchar(300) NOT NULL DEFAULT "" COMMENT '字段信息',
    `c_is_delete` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除',
  `c_auto_del_delay` tinyint(3) NOT NULL DEFAULT -1 COMMENT '延时',
    PRIMARY KEY (`c_id`),
  KEY `ix_company` (`c_company_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='表格名称';
""".upper()

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
    Optional
)


sub_keyword = Word(alphas, alphanums + "_\"':-")
keyword = ("`" + sub_keyword + "`") | sub_keyword
skobki = "(" + ZeroOrMore(CharsNotIn(")")) + ")"
string = QuotedString("'") | QuotedString('"')
number = (Optional("-") + Word(nums))
field_def = OneOrMore(keyword | skobki | QuotedString("'") | QuotedString('"') | number)
table_def = OneOrMore(OneOrMore(sub_keyword) + "=" + (sub_keyword | string | number))


def field_act(s, loc, tok):
    # print("s", s, "loc", loc, "tok", tok)
    return [tok]
    # return ("<" + tok[0] + "> " + " ".join(tok)).replace('"', '\\"')


field_def.setParseAction(field_act)

field_list_def = delimitedList(field_def)


def field_list_act(toks):
    return [toks]


field_list_def.setParseAction(field_list_act)

create_table_def = (
    Literal("CREATE")
    + "TABLE"
    + keyword.setResultsName("tablename")
    + "("
    + field_list_def.setResultsName("columns")
    + ")"
    + table_def.setResultsName("tabledef")
    + ";"
)


def create_table_act(toks):
    print("toks", toks)
    return (
        """"%(tablename)s" [\n\t label="<%(tablename)s> %(tablename)s | %(columns)s"\n\t shape="record"\n];"""
        % toks
    )


create_table_def.setParseAction(create_table_act)

add_fkey_def = (
    Literal("ALTER")
    + "TABLE"
    + "ONLY"
    + Word(alphanums + "_").setResultsName("fromtable")
    + "ADD"
    + "CONSTRAINT"
    + Word(alphanums + "_")
    + "FOREIGN"
    + "KEY"
    + "("
    + Word(alphanums + "_").setResultsName("fromcolumn")
    + ")"
    + "REFERENCES"
    + Word(alphanums + "_").setResultsName("totable")
    + "("
    + Word(alphanums + "_").setResultsName("tocolumn")
    + ")"
    + ";"
)


def add_fkey_act(toks):
    return """ "%(fromtable)s":%(fromcolumn)s -> "%(totable)s":%(tocolumn)s """ % toks


add_fkey_def.setParseAction(add_fkey_act)

other_statement_def = OneOrMore(CharsNotIn(";")) + ";"
other_statement_def.setParseAction(replaceWith(""))
comment_def = "--" + ZeroOrMore(CharsNotIn("\n"))
comment_def.setParseAction(replaceWith(""))

statement_def = create_table_def  # comment_def | create_table_def | add_fkey_def | other_statement_def
defs = OneOrMore(statement_def)

for i in defs.parseString(sampleSQL):
    print(i)
#
# print("""digraph g { graph [ rankdir = "LR" ]; """)
# for i in defs.parseString(sampleSQL):
#     if i != "":
#         print(i)
# print("}")
