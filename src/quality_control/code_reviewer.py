"""
コード品質管理システム

生成されたコードの品質評価と改善提案を行う
"""

import re
import ast
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
from loguru import logger


class CodeReviewer:
    """コード品質レビューアー"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enable_security_check = config.get("enable_security_check", True)
        self.enable_performance_check = config.get("enable_performance_check", True) 
        self.enable_style_check = config.get("enable_style_check", True)
        
        # チェックリスト読み込み
        checklist_path = config.get("review_checklist_path", "config/review_checklist.json")
        self.checklist = self._load_checklist(checklist_path)
        
    def _load_checklist(self, path: str) -> Dict[str, Any]:
        """レビューチェックリストを読み込み"""
        checklist_file = Path(path)
        if checklist_file.exists():
            try:
                with open(checklist_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"チェックリスト読み込みエラー: {e}")
                
        # デフォルトチェックリスト
        return self._get_default_checklist()
        
    def _get_default_checklist(self) -> Dict[str, Any]:
        """デフォルトチェックリスト"""
        return {
            "security": {
                "sql_injection": ["sql", "query", "execute", "cursor"],
                "command_injection": ["os.system", "subprocess", "eval", "exec"],
                "file_traversal": ["../", "..\\", "open(", "file("],
                "hardcoded_secrets": ["password", "api_key", "secret", "token"]
            },
            "performance": {
                "inefficient_patterns": ["nested_loops", "redundant_operations"],
                "memory_leaks": ["unclosed_files", "circular_references"],
                "algorithm_complexity": ["O(n^2)", "O(n^3)"]
            },
            "style": {
                "naming_conventions": ["snake_case", "UPPER_CASE"],
                "documentation": ["docstring", "type_hints"],
                "code_structure": ["function_length", "complexity"]
            }
        }
        
    def review_code(self, code: str, function_name: str = "") -> Dict[str, Any]:
        """コードの総合レビュー"""
        logger.info(f"コードレビュー開始: {function_name}")
        
        review_result = {
            "function_name": function_name,
            "review_date": datetime.now().isoformat(),
            "overall_score": 0,
            "issues": {
                "critical": [],
                "major": [],
                "minor": []
            },
            "suggestions": [],
            "compliance": {},
            "metrics": {}
        }
        
        try:
            # AST解析で構文チェック
            tree = ast.parse(code)
            review_result["syntax_valid"] = True
            
            # 各種チェック実行
            if self.enable_security_check:
                security_issues = self._check_security(code)
                review_result["issues"]["critical"].extend(security_issues)
                
            if self.enable_performance_check:
                performance_issues = self._check_performance(code, tree)
                review_result["issues"]["major"].extend(performance_issues)
                
            if self.enable_style_check:
                style_issues = self._check_style(code, tree)
                review_result["issues"]["minor"].extend(style_issues)
                
            # コードメトリクス計算
            review_result["metrics"] = self._calculate_metrics(code, tree)
            
            # 総合スコア計算
            review_result["overall_score"] = self._calculate_score(review_result)
            
            # 改善提案生成
            review_result["suggestions"] = self._generate_suggestions(review_result)
            
        except SyntaxError as e:
            logger.error(f"構文エラー: {e}")
            review_result["syntax_valid"] = False
            review_result["issues"]["critical"].append({
                "type": "syntax_error",
                "message": f"構文エラー: {str(e)}",
                "line": e.lineno if hasattr(e, 'lineno') else 0
            })
            
        except Exception as e:
            logger.error(f"レビュー処理エラー: {e}")
            review_result["error"] = str(e)
            
        logger.info(f"コードレビュー完了: スコア {review_result['overall_score']}")
        return review_result
        
    def _check_security(self, code: str) -> List[Dict[str, Any]]:
        """セキュリティチェック"""
        issues = []
        security_patterns = self.checklist["security"]
        
        # SQLインジェクション
        for pattern in security_patterns["sql_injection"]:
            if pattern in code.lower():
                issues.append({
                    "type": "security",
                    "severity": "critical",
                    "category": "sql_injection",
                    "message": f"SQLインジェクションの可能性: '{pattern}' が検出されました",
                    "recommendation": "パラメータ化クエリを使用してください"
                })
                
        # コマンドインジェクション
        for pattern in security_patterns["command_injection"]:
            if pattern in code:
                issues.append({
                    "type": "security",
                    "severity": "critical",
                    "category": "command_injection", 
                    "message": f"コマンドインジェクションの可能性: '{pattern}' が検出されました",
                    "recommendation": "入力値の検証とエスケープを行ってください"
                })
                
        # ハードコードされた秘密情報
        for pattern in security_patterns["hardcoded_secrets"]:
            if re.search(f'{pattern}\\s*=\\s*["\'][^"\']+["\']', code, re.IGNORECASE):
                issues.append({
                    "type": "security",
                    "severity": "major",
                    "category": "hardcoded_secrets",
                    "message": f"ハードコードされた秘密情報: '{pattern}' が検出されました", 
                    "recommendation": "環境変数や設定ファイルを使用してください"
                })
                
        return issues
        
    def _check_performance(self, code: str, tree: ast.AST) -> List[Dict[str, Any]]:
        """パフォーマンスチェック"""
        issues = []
        
        # ネストしたループの検出
        nested_loops = self._find_nested_loops(tree)
        if nested_loops > 2:
            issues.append({
                "type": "performance",
                "severity": "major", 
                "category": "nested_loops",
                "message": f"深いネストループ (深度: {nested_loops}) が検出されました",
                "recommendation": "アルゴリズムの見直しを検討してください"
            })
            
        # リソースリークの検出
        if "open(" in code and "with open(" not in code:
            issues.append({
                "type": "performance",
                "severity": "major",
                "category": "resource_leak", 
                "message": "ファイルが適切にクローズされていない可能性があります",
                "recommendation": "with文を使用してファイルを開いてください"
            })
            
        return issues
        
    def _check_style(self, code: str, tree: ast.AST) -> List[Dict[str, Any]]:
        """スタイルチェック"""
        issues = []
        
        # 関数の長さチェック
        long_functions = self._find_long_functions(tree)
        for func_name, line_count in long_functions:
            if line_count > 50:
                issues.append({
                    "type": "style",
                    "severity": "minor",
                    "category": "function_length",
                    "message": f"関数 '{func_name}' が長すぎます ({line_count} 行)",
                    "recommendation": "関数を分割することを検討してください"
                })
                
        # ドキュメント文字列チェック
        missing_docstrings = self._find_missing_docstrings(tree)
        for func_name in missing_docstrings:
            issues.append({
                "type": "style",
                "severity": "minor",
                "category": "documentation",
                "message": f"関数 '{func_name}' にdocstringがありません",
                "recommendation": "関数の説明を追加してください"
            })
            
        return issues
        
    def _find_nested_loops(self, tree: ast.AST) -> int:
        """ネストしたループの深さを検出"""
        max_depth = 0
        
        class LoopVisitor(ast.NodeVisitor):
            def __init__(self):
                self.current_depth = 0
                self.max_depth = 0
                
            def visit_For(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1
                
            def visit_While(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1
                
        visitor = LoopVisitor()
        visitor.visit(tree)
        return visitor.max_depth
        
    def _find_long_functions(self, tree: ast.AST) -> List[Tuple[str, int]]:
        """長い関数を検出"""
        long_functions = []
        
        class FunctionVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                line_count = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                long_functions.append((node.name, line_count))
                self.generic_visit(node)
                
        visitor = FunctionVisitor()
        visitor.visit(tree)
        return long_functions
        
    def _find_missing_docstrings(self, tree: ast.AST) -> List[str]:
        """docstringがない関数を検出"""
        missing_docs = []
        
        class DocstringVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                has_docstring = (
                    len(node.body) > 0 and
                    isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant) and
                    isinstance(node.body[0].value.value, str)
                )
                
                if not has_docstring:
                    missing_docs.append(node.name)
                    
                self.generic_visit(node)
                
        visitor = DocstringVisitor()
        visitor.visit(tree)
        return missing_docs
        
    def _calculate_metrics(self, code: str, tree: ast.AST) -> Dict[str, Any]:
        """コードメトリクスを計算"""
        lines = code.split('\n')
        
        return {
            "lines_of_code": len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
            "total_lines": len(lines),
            "comment_lines": len([line for line in lines if line.strip().startswith('#')]),
            "blank_lines": len([line for line in lines if not line.strip()]),
            "function_count": len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]),
            "class_count": len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
        }
        
    def _calculate_score(self, review_result: Dict[str, Any]) -> int:
        """総合スコアを計算（0-100）"""
        base_score = 100
        
        # 重大度別の減点
        critical_issues = len(review_result["issues"]["critical"])
        major_issues = len(review_result["issues"]["major"]) 
        minor_issues = len(review_result["issues"]["minor"])
        
        score = base_score - (critical_issues * 30) - (major_issues * 15) - (minor_issues * 5)
        
        # 構文エラーがある場合は大幅減点
        if not review_result.get("syntax_valid", True):
            score = min(score, 20)
            
        return max(0, min(100, score))
        
    def _generate_suggestions(self, review_result: Dict[str, Any]) -> List[str]:
        """改善提案を生成"""
        suggestions = []
        
        critical_count = len(review_result["issues"]["critical"])
        major_count = len(review_result["issues"]["major"])
        
        if critical_count > 0:
            suggestions.append(f"🚨 {critical_count}件の重大な問題があります。セキュリティの観点から即座に対応が必要です。")
            
        if major_count > 0:
            suggestions.append(f"⚠️ {major_count}件の重要な問題があります。パフォーマンスや保守性の改善を検討してください。")
            
        score = review_result["overall_score"]
        if score >= 80:
            suggestions.append("✨ 全体的に高品質なコードです。")
        elif score >= 60:
            suggestions.append("👍 概ね良好なコードです。軽微な改善で品質向上が期待できます。")
        else:
            suggestions.append("🔧 コードの大幅な見直しが推奨されます。")
            
        return suggestions