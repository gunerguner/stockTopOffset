"""数值格式化与单位转换"""


def to_billions(value: float) -> float:
    """将美元数值转换为十亿美元（B）单位。"""
    return float(value) / 1e9
