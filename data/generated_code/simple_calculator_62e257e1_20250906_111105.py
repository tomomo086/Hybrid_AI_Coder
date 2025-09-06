"""
生成日時: 2025-09-06T11:11:05.287649
命令書ID: 62e257e1-5ba4-4060-ae8c-3b2f84016325
機能名: simple_calculator
生成AI: DeepSeek-Coder
"""

def simple_calculator(operation: str, a: float, b: float) -> dict:
    """
    電卓の基本的な演算を実行する関数。
    
    Args:
        operation (str): 'add', 'subtract', 'multiply', 'divide'のいずれか。
        a (float): 第一オペランド。
        b (float): 第二オペランド。
    
    Returns:
        dict: {'result': float, 'operation': str, 'operands': [a, b]}の形式で、演算結果と操作およびオペランドを返す。
    
    Raises:
        ValueError: 無効なoperationの場合、a, bが数値に変換可能でない場合、bが0で'divide'操作の場合。
    
    Examples:
        simple_calculator('add', 2.0, 3.0) -> {'result': 5.0, 'operation': 'add', 'operands': [2.0, 3.0]}
        simple_calculator('subtract', 2.0, 3.0) -> {'result': -1.0, 'operation': 'subtract', 'operands': [2.0, 3.0]}
    """
    
    if operation not in ['add', 'subtract', 'multiply', 'divide']:
        raise ValueError("無効な演算。許可される値は'add', 'subtract', 'multiply', 'divide'")
    
    try:
        a = float(a)
        b = float(b)
    except ValueError as e:
        raise ValueError("無効なオペランド。両方の値を数値に変換可能である必要があります") from e
    
    if operation == 'divide' and b == 0:
        raise ValueError("除算不可。第二オペランドは0にできません")
    
    result = None
    
    if operation == 'add':
        result = a + b
    elif operation == 'subtract':
        result = a - b
    elif operation == 'multiply':
        result = a * b
    else:  # operation == 'divide'
        result = a / b
    
    return {'result': result, 'operation': operation, 'operands': [a, b]}