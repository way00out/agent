import os
import datetime
from typing import Optional
from fastmcp import FastMCP
from markitdown import MarkItDown


mcp = FastMCP(
    name="Document-Parsing-Automation-Server",
    instructions="다양한 형식 (PDF, Word, Excel, PPT)의 문서를 파싱하여 통일된 표준 마크다운 양식으로 반환합니다."
)

md_parser = MarkItDown()


def format_to_standard_markdown(
        doc_id: str,
        doc_type: str,
        domain: str,
        file_path: str,
        raw_markdown_content: str
) -> str:
    """
    파싱된 원본 텍스트를 통일된 4단계 표준 마크다운 포맷으로 변환합니다.
    """
    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_name)[1].upper().replace(".", "")
    today = datetime.date.today().strftime("%Y-%m-%d")

    standard_template = f"""# [표준 정제 문서] {file_name}

## 1. 메타데이터 (Document Metadata)
- **문서 ID**: {doc_id}
- **문서 종류**: {doc_type}
- **도메인**: {domain}
- **작성일 및 정제일**: {today}
- **원본 파일 경로**: {file_path}
- **원본 파일 형식**: {file_ext}


---

## 2. 문서 요약 (Executive Summary)
> 본 문서는 '{file_name}' 파일로부터 자동 추출 및 정제된 마크다운 문서입니다.


---

## 3. 본문 상세 내용 (Main Content)

{raw_markdown_content}


---

## 4. 부록 및 참조 (Appendix)
- **파싱 엔진**: MarkItDown + FastMCP Automation
- **상태**: 파싱 성공 (Parsing Completed)
"""
    return standard_template


@mcp.tool()
def parse_and_nomalize_document(
    file_path: str,
    doc_id: Optional[str] = "DOC-AUTO-001",
    doc_type: Optional[str] = "일반 산출물/문서",
    domain: Optional[str] = "설비관리/재고관리"
) -> str:
    """
    지정된 경로의 문서(PDF, Word, Excel, PPT 등)을 파싱하여 통일 표준 마크다운으로 반환합니다.
    
    Args:
        file_path: 파싱할 대상 파일의 전체 경로 (예: ./sample.docx, /data/report.pdf)
        doc_id: 문서 식별 ID (예: DOC-REQ-001)
        doc_type: 문서 종류 (예: 요구사항 정의서, 기능 명세서, 예지보전 보고서)
        domain: 도메인 분류 (예: 재고관리, 설비관리)
    """
    if not os.path.exists(file_path):
        return f"오류: 지정한 파일 경로를 찾을 수 없습니다 -> {file_path}"

    try:
        result = md_parser.convert(file_path)
        raw_md = result.text_content

        normalized_md = format_to_standard_markdown(
            doc_id=doc_id,
            doc_type=doc_type,
            domain=domain,
            file_path=file_path,
            raw_markdown_content=raw_md
        )

        return normalized_md

    except Exception as e:
        return f"문서 파싱 중 오류가 발생했습니다: {str(e)}"


    @mcp.tool()
    def batch_parse_directory(dir_path: str, domain: str = "공통") -> str:
        """
        디렉토리 내의 모든 문서(PDF, DOCX, XLSX, PPTX)를 일괄 파싱하여 요약 리포트를 반환합니다.
        """
        if not os.path.exists(dir_path):
            return f"오류: 디렉토리를 찾을 수 없습니다 -> {dir_path}"

        supported_extensions = ('.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.md')
        parsed_results = []

        idx = 1
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.lower().endswith(supported_extensions):
                    full_path = os.path.join(root, file)
                    doc_id = f"DOC-BATCH-{idx:03d}"
                    res = parse_and_nomalize_document(
                        file_path=full_path,
                        doc_id=doc_id,
                        doc_type="일괄 파싱 문서",
                        domain=domain
                    )
                    parsed_results.append(res)
                    idx += 1

        summary_header = f"# 디렉토리 일괄 파싱 완료 보고서\n- 대상 폴더: '{dir_path}'\n- 총 파싱 파일 수: {len(parsed_results)}개\n\n"
        return summary_header + "\n\n" + ("=" * 50) + "\n\n".join(parsed_results)



if __name__ == "__main__":
    mcp.run(transport="stdio")