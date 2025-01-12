from markitdown import MarkItDown

if __name__ == '__main__':
    md = MarkItDown()
    result = md.convert("/Users/57block/pythonproject/test-genie/files/2025-01-11 08:12:34.273559-Cobo Invoice MVP PRD（中文版）.docx")
    print(result.text_content)