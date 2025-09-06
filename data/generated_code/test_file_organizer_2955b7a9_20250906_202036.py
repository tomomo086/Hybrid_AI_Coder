"""
生成日時: 2025-09-06T20:20:36.039231
命令書ID: 2955b7a9-d587-48d7-9c9d-41843462b3e3
機能名: test_file_organizer
生成AI: DeepSeek-Coder
"""

import os
from typing import List, Tuple

def test_file_organizer(directory: str) -> Tuple[List[str], List[str]]:
    """ディレクトリ内のファイルとディレクトリを整理する関数。
    
    Args:
        directory (str): 対象のディレクトリ
        
    Returns:
        Tuple[List[str], List[str]]: ファイルとディレクトリのリスト。
    
    Raises:
        FileNotFoundError: 指定したディレクトリが存在しない場合。
    """
    if not os.path.isdir(directory):
        raise FileNotFoundError('指定されたパスは存在しません')
    
    files = []  # type: List[str]
    dirs = []   # type: List[str]
    
    for item in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, item)):
            files.append(item)
        elif os.path.isdir(os.path.join(directory, item)):
            dirs.append(item)
            
    return (files, dirs)