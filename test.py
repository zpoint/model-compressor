# coding: utf-8

pattern = {
    "id": {"type": "uuid"},
    "emp_name": {"type": "char"},
    # default bool type must not be null, because bool will be represented as 0: false, 1: true, no bit left for null
    "has_children": {"type": "bool"},
    "has_mobile": {"type": "bool", "null": True},
    # 32 bit
    "sex": {"type": "int"},
    "mobile": {"type": "char"}
}

model1 = {

}

model2 = {

}


def test():
    # r1 = compress(model1)
    # r2 = compress(model2)
    # assert r1 ==
    # assert r2 ==
    pass
