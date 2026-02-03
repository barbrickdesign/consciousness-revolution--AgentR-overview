# ARAYA FILE WRITER - QUICK START

**Status:** LIVE AND TESTED (7/7 tests pass)
**Server:** http://localhost:5001
**Security:** Locked to 100X_DEPLOYMENT folder only

---

## START THE SERVER

**Option 1: Desktop launcher**
```
Double-click: Desktop/START_ARAYA_FILE_WRITER.bat
```

**Option 2: Command line**
```bash
cd C:/Users/dwrek/100X_DEPLOYMENT
python ARAYA_FILE_WRITER.py
```

Server runs on **port 5001** (ARAYA API is on 8000)

---

## ENDPOINTS

### 1. Write File (CREATE/OVERWRITE)
```javascript
fetch('http://localhost:5001/write-file', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        file_path: 'test.html',
        content: '<h1>Hello World</h1>',
        action: 'write'
    })
})
```

### 2. Append to File
```javascript
fetch('http://localhost:5001/write-file', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        file_path: 'test.html',
        content: '\n<p>New line</p>',
        action: 'append'
    })
})
```

### 3. Edit File (FIND/REPLACE)
```javascript
fetch('http://localhost:5001/write-file', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        file_path: 'test.html',
        action: 'edit',
        old_string: 'Hello World',
        new_string: 'Hello ARAYA'
    })
})
```

### 4. Read File
```javascript
fetch('http://localhost:5001/read-file', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        file_path: 'test.html'
    })
})
```

### 5. List Files
```javascript
fetch('http://localhost:5001/list-files', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        dir_path: '.'  // or any subdirectory
    })
})
```

### 6. Health Check
```javascript
fetch('http://localhost:5001/health')
```

---

## SECURITY

- **LOCKED:** Only writes within `C:/Users/dwrek/100X_DEPLOYMENT`
- **TESTED:** Blocks writes to Desktop, Documents, etc.
- **CORS enabled:** Can call from browser/ARAYA

---

## FILE PATHS

**Relative paths:** Auto-converted to 100X_DEPLOYMENT
```javascript
file_path: 'test.html'  // → C:/Users/dwrek/100X_DEPLOYMENT/test.html
```

**Absolute paths:** Must be within 100X_DEPLOYMENT
```javascript
file_path: 'C:/Users/dwrek/100X_DEPLOYMENT/test.html'  // ✅ OK
file_path: 'C:/Users/dwrek/Desktop/test.html'  // ❌ BLOCKED (403)
```

---

## RESPONSE FORMAT

**Success:**
```json
{
    "success": true,
    "file_path": "C:/Users/dwrek/100X_DEPLOYMENT/test.html",
    "action": "write",
    "size": 160,
    "timestamp": "2025-12-24T19:19:28.652964"
}
```

**Error:**
```json
{
    "error": "Security violation: Path outside allowed root",
    "path": "C:/Users/dwrek/Desktop/HACKER.txt",
    "allowed_root": "C:/Users/dwrek/100X_DEPLOYMENT"
}
```

---

## TEST IT

```bash
cd C:/Users/dwrek/100X_DEPLOYMENT
python TEST_FILE_WRITER.py
```

Should show: **7/7 tests passed**

---

## NEXT: INTEGRATE WITH ARAYA

Add to `araya-chat.html`:

```javascript
async function writeFile(filePath, content, action='write') {
    const response = await fetch('http://localhost:5001/write-file', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            file_path: filePath,
            content: content,
            action: action
        })
    });
    return await response.json();
}
```

Then ARAYA can actually edit the website!
