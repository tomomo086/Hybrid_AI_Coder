以下のPythonコードは、指定された仕様に従って`data_analyzer`関数を実装します。

```python
from typing import List, Dict, Union
import statistics as stats
import math

def data_analyzer(data: List[Dict[str, Union[int, float, str]]], target_column: str, analysis_type: str) -> dict:
    """
    データ分析関数。
    
    Args:
        data (List[Dict[str, Union[int, float, str]]]): 分析対象のデータリスト（辞書形式）
        target_column (str): 分析対象のカラム名
        analysis_type (str): 分析タイプ ('basic_stats', 'distribution', 'correlation')
    
    Returns:
        dict: {"analysis_type": str, "target_column": str, "results": dict, "summary": str}
        
    Raises:
        ValueError: 不正な分析タイプ、空のデータ、存在しないカラム名、非数値データ
    
    Examples:
        >>> data = [{"age": 25}, {"age": 30}]
        >>> data_analyzer(data, "age", "basic_stats")
        {'analysis_type': 'basic_stats', 'target_column': 'age', 'results': {'mean': 27.5, 'median': 27.5, 'std': 0}, 'summary': 'データの基本統計情報'}
    """
    
    # 入力検証
    if not data:
        raise ValueError("データは空であってはならず、少なくとも1つ以上の要素を持ちます。")
    if target_column not in data[0]:
        raise ValueError(f"{target_column} はデータ内のキーに存在しなければなりません。")
    if analysis_type not in ["basic_stats", "distribution", "correlation"]:
        raise ValueError(f"{analysis_type} は有効な分析タイプではありません。")
    if any(not isinstance(d[target_column], (int, float)) for d in data):
        raise ValueError("対象カラムの値は数値データである必要があります。")
    
    # 分析実行
    target_values = [d[target_column] for d in data]
    if analysis_type == "basic_stats":
        results = {
            "mean": stats.mean(target_values),
            "median": stats.median(target_values),
            "std": stats.stdev(target_values)
        }
        summary = "データの基本統計情報"
    elif analysis_type == "distribution":
        results = {
            "min": min(target_values),
            "max": max(target_values),
            "range": max(target_values) - min(target_values)
        }
        summary = "データの分布情報"
    elif analysis_type == "correlation":
        results = {
            "pearson": stats.correlation(target_values, [d[target_column] for d in data])
        }
        summary = "相関係数の計算結果"
    
    return {"analysis_type": analysis_type, "target_column": target_column, "results": results, "summary": summary}
```

このコードは、基本統計情報（平均値、中央値、標準偏差）、分布情報（最小値、最大値、範囲）、相関係数の3種類の分析を行う`data_analyzer`関数を定義します。
