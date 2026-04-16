# File Uploads

Estimated time: 90 minutes

## 1. Definition

FastAPI handles file uploads through **`UploadFile`**, which wraps the multipart form data in an async-friendly interface. `File()` is the corresponding metadata helper. Multiple files can be uploaded in a single request using `List[UploadFile]`.

### Key Characteristics

- **`UploadFile`**: provides `filename`, `content_type`, and async methods `read()`, `write()`, `seek()`, `close()`.
- **Async reads**: `await file.read()` does not block the event loop.
- **MIME type validation**: `file.content_type` carries the declared MIME type (verify it, don't trust it alone).
- **`File(...)`**: marks an argument as multipart form data.
- **Size limits**: enforce manually by checking `len(contents)` after reading.

## 2. Practical Application

### Use Cases

- Profile picture upload with image type validation.
- Document upload (PDF, CSV) for processing pipelines.
- Batch upload of multiple files in one request.
- Streaming large files to disk without buffering entirely in memory.

### Code Example

```python
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()

@app.post("/upload/image", status_code=201)
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(415, "Only JPEG/PNG accepted")
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

## 3. Why Is It Important?

### Problem It Solves

File uploads involve multipart form encoding, MIME type detection, size enforcement, and async I/O — none of which are trivial to handle correctly with raw ASGI.

### Solution and Benefits

`UploadFile` abstracts all of that behind a clean async interface. FastAPI parses multipart boundaries, populates metadata, and makes the file stream available without buffering.

## 4. References

- [FastAPI File Uploads](https://fastapi.tiangolo.com/tutorial/request-files/)
- [UploadFile reference](https://fastapi.tiangolo.com/reference/uploadfile/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create `POST /upload` that accepts a single `UploadFile`, reads it, and returns `filename`, `content_type`, and `size_bytes`.

### Intermediate Level

Validate that the uploaded file is a JPEG or PNG, reject files larger than 2 MB, and save the file to `/tmp/uploads/` with a UUID-prefixed name.

### Advanced Level

Create `POST /upload/batch` accepting `List[UploadFile]` (max 5). Return a summary with per-file status (success or error reason), total uploaded bytes, and count.

### Success Criteria

- Uploading a `.txt` file to the image endpoint returns 415.
- A file over 2 MB returns 413.
- Batch upload reports per-file results without aborting on a single failure.

## 6. Summary

`UploadFile` is the FastAPI primitive for multipart file uploads. It provides async file reads, filename and content type metadata, and integrates with the same validation pipeline as other request inputs. Always validate MIME type and size at the application level.

## 7. Reflection Prompt

Why is it insufficient to trust `file.content_type` alone when validating uploaded files? What additional checks would you perform to prevent malicious file uploads in a production system?
