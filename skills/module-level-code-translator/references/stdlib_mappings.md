# Standard Library Equivalences

Common standard library mappings between languages.

## File I/O

### Python → JavaScript (Node.js)
- `open(file, 'r')` → `fs.readFileSync(file, 'utf8')`
- `open(file, 'w')` → `fs.writeFileSync(file, data)`
- `os.path.join()` → `path.join()`
- `os.path.exists()` → `fs.existsSync()`

### Python → Java
- `open(file, 'r')` → `Files.readString(Path.of(file))`
- `open(file, 'w')` → `Files.writeString(Path.of(file), data)`
- `os.path.join()` → `Paths.get().toString()`

### Python → Go
- `open(file, 'r')` → `os.ReadFile(file)`
- `open(file, 'w')` → `os.WriteFile(file, data, 0644)`
- `os.path.join()` → `filepath.Join()`

## HTTP Requests

### Python → JavaScript
- `requests.get(url)` → `fetch(url)` or `axios.get(url)`
- `requests.post(url, json=data)` → `fetch(url, {method: 'POST', body: JSON.stringify(data)})`

### Python → Java
- `requests.get(url)` → `HttpClient.newHttpClient().send(request, BodyHandlers.ofString())`

### Python → Go
- `requests.get(url)` → `http.Get(url)`
- `requests.post(url, json=data)` → `http.Post(url, "application/json", bytes.NewBuffer(jsonData))`

## JSON Handling

### Python → JavaScript
- `json.loads(s)` → `JSON.parse(s)`
- `json.dumps(obj)` → `JSON.stringify(obj)`

### Python → Java
- `json.loads(s)` → `new ObjectMapper().readValue(s, Class)`
- `json.dumps(obj)` → `new ObjectMapper().writeValueAsString(obj)`

### Python → Go
- `json.loads(s)` → `json.Unmarshal([]byte(s), &obj)`
- `json.dumps(obj)` → `json.Marshal(obj)`

## Date/Time

### Python → JavaScript
- `datetime.now()` → `new Date()`
- `datetime.strptime()` → `new Date(dateString)` or use `date-fns`
- `time.sleep(seconds)` → `await new Promise(r => setTimeout(r, seconds*1000))`

### Python → Java
- `datetime.now()` → `LocalDateTime.now()`
- `datetime.strptime()` → `LocalDateTime.parse(str, formatter)`
- `time.sleep(seconds)` → `Thread.sleep(seconds * 1000)`

### Python → Go
- `datetime.now()` → `time.Now()`
- `datetime.strptime()` → `time.Parse(layout, str)`
- `time.sleep(seconds)` → `time.Sleep(time.Duration(seconds) * time.Second)`

## Regular Expressions

### Python → JavaScript
- `re.search(pattern, text)` → `text.match(new RegExp(pattern))`
- `re.findall(pattern, text)` → `text.match(new RegExp(pattern, 'g'))`
- `re.sub(pattern, repl, text)` → `text.replace(new RegExp(pattern, 'g'), repl)`

### Python → Java
- `re.search(pattern, text)` → `Pattern.compile(pattern).matcher(text).find()`
- `re.findall(pattern, text)` → Use `Matcher` with loop
- `re.sub(pattern, repl, text)` → `text.replaceAll(pattern, repl)`

### Python → Go
- `re.search(pattern, text)` → `regexp.MustCompile(pattern).FindString(text)`
- `re.findall(pattern, text)` → `regexp.MustCompile(pattern).FindAllString(text, -1)`
- `re.sub(pattern, repl, text)` → `regexp.MustCompile(pattern).ReplaceAllString(text, repl)`
