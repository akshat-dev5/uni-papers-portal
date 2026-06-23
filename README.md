# uni-papers-portal
End-to-End University Question Paper Processing and Solution Generation Platform

# Watermark Removal API

## Endpoint

### Remove Watermark from PDF

**POST**

```http
/api/watermark/remove
```

---

## Request Body

```json
{
  "pdfUrl": "https://example.com/question-paper.pdf"
}
```

### Parameters

| Field  | Type   | Required | Description                      |
| ------ | ------ | -------- | -------------------------------- |
| pdfUrl | string | Yes      | Public URL of the PDF to process |

---

## Success Response

**HTTP 200**

```json
{
  "status": "success",
  "downloadUrl": "/downloads/doc_001_clean.pdf"
}
```

### Response Fields

| Field       | Type   | Description                     |
| ----------- | ------ | ------------------------------- |
| status      | string | Request status                  |
| downloadUrl | string | URL to download the cleaned PDF |

---

## Error Response

**HTTP 400**

```json
{
  "error": "pdfUrl is required"
}
```

**HTTP 500**

```json
{
  "error": "Watermark removal failed"
}
```

---

## Example cURL

```bash
curl -X POST http://localhost:5000/api/watermark/remove \
-H "Content-Type: application/json" \
-d '{
  "pdfUrl":"https://cdn.example.com/sample.pdf"
}'
```

---

## Download Clean PDF

After processing completes, open:

```http
http://localhost:5000/downloads/doc_001_clean.pdf
```

The generated PDF is served through the `/downloads` route configured in the backend.

```
```
