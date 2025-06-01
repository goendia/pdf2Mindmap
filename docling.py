from docling.document_converter import DocumentConverter

source = "1_DOCLING_1-2_CompTIA+Network++(N10-009)+Study+Guide.pdf" \
""  # PDF path or URL
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_dict())  # output: "### Docling Technical Report[...]"