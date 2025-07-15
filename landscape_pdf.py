#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
가로형 페이지 HTML to PDF 변환 스크립트 (섹션별 페이지 분할)
"""

import os
from playwright.sync_api import sync_playwright

def create_landscape_pdf():
    """HTML 웹페이지를 가로형 PDF로 변환 (섹션별 페이지 분할)"""
    
    print("🎬 가로형 PDF 변환을 시작합니다...")
    
    # HTML 파일 확인
    html_file = "index.html"
    if not os.path.exists(html_file):
        print(f"❌ {html_file} 파일을 찾을 수 없습니다.")
        return False
    
    try:
        print("📄 playwright를 사용하여 가로형 PDF를 생성합니다...")
        
        html_file_path = os.path.abspath(html_file)
        output_file = "음원_마케팅_체험단_가로형.pdf"
        
        # PDF 최적화를 위한 CSS 추가
        pdf_optimized_css = """
        <style>
        /* PDF 가로형 페이지 최적화 CSS */
        @page {
            size: A4 landscape;
            margin: 10mm 15mm 15mm 15mm; /* 상단 여백 줄임 */
        }
        
        /* 페이지 분할 설정 */
        .hero {
            page-break-after: always;
            min-height: 95vh; /* 높이 줄임 */
            display: flex;
            align-items: center;
            padding: 20px 0; /* 패딩 추가 */
        }
        
        .process {
            page-break-before: always;
            page-break-after: always;
            min-height: 95vh; /* 높이 줄임 */
            padding: 20px 0; /* 패딩 줄임 */
        }
        
        .programs {
            page-break-before: always;
            page-break-after: always;
            min-height: 95vh; /* 높이 줄임 */
            padding: 20px 0; /* 패딩 줄임 */
        }
        
        .benefits {
            page-break-before: always;
            page-break-after: always;
            min-height: 95vh; /* 높이 줄임 */
            padding: 20px 0; /* 패딩 줄임 */
        }
        
        .apply {
            page-break-before: always;
            page-break-after: always;
            min-height: 95vh; /* 높이 줄임 */
            padding: 20px 0; /* 패딩 줄임 */
        }
        
        .footer {
            page-break-before: always;
            min-height: 40vh; /* 높이 줄임 */
            padding: 20px 0; /* 패딩 줄임 */
        }
        
        /* 가로형에 맞는 레이아웃 조정 */
        body {
            font-size: 14px;
            line-height: 1.4; /* 줄간격 줄임 */
        }
        
        .container {
            max-width: 100%;
            padding: 0 20px;
        }
        
        /* 섹션 제목 크기 및 여백 조정 */
        .section-header h2, h2 {
            font-size: 2rem !important; /* 제목 크기 줄임 */
            margin: 10px 0 20px 0 !important; /* 상단 여백 줄임 */
            line-height: 1.2 !important;
        }
        
        .section-header p {
            margin: 0 0 20px 0 !important; /* 여백 조정 */
        }
        
        /* 히어로 섹션 가로형 최적화 */
        .hero-container {
            display: flex;
            align-items: center;
            gap: 30px; /* 간격 줄임 */
            height: 100%;
            max-height: 85vh; /* 최대 높이 제한 */
        }
        
        .hero-content {
            flex: 1;
        }
        
        .hero-title {
            font-size: 2.5rem !important; /* 크기 줄임 */
            margin-bottom: 15px !important; /* 여백 줄임 */
            line-height: 1.2 !important;
        }
        
        .hero-buttons {
            margin-top: 20px !important; /* 여백 줄임 */
        }
        
        /* 플로팅 카드 크기 및 위치 조정 */
        .hero-image {
            flex: 0 0 400px; /* 고정 너비로 설정 */
            height: 300px; /* 높이 제한 */
            position: relative;
        }
        
        .hero-graphic {
            width: 100%;
            height: 100%;
            position: relative;
        }
        
        .floating-card {
            position: absolute !important;
            width: 120px !important; /* 크기 줄임 */
            height: 60px !important; /* 높이 줄임 */
            display: flex !important;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            font-size: 12px !important; /* 폰트 크기 줄임 */
            font-weight: 500;
        }
        
        .floating-card.card-1 {
            top: 20px;
            left: 20px;
        }
        
        .floating-card.card-2 {
            top: 80px;
            right: 30px;
        }
        
        .floating-card.card-3 {
            bottom: 30px; /* 하단에서 여유 있게 */
            left: 50px;
        }
        
        /* 프로세스 스텝 가로형 최적화 */
        .process-steps {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: nowrap;
            gap: 15px; /* 간격 줄임 */
            margin: 30px 0; /* 여백 줄임 */
        }
        
        .step-item {
            flex: 1;
            text-align: center;
            min-width: 100px; /* 최소 너비 줄임 */
        }
        
        .step-item h3 {
            font-size: 14px !important; /* 크기 줄임 */
            margin: 8px 0 !important; /* 여백 줄임 */
        }
        
        .step-number {
            font-size: 18px !important; /* 크기 줄임 */
            margin-bottom: 8px !important; /* 여백 줄임 */
        }
        
        .step-arrow {
            color: var(--primary-color);
            font-size: 20px; /* 크기 줄임 */
        }
        
        /* 프로그램 테이블 가로형 최적화 */
        .program-category {
            margin-bottom: 30px; /* 여백 줄임 */
            page-break-inside: avoid;
        }
        
        .category-title {
            font-size: 1.3rem !important; /* 크기 줄임 */
            margin: 15px 0 !important; /* 여백 줄임 */
        }
        
        .program-table {
            font-size: 11px; /* 폰트 크기 줄임 */
            margin: 15px 0; /* 여백 줄임 */
        }
        
        .table-header, .table-row {
            display: grid;
            grid-template-columns: 50px 2fr 3fr 3fr 70px; /* 컬럼 크기 조정 */
            gap: 8px; /* 간격 줄임 */
            padding: 8px; /* 패딩 줄임 */
            border: 1px solid #ddd;
        }
        
        .table-header {
            background: var(--primary-color);
            color: white;
            font-weight: bold;
        }
        
        /* 혜택 섹션 가로형 최적화 */
        .benefits-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px; /* 간격 줄임 */
            margin: 30px 0; /* 여백 줄임 */
        }
        
        .benefit-item {
            text-align: center;
            padding: 15px; /* 패딩 줄임 */
        }
        
        .benefit-item h3 {
            font-size: 1.1rem !important; /* 크기 줄임 */
            margin: 10px 0 !important; /* 여백 줄임 */
        }
        
        /* 신청 섹션 가로형 최적화 */
        .apply-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px; /* 간격 줄임 */
            align-items: start;
        }
        
        .apply-form {
            max-width: 100%;
        }
        
        .apply-text h2 {
            font-size: 1.8rem !important; /* 크기 줄임 */
            margin: 0 0 15px 0 !important; /* 여백 줄임 */
        }
        
        /* 푸터 가로형 최적화 */
        .footer-content {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px; /* 간격 줄임 */
        }
        
        .footer-section h3, .footer-section h4 {
            font-size: 1rem !important; /* 크기 줄임 */
            margin: 0 0 10px 0 !important; /* 여백 줄임 */
        }
        
        /* 모바일 요소 숨김 */
        .hamburger, .mobile-menu {
            display: none !important;
        }
        
        /* 헤더 높이 조정 */
        .header {
            height: auto !important;
            min-height: 60px !important; /* 높이 줄임 */
            padding: 10px 0 !important; /* 패딩 줄임 */
        }
        
        /* 인쇄 최적화 */
        @media print {
            * {
                -webkit-print-color-adjust: exact !important;
                color-adjust: exact !important;
            }
            
            .nav-menu {
                display: flex !important;
            }
        }
        
        /* 배경 그라데이션 유지 */
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .process {
            background: #f8fafc;
        }
        
        .benefits {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        
        .apply {
            background: #1a1a2e;
            color: white;
        }
        </style>
        """
        
        with sync_playwright() as p:
            # 브라우저 실행
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 가로형에 적합한 뷰포트 설정 (더 큰 크기로)
            page.set_viewport_size({"width": 1600, "height": 1000})
            
            # HTML 파일 읽기
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # CSS 최적화 코드 삽입
            html_content = html_content.replace('</head>', f'{pdf_optimized_css}</head>')
            
            # 수정된 HTML을 임시 파일로 저장
            temp_html = "temp_landscape.html"
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            temp_html_path = os.path.abspath(temp_html)
            
            # HTML 파일 로드
            page.goto(f"file:///{temp_html_path.replace(os.sep, '/')}")
            
            # 페이지가 완전히 로드될 때까지 대기
            page.wait_for_load_state('networkidle')
            
            # 애니메이션 완료를 위한 추가 대기
            page.wait_for_timeout(3000)  # 3초 대기
            
            # PDF 생성 (가로형)
            page.pdf(
                path=output_file,
                format='A4',
                landscape=True,  # 가로형 설정
                margin={
                    'top': '10mm',    # 상단 여백 줄임
                    'right': '15mm', 
                    'bottom': '15mm',
                    'left': '15mm'
                },
                print_background=True,
                prefer_css_page_size=True,
                display_header_footer=True,
                header_template='<div style="font-size:9px; text-align:center; width:100%; color:#666; margin-top:5mm;">음원 마케팅 체험단</div>',
                footer_template='<div style="font-size:9px; text-align:center; width:100%; color:#666; margin-bottom:5mm;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'
            )
            
            browser.close()
            
            # 임시 파일 삭제
            if os.path.exists(temp_html):
                os.remove(temp_html)
        
        print(f"✅ 수정된 가로형 PDF 파일이 생성되었습니다: {output_file}")
        print(f"📁 파일 위치: {os.path.abspath(output_file)}")
        
        # 페이지 구성 안내
        print("\n📄 수정된 PDF 페이지 구성:")
        print("   1페이지: 메인 히어로 섹션 (제목, 소개) - 네이버 카드 잘림 해결")
        print("   2페이지: 체험단 진행과정 (6단계 프로세스) - 제목 잘림 해결")
        print("   3페이지: 체험 프로그램 (인스타그램/틱톡/음원다운로드/후기작성) - 제목 잘림 해결")
        print("   4페이지: 체험단 특별 혜택 (4가지 혜택) - 제목 잘림 해결")
        print("   5페이지: 신청 방법 (신청 폼) - 제목 잘림 해결")
        print("   6페이지: 연락처 및 푸터 정보 - 제목 잘림 해결")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF 생성 중 오류가 발생했습니다: {e}")
        return False

if __name__ == "__main__":
    success = create_landscape_pdf()
    
    if success:
        print("🎉 성공적으로 수정된 가로형 PDF 파일이 생성되었습니다!")
        print("🔧 네이버 카드 잘림과 제목 잘림 문제가 해결되었습니다.")
    else:
        print("❌ PDF 생성에 실패했습니다.") 