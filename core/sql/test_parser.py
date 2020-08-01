from core.sql.create_parser import defs, d_table
from core.sql.output.peewee import PeeWeeOutPut

sampleSQL = """
""".upper()
res = defs.parseString(sampleSQL)
for k, v in d_table.items():
    print(k, v)
    for k, v in v.items():
        print(k, v)

for each in list(d_table.values())[0]["cols"]:
    print(each)

output = PeeWeeOutPut(d_table)
r = output.emit_table()
print(r)
