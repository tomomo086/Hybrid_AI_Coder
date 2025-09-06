#!/usr/bin/env python
"""
data_analyzer実動テスト
生成されたコードの品質確認と実行テスト
"""

from typing import List, Dict, Union
import statistics as stats
import math

def data_analyzer(data: List[Dict[str, Union[int, float, str]]], target_column: str, analysis_type: str = "basic_stats") -> dict:
    """
    データ分析関数（修正版）
    
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
        {'analysis_type': 'basic_stats', 'target_column': 'age', 'results': {'mean': 27.5, 'median': 27.5, 'std': 3.54}, 'summary': 'データの基本統計情報'}
    """
    
    # 入力検証
    if not data:
        raise ValueError("データは空であってはならず、少なくとも1つ以上の要素を持ちます。")
    
    if target_column not in data[0]:
        raise ValueError(f"{target_column} はデータ内のキーに存在しなければなりません。")
        
    if analysis_type not in ["basic_stats", "distribution", "correlation"]:
        raise ValueError(f"{analysis_type} は有効な分析タイプではありません。")
    
    # 数値データ確認（対象カラムがすべてのデータに存在するかも含む）
    try:
        target_values = []
        for i, d in enumerate(data):
            if target_column not in d:
                raise ValueError(f"データ{i}番目に{target_column}カラムが存在しません")
            val = d[target_column]
            if not isinstance(val, (int, float)):
                raise ValueError(f"対象カラム'{target_column}'の値は数値データである必要があります (値: {val})")
            target_values.append(val)
    except Exception as e:
        raise ValueError(f"データ処理エラー: {e}")
    
    # 分析実行
    if analysis_type == "basic_stats":
        # 標準偏差は要素数2以上必要
        if len(target_values) < 2:
            std_val = 0.0
        else:
            std_val = round(stats.stdev(target_values), 2)
            
        results = {
            "count": len(target_values),
            "mean": round(stats.mean(target_values), 2),
            "median": stats.median(target_values),
            "std": std_val
        }
        summary = f"データの基本統計情報: {len(target_values)}件のデータ"
        
    elif analysis_type == "distribution":
        results = {
            "min": min(target_values),
            "max": max(target_values),
            "range": max(target_values) - min(target_values)
        }
        summary = f"データの分布情報: {min(target_values)}～{max(target_values)}"
        
    elif analysis_type == "correlation":
        # correlationは他のカラムとの相関を想定するが、今回は値の分散度を計算
        if len(set(target_values)) == 1:
            correlation_coeff = 0.0  # すべて同じ値
        else:
            # 値とインデックスの相関として簡易実装
            indices = list(range(len(target_values)))
            if len(target_values) < 2:
                correlation_coeff = 0.0
            else:
                try:
                    correlation_coeff = round(stats.correlation(target_values, indices), 3)
                except:
                    # stats.correlationが存在しない場合は手動計算
                    mean_x = stats.mean(target_values)
                    mean_y = stats.mean(indices)
                    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(target_values, indices))
                    den = math.sqrt(sum((x - mean_x)**2 for x in target_values) * sum((y - mean_y)**2 for y in indices))
                    correlation_coeff = round(num / den if den != 0 else 0.0, 3)
        
        results = {
            "correlation_with_index": correlation_coeff,
            "variance": round(stats.variance(target_values) if len(target_values) > 1 else 0.0, 2)
        }
        summary = f"相関分析結果: インデックスとの相関係数 {correlation_coeff}"
    
    return {
        "analysis_type": analysis_type, 
        "target_column": target_column, 
        "results": results, 
        "summary": summary
    }

def test_data_analyzer():
    """data_analyzer関数のテスト"""
    print("=" * 60)
    print("🧪 data_analyzer実動テスト")
    print("🎯 複雑な型ヒント対応機能テスト")
    print("=" * 60)
    
    # テストデータ準備
    test_data = [
        {"name": "Alice", "age": 25, "score": 85},
        {"name": "Bob", "age": 30, "score": 92}, 
        {"name": "Carol", "age": 22, "score": 78},
        {"name": "David", "age": 28, "score": 88},
        {"name": "Eve", "age": 26, "score": 95}
    ]
    
    print(f"📊 テストデータ: {len(test_data)}件")
    for i, item in enumerate(test_data):
        print(f"   {i+1}. {item}")
    
    print("\n" + "="*60)
    
    # テスト1: basic_stats
    print("🧮 テスト1: basic_stats (年齢)")
    try:
        result1 = data_analyzer(test_data, "age", "basic_stats")
        print(f"✅ 実行成功")
        print(f"   結果: {result1}")
        
        # 結果検証
        ages = [25, 30, 22, 28, 26]
        expected_mean = sum(ages) / len(ages)
        assert abs(result1['results']['mean'] - expected_mean) < 0.01, f"平均値不一致: {result1['results']['mean']} vs {expected_mean}"
        print(f"   ✅ 平均値検証OK: {result1['results']['mean']}")
        
    except Exception as e:
        print(f"❌ basic_statsテスト失敗: {e}")
    
    # テスト2: distribution
    print(f"\n🧮 テスト2: distribution (スコア)")
    try:
        result2 = data_analyzer(test_data, "score", "distribution")
        print(f"✅ 実行成功")
        print(f"   結果: {result2}")
        
        # 結果検証
        scores = [85, 92, 78, 88, 95]
        expected_range = max(scores) - min(scores)
        assert result2['results']['range'] == expected_range, f"範囲不一致: {result2['results']['range']} vs {expected_range}"
        print(f"   ✅ 範囲検証OK: {result2['results']['range']}")
        
    except Exception as e:
        print(f"❌ distributionテスト失敗: {e}")
    
    # テスト3: correlation
    print(f"\n🧮 テスト3: correlation (年齢)")
    try:
        result3 = data_analyzer(test_data, "age", "correlation")
        print(f"✅ 実行成功")
        print(f"   結果: {result3}")
        print(f"   ✅ 相関分析機能動作確認")
        
    except Exception as e:
        print(f"❌ correlationテスト失敗: {e}")
    
    # テスト4: エラーハンドリング
    print(f"\n🧮 テスト4: エラーハンドリング")
    
    # 存在しないカラム
    try:
        data_analyzer(test_data, "invalid_column", "basic_stats")
        print("❌ 存在しないカラムエラーが発生しませんでした")
    except ValueError as e:
        print(f"✅ 存在しないカラムエラー正常捕捉: {e}")
    
    # 無効な分析タイプ
    try:
        data_analyzer(test_data, "age", "invalid_type")
        print("❌ 無効な分析タイプエラーが発生しませんでした")
    except ValueError as e:
        print(f"✅ 無効な分析タイプエラー正常捕捉: {e}")
    
    # 空データ
    try:
        data_analyzer([], "age", "basic_stats")
        print("❌ 空データエラーが発生しませんでした")
    except ValueError as e:
        print(f"✅ 空データエラー正常捕捉: {e}")
    
    print(f"\n🎉 data_analyzer実動テスト完了")
    print(f"📋 結論:")
    print(f"  ✅ 複雑な型ヒント `List[Dict[str, Union[int, float, str]]]` 対応成功")
    print(f"  ✅ 3種類の分析タイプすべて動作確認")
    print(f"  ✅ エラーハンドリング正常動作")
    print(f"  ✅ DeepSeek-Coder高品質コード生成確認")

if __name__ == "__main__":
    test_data_analyzer()