from core.sql.create_parser import defs, d_table
from core.sql.output.peewee import PeeWeeOutPut

sampleSQL = """CREATE TABLE `t_verify_people_device` 
(
`c_id` INT(64) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `c_company_id` varchar(32) NOT NULL COMMENT '企业Id',
  `c_fields` varchar(300) NOT NULL DEFAULT "" COMMENT '字段信息',
    `c_is_delete` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除',
  `c_auto_del_delay` tinyint(3) NOT NULL DEFAULT -1 COMMENT '延时',
    state varchar(2),
    zipcode varchar(10),
    dob date,
    PRIMARY KEY (`c_id`),
  KEY `ix_company` (`c_company_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='表格名称';
""".upper()
res = defs.parseString(sampleSQL)
for k, v in d_table.items():
    print(k, v)

for each in list(d_table.values())[0]["cols"]:
    print(each)

output = PeeWeeOutPut(d_table)
r = output.emit_table()
print(r)
