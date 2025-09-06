"""
生成日時: 2025-09-06T16:17:38.817595
命令書ID: 9ea46229-d0bf-49ca-907a-352aac7c7339
機能名: batch_processor
生成AI: DeepSeek-Coder
"""

import concurrent.futures
import asyncio
from src.core.instruction_manager import InstructionManager
from src.workflow.executor import Executor
import logging
import time

def batch_processor(instruction_ids, operation, parallel=True):
    start = time.time()
    success = 0
    failed = 0
    details = []
    
    # エラーハンドリングのための例外定義
    class InstructionNotFoundError(Exception): pass
    class InvalidOperationError(Exception): pass
    class BatchProcessingError(Exception): pass
    
    # 入力検証
    if not instruction_ids:
        raise BatchProcessingError('instruction_idsは空ではないリストである必要があります。')
    
    # 操作名の検証
    if operation not in ['execute', 'validate', 'approve']:
        raise InvalidOperationError(f'操作 {operation} は無効です。')
        
    # 処理開始
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            
            for instruction_id in instruction_ids:
                future = executor.submit(process, instruction_id, operation)
                
                # 並列処理の場合、タスクを追加しない
                if not parallel:
                    loop.run_until_complete(asyncio.ensure_future(future))
            
            # 並列処理の場合、全てのタスクを待機
            if parallel:
                loop.run_until_complete(asyncio.wait(futures))
    
    except Exception as e:
        raise BatchProcessingError('バッチ処理中に予期しないエラーが発生しました。') from e
        
    finally:
        # 処理時間計測、結果の整形
        total_time = time.time() - start
        return {'success': success, 'failed': failed, 'details': details, 'total_time': total_time}
        
def process(instruction_id, operation):
    # 命令書IDが存在し、アクセス可能か検証
    if not InstructionManager.exists(instruction_id):
        raise InstructionNotFoundError(f'指定された命令書 {instruction_id} が見つかりません。')
    
    # 処理実行
    result = Executor.execute(operation, instruction_id)
    
    if result['status'] == 'success':
        success += 1
    else:
        failed += 1
        
    details.append({'id': instruction_id, 'status': result['status'], 'error': result.get('error')})