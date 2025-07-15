#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 HTML to PDF 변환 스크립트 (playwright 사용)
"""

import os
from playwright.sync_api import sync_playwright

def create_pdf():
    """HTML 웹페이지를 PDF로 변환"""
    
    print("🎬 HTML to PDF 변환을 시작합니다...")
    
    # HTML 파일 확인
    html_file = "index.html"
    if not os.path.exists(html_file):
        print(f"❌ {html_file} 파일을 찾을 수 없습니다.")
        return False
    
    try:
        print("📄 playwright를 사용하여 PDF를 생성합니다...")
        
        html_file_path = os.path.abspath(html_file)
        output_file = "음원_마케팅_체험단.pdf"
        
        with sync_playwright() as p:
            # 브라우저 실행
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 뷰포트 설정 (데스크톱 크기)
            page.set_viewport_size({"width": 1200, "height": 800})
            
            # HTML 파일 로드
            page.goto(f"file:///{html_file_path.replace(os.sep, '/')}")
            
            # 페이지가 완전히 로드될 때까지 대기
            page.wait_for_load_state('networkidle')
            
            # 애니메이션 완료를 위한 추가 대기
            page.wait_for_timeout(2000)  # 2초 대기
            
            # PDF 생성
            page.pdf(
                path=output_file,
                format='A4',
                margin={
                    'top': '15mm',
                    'right': '15mm', 
                    'bottom': '15mm',
                    'left': '15mm'
                },
                print_background=True,
                prefer_css_page_size=False,
                display_header_footer=True,
                header_template='<div style="font-size:10px; text-align:center; width:100%;">음원 마케팅 체험단</div>',
                footer_template='<div style="font-size:10px; text-align:center; width:100%;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'
            )
            
            browser.close()
        
        print(f"✅ PDF 파일이 생성되었습니다: {output_file}")
        print(f"📁 파일 위치: {os.path.abspath(output_file)}")
        return True
        
    except Exception as e:
        print(f"❌ PDF 생성 중 오류가 발생했습니다: {e}")
        return False

if __name__ == "__main__":
    success = create_pdf()
    
    if success:
        print("🎉 성공적으로 PDF 파일이 생성되었습니다!")
    else:
        print("❌ PDF 생성에 실패했습니다.") 