from core.sql.create_parser import defs, d_table
from core.sql.output.peewee import PeeWeeOutPut

sampleSQL = """CREATE TABLE `t_district` (
  `c_id` int(11) NOT NULL AUTO_INCREMENT,
  `c_administrative_code` varchar(12) DEFAULT NULL COMMENT '行政区代码',
  `c_pid` int(11) NOT NULL DEFAULT '0',
  `c_full_name` varchar(60) NOT NULL COMMENT '区域名称',
  `c_name` varchar(30) DEFAULT NULL COMMENT '名称',
  `c_merger_name` varchar(200) DEFAULT NULL,
  `c_pinyin` varchar(60) DEFAULT NULL COMMENT '拼音',
  `c_pinyin_lite` varchar(30) DEFAULT NULL COMMENT '拼音简称',
  `c_level` tinyint(3) NOT NULL DEFAULT '1' COMMENT '级别：1省 2市 3区',
  `c_is_municipal_district` tinyint(1) NOT NULL DEFAULT '0' COMMENT '市辖区',
  `c_is_county_level_city` tinyint(1) DEFAULT '0' COMMENT '是否县级市',
  `c_sort` int(11) DEFAULT NULL,
  `c_population` decimal(10,2) DEFAULT NULL COMMENT '人口(万人)',
  `c_gdp` decimal(10,2) DEFAULT NULL COMMENT 'GDP(亿元)',
  `c_is_deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`c_id`) USING BTREE,
  KEY `ix_name_key` (`c_name`) USING BTREE,
  KEY `ix_pinyin_key` (`c_pinyin`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3047349 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
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
