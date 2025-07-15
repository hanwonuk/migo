#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
음원 마케팅 체험단 웹페이지 PDF 변환 스크립트
HTML 파일과 CSS 스타일을 그대로 유지하면서 PDF로 변환합니다.
"""

import os
import sys
from pathlib import Path

def create_pdf_from_html():
    """HTML 웹페이지를 PDF로 변환"""
    
    print("🔄 HTML to PDF 변환을 시작합니다...")
    
    # 현재 디렉토리의 HTML 파일 확인
    html_file = "index.html"
    if not os.path.exists(html_file):
        print(f"❌ {html_file} 파일을 찾을 수 없습니다.")
        return False
    
    try:
        # weasyprint 사용
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
        
        print("📄 weasyprint를 사용하여 PDF를 생성합니다...")
        
        # 폰트 설정
        font_config = FontConfiguration()
        
        # HTML 파일 읽기
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 추가 CSS (PDF 최적화)
        pdf_css = CSS(string='''
            @page {
                size: A4;
                margin: 20mm;
                @bottom-center {
                    content: "음원 마케팅 체험단 - " counter(page);
                    font-size: 10pt;
                    color: #666;
                }
            }
            
            body {
                font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
                line-height: 1.4;
            }
            
            /* 페이지 나누기 최적화 */
            .hero-section, .process-section, .program-section, 
            .benefits-section, .application-section {
                page-break-inside: avoid;
                margin-bottom: 30px;
            }
            
            /* 모바일 스타일 비활성화 */
            @media print {
                .mobile-menu-btn { display: none !important; }
                .mobile-menu { display: none !important; }
                .floating-elements { position: static !important; }
                .floating-card { 
                    position: static !important; 
                    transform: none !important;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
                    margin: 10px;
                    display: inline-block;
                }
            }
            
            /* 테이블 스타일 보정 */
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                page-break-inside: avoid;
            }
            
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
                font-size: 12px;
            }
            
            /* 프로세스 스텝 레이아웃 조정 */
            .process-steps {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 10px;
            }
            
            .process-step {
                width: 150px;
                min-height: 80px;
                margin: 5px;
            }
        ''', font_config=font_config)
        
        # PDF 생성
        output_file = "음원_마케팅_체험단.pdf"
        
        html_doc = HTML(string=html_content, base_url=Path.cwd().as_uri())
        html_doc.write_pdf(
            output_file, 
            stylesheets=[pdf_css],
            font_config=font_config,
            optimize_images=True
        )
        
        print(f"✅ PDF 파일이 생성되었습니다: {output_file}")
        print(f"📁 파일 위치: {os.path.abspath(output_file)}")
        return True
        
    except ImportError:
        print("❌ weasyprint가 설치되지 않았습니다. pdfkit을 시도합니다...")
        return create_pdf_with_pdfkit()
    except Exception as e:
        print(f"❌ weasyprint로 PDF 생성 실패: {e}")
        print("🔄 pdfkit을 시도합니다...")
        return create_pdf_with_pdfkit()

def create_pdf_with_pdfkit():
    """pdfkit을 사용한 PDF 생성 (대안)"""
    
    try:
        import pdfkit
        
        print("📄 pdfkit을 사용하여 PDF를 생성합니다...")
        
        # HTML 파일 경로
        html_file = os.path.abspath("index.html")
        output_file = "음원_마케팅_체험단.pdf"
        
        # PDF 옵션 설정
        options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None,
            'disable-smart-shrinking': None,
            'footer-center': '음원 마케팅 체험단 - [page]',
            'footer-font-size': '10'
        }
        
        # PDF 생성
        pdfkit.from_file(html_file, output_file, options=options)
        
        print(f"✅ PDF 파일이 생성되었습니다: {output_file}")
        print(f"📁 파일 위치: {os.path.abspath(output_file)}")
        return True
        
    except ImportError as e:
        print("❌ pdfkit이 설치되지 않았습니다.")
        print("💡 다음 중 하나를 설치해주세요:")
        print("   - pip install weasyprint")
        print("   - pip install pdfkit")
        print("   - pdfkit 사용 시 wkhtmltopdf도 별도 설치 필요")
        return False
    except Exception as e:
        print(f"❌ pdfkit으로 PDF 생성 실패: {e}")
        return create_pdf_with_playwright()

def create_pdf_with_playwright():
    """playwright를 사용한 PDF 생성 (최후 대안)"""
    
    try:
        from playwright.sync_api import sync_playwright
        
        print("📄 playwright를 사용하여 PDF를 생성합니다...")
        
        html_file = os.path.abspath("index.html")
        output_file = "음원_마케팅_체험단.pdf"
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # HTML 파일 로드
            page.goto(f"file://{html_file}")
            
            # 페이지가 완전히 로드될 때까지 대기
            page.wait_for_load_state('networkidle')
            
            # PDF 생성
            page.pdf(
                path=output_file,
                format='A4',
                margin={
                    'top': '20mm',
                    'right': '20mm', 
                    'bottom': '20mm',
                    'left': '20mm'
                },
                print_background=True,
                prefer_css_page_size=True
            )
            
            browser.close()
        
        print(f"✅ PDF 파일이 생성되었습니다: {output_file}")
        print(f"📁 파일 위치: {os.path.abspath(output_file)}")
        return True
        
    except ImportError:
        print("❌ playwright가 설치되지 않았습니다.")
        print("💡 다음 명령어로 설치해주세요:")
        print("   pip install playwright")
        print("   playwright install")
        return False
    except Exception as e:
        print(f"❌ playwright로 PDF 생성 실패: {e}")
        return False

if __name__ == "__main__":
    print("🎬 음원 마케팅 체험단 웹페이지 PDF 변환을 시작합니다...")
    
    success = create_pdf_from_html()
    
    if success:
        print("🎉 성공적으로 PDF 파일이 생성되었습니다!")
        print("\n📋 생성된 파일:")
        print("   - 음원_마케팅_체험단.pdf (웹페이지 PDF 버전)")
        if os.path.exists("음원_마케팅_체험단.pptx"):
            print("   - 음원_마케팅_체험단.pptx (PPT 버전)")
    else:
        print("❌ PDF 생성에 실패했습니다.")
        print("\n🔧 해결 방법:")
        print("1. weasyprint 설치: pip install weasyprint")
        print("2. 또는 pdfkit 설치: pip install pdfkit + wkhtmltopdf 설치")
        print("3. 또는 playwright 설치: pip install playwright && playwright install") 