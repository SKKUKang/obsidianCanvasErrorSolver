import os
import re
import json
import tkinter as tk
from tkinter import filedialog, messagebox

# 파일 검색 및 처리 함수
def fix_json_comma_error(file_path):
    try:
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 쉼표 뒤에 공백/줄바꿈이 있거나 바로 } 또는 ]이 오는 경우를 찾아 수정
        fixed_content, num_fixes = re.subn(r',\s*(\}|])|,(?=\}|])', r'\1', content)

        # JSON으로 로드 (JSON 파싱 에러를 방지)
        try:
            json.loads(fixed_content)  # 유효한 JSON인지 확인
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류 발생: {file_path}, {str(e)}")
            messagebox.showerror("JSON 오류", f"JSON 파싱 오류 발생: {file_path}\n{str(e)}")
            return 0  # 수정된 쉼표 수를 0으로 반환

        # 수정된 파일 저장
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(fixed_content)

        return num_fixes  # 수정된 쉼표 수 반환
    
    except Exception as e:
        print(f"오류 발생: {file_path}, {str(e)}")
        messagebox.showerror("오류", f"오류 발생: {file_path}\n{str(e)}")
        return 0  # 수정된 쉼표 수를 0으로 반환

# 파일 선택 및 처리 함수
def select_files():
    file_paths = filedialog.askopenfilenames(
        title="파일 선택",
        filetypes=[("Canvas Files", "*.canvas"), ("All Files", "*.*")]
    )

    total_fixes = 0
    if file_paths:  # 파일이 선택되었을 때
        for file_path in file_paths:
            num_fixes = fix_json_comma_error(file_path)
            total_fixes += num_fixes  # 총 수정된 쉼표 수 증가

        messagebox.showinfo("처리 완료", f"총 수정된 쉼표 수: {total_fixes}")

# GUI 창 생성
root = tk.Tk()
root.withdraw()  # 메인 윈도우 숨기기

# 파일 선택 대화 상자 열기
select_files()
