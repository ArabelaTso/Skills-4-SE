# Python Deprecated APIs

## Python Standard Library

### collections module (Python 3.3+)

Abstract base classes moved to `collections.abc`:

```python
# ❌ Deprecated
from collections import Mapping, MutableMapping, Iterable, Iterator, Sequence
isinstance(obj, collections.Mapping)

# ✅ Modern
from collections.abc import Mapping, MutableMapping, Iterable, Iterator, Sequence
isinstance(obj, collections.abc.Mapping)
```

### time module (Python 3.3+)

```python
# ❌ Deprecated
import time
start = time.clock()

# ✅ Modern - for wall-clock time
start = time.perf_counter()

# ✅ Modern - for CPU time
start = time.process_time()
```

### os module

```python
# ❌ Deprecated
import os
output = os.popen('ls').read()

# ✅ Modern
import subprocess
result = subprocess.run('ls', shell=True, capture_output=True, text=True)
output = result.stdout
```

### platform module (Python 3.8+)

```python
# ❌ Deprecated
import platform
dist = platform.dist()
linux_dist = platform.linux_distribution()

# ✅ Modern
import distro  # pip install distro
dist = distro.linux_distribution()
```

### imp module (Python 3.4+)

```python
# ❌ Deprecated
import imp
module = imp.load_source('name', 'path')

# ✅ Modern
import importlib.util
spec = importlib.util.spec_from_file_location('name', 'path')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
```

## Django Framework

### URL routing (Django 2.0+)

```python
# ❌ Deprecated
from django.conf.urls import url

urlpatterns = [
    url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
]

# ✅ Modern
from django.urls import path, re_path

urlpatterns = [
    path('articles/<int:year>/', views.year_archive),  # Preferred
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),  # For complex patterns
]
```

### Encoding utilities (Django 3.0+)

```python
# ❌ Deprecated
from django.utils.encoding import force_text, smart_text

text = force_text(value)
smart = smart_text(value)

# ✅ Modern
from django.utils.encoding import force_str, smart_str

text = force_str(value)
smart = smart_str(value)
```

### Translation functions (Django 3.0+)

```python
# ❌ Deprecated
from django.utils.translation import ugettext, ugettext_lazy, ugettext_noop
from django.utils.translation import ungettext, ungettext_lazy

_ = ugettext
_lazy = ugettext_lazy

# ✅ Modern
from django.utils.translation import gettext, gettext_lazy, gettext_noop
from django.utils.translation import ngettext, ngettext_lazy

_ = gettext
_lazy = gettext_lazy
```

### Model field on_delete (Django 2.0+)

```python
# ❌ Deprecated (implicit CASCADE)
from django.db import models

class Book(models.Model):
    author = models.ForeignKey(Author)  # on_delete is required

# ✅ Modern (explicit on_delete)
class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
```

### render_to_response (Django 3.0+)

```python
# ❌ Deprecated
from django.shortcuts import render_to_response

def my_view(request):
    return render_to_response('template.html', context)

# ✅ Modern
from django.shortcuts import render

def my_view(request):
    return render(request, 'template.html', context)
```

## Flask Framework

### JSON handling (Flask 2.2+)

```python
# ❌ Deprecated
from flask.json import jsonify

# ✅ Modern
from flask import jsonify
```

### send_file parameters (Flask 2.0+)

```python
# ❌ Deprecated
from flask import send_file

@app.route('/download')
def download():
    return send_file('file.pdf', attachment_filename='document.pdf')

# ✅ Modern
@app.route('/download')
def download():
    return send_file('file.pdf', download_name='document.pdf')
```

### Accessing JSON (Flask 1.0+)

```python
# ❌ Deprecated
@app.route('/api', methods=['POST'])
def api():
    data = request.get_json(force=True)

# ✅ Modern
@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
```

## SQLAlchemy

### Declarative base (SQLAlchemy 2.0+)

```python
# ❌ Deprecated
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# ✅ Modern
from sqlalchemy.orm import declarative_base

Base = declarative_base()
```

### Engine execution (SQLAlchemy 2.0+)

```python
# ❌ Deprecated
result = engine.execute('SELECT * FROM users')

# ✅ Modern
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text('SELECT * FROM users'))
```

## Pandas

### DataFrame.append (Pandas 1.4.0+)

```python
# ❌ Deprecated
df1 = df1.append(df2)

# ✅ Modern
df1 = pd.concat([df1, df2], ignore_index=True)
```

### DataFrame.ix (Pandas 1.0.0+)

```python
# ❌ Deprecated
df.ix[0, 'column']

# ✅ Modern
df.loc[0, 'column']  # Label-based
df.iloc[0, 0]  # Position-based
```

## NumPy

### Type aliases (NumPy 1.20+)

```python
# ❌ Deprecated
import numpy as np
arr = np.array([1, 2, 3], dtype=np.int)
arr = np.array([1.0, 2.0], dtype=np.float)

# ✅ Modern
arr = np.array([1, 2, 3], dtype=np.int_)
arr = np.array([1.0, 2.0], dtype=np.float64)
```

## Requests

### Session context manager (Requests 2.28+)

```python
# ❌ Old style
import requests
s = requests.Session()
try:
    response = s.get('https://api.example.com')
finally:
    s.close()

# ✅ Modern
with requests.Session() as s:
    response = s.get('https://api.example.com')
```
