# JavaScript/TypeScript Deprecated APIs

## Node.js Core APIs

### Buffer constructor (Node.js 6.0+)

```javascript
// ❌ Deprecated
const buf1 = new Buffer(10);  // Allocate buffer
const buf2 = new Buffer('hello');  // From string
const buf3 = new Buffer([1, 2, 3]);  // From array

// ✅ Modern
const buf1 = Buffer.alloc(10);  // Safe allocation (zero-filled)
const buf2 = Buffer.from('hello');  // From string
const buf3 = Buffer.from([1, 2, 3]);  // From array
const buf4 = Buffer.allocUnsafe(10);  // Faster but uninitialized
```

### url.parse() (Node.js 11.0+)

```javascript
// ❌ Deprecated
const url = require('url');
const parsed = url.parse('https://example.com/path?query=1');

// ✅ Modern
const parsed = new URL('https://example.com/path?query=1');
console.log(parsed.hostname);  // example.com
console.log(parsed.pathname);  // /path
console.log(parsed.searchParams.get('query'));  // 1
```

### crypto.createCipher() (Node.js 10.0+)

```javascript
// ❌ Deprecated (insecure - uses weak key derivation)
const crypto = require('crypto');
const cipher = crypto.createCipher('aes192', 'password');

// ✅ Modern (secure - use createCipheriv with proper IV)
const algorithm = 'aes-256-cbc';
const key = crypto.scryptSync('password', 'salt', 32);
const iv = crypto.randomBytes(16);
const cipher = crypto.createCipheriv(algorithm, key, iv);
```

### fs.exists() (Node.js 1.0+)

```javascript
// ❌ Deprecated
const fs = require('fs');
fs.exists('/path/to/file', (exists) => {
    if (exists) {
        // File exists
    }
});

// ✅ Modern - use fs.access() or fs.stat()
const fs = require('fs').promises;

// Check if file exists
try {
    await fs.access('/path/to/file');
    // File exists
} catch {
    // File doesn't exist
}

// Or get file stats
try {
    const stats = await fs.stat('/path/to/file');
    // File exists and you have stats
} catch {
    // File doesn't exist
}
```

### process.binding() (Node.js 10.9+)

```javascript
// ❌ Deprecated (internal API)
const natives = process.binding('natives');

// ✅ Modern - use public APIs instead
// No direct replacement - use documented public APIs
```

### util.isArray() and similar (Node.js 4.0+)

```javascript
// ❌ Deprecated
const util = require('util');
util.isArray([]);
util.isFunction(() => {});
util.isString('hello');

// ✅ Modern - use native methods
Array.isArray([]);
typeof func === 'function';
typeof str === 'string';
```

## React

### React.createClass (React 16.0+)

```javascript
// ❌ Deprecated
const MyComponent = React.createClass({
    getInitialState: function() {
        return { count: 0 };
    },
    render: function() {
        return <div>{this.state.count}</div>;
    }
});

// ✅ Modern - class component
class MyComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = { count: 0 };
    }
    render() {
        return <div>{this.state.count}</div>;
    }
}

// ✅ Best - function component with hooks
function MyComponent() {
    const [count, setCount] = useState(0);
    return <div>{count}</div>;
}
```

### ReactDOM.render() (React 18.0+)

```javascript
// ❌ Deprecated
import ReactDOM from 'react-dom';

ReactDOM.render(<App />, document.getElementById('root'));

// ✅ Modern
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
root.render(<App />);
```

### React.PropTypes (React 15.5+)

```javascript
// ❌ Deprecated
import React from 'react';

MyComponent.propTypes = {
    name: React.PropTypes.string
};

// ✅ Modern
import PropTypes from 'prop-types';

MyComponent.propTypes = {
    name: PropTypes.string
};
```

### componentWillMount, componentWillReceiveProps, componentWillUpdate (React 16.3+)

```javascript
// ❌ Deprecated (unsafe lifecycle methods)
class MyComponent extends React.Component {
    componentWillMount() {
        // Initialize
    }

    componentWillReceiveProps(nextProps) {
        // Update state based on props
        if (nextProps.value !== this.props.value) {
            this.setState({ value: nextProps.value });
        }
    }

    componentWillUpdate(nextProps, nextState) {
        // Prepare for update
    }
}

// ✅ Modern
class MyComponent extends React.Component {
    componentDidMount() {
        // Initialize after mounting
    }

    static getDerivedStateFromProps(props, state) {
        // Return new state based on props change
        if (props.value !== state.prevValue) {
            return {
                value: props.value,
                prevValue: props.value
            };
        }
        return null;
    }

    getSnapshotBeforeUpdate(prevProps, prevState) {
        // Capture information before DOM update
        return null;
    }
}
```

### findDOMNode (React 16.3+)

```javascript
// ❌ Deprecated
import { findDOMNode } from 'react-dom';

class MyComponent extends React.Component {
    handleClick = () => {
        const node = findDOMNode(this);
        node.scrollIntoView();
    }
}

// ✅ Modern - use refs
class MyComponent extends React.Component {
    myRef = React.createRef();

    handleClick = () => {
        this.myRef.current.scrollIntoView();
    }

    render() {
        return <div ref={this.myRef}>...</div>;
    }
}

// ✅ Best - function component with useRef
function MyComponent() {
    const myRef = useRef(null);

    const handleClick = () => {
        myRef.current.scrollIntoView();
    };

    return <div ref={myRef}>...</div>;
}
```

### String refs (React 16.3+)

```javascript
// ❌ Deprecated
class MyComponent extends React.Component {
    handleClick = () => {
        this.refs.myInput.focus();
    }

    render() {
        return <input ref="myInput" />;
    }
}

// ✅ Modern - createRef
class MyComponent extends React.Component {
    myInputRef = React.createRef();

    handleClick = () => {
        this.myInputRef.current.focus();
    }

    render() {
        return <input ref={this.myInputRef} />;
    }
}

// ✅ Best - useRef hook
function MyComponent() {
    const myInputRef = useRef(null);

    const handleClick = () => {
        myInputRef.current.focus();
    };

    return <input ref={myInputRef} />;
}
```

### Legacy Context API (React 16.3+)

```javascript
// ❌ Deprecated
class MyComponent extends React.Component {
    static childContextTypes = {
        theme: PropTypes.string
    };

    getChildContext() {
        return { theme: 'dark' };
    }
}

// ✅ Modern - Context API
const ThemeContext = React.createContext('light');

function App() {
    return (
        <ThemeContext.Provider value="dark">
            <MyComponent />
        </ThemeContext.Provider>
    );
}

function MyComponent() {
    const theme = useContext(ThemeContext);
    return <div>Theme: {theme}</div>;
}
```

## Express.js

### body-parser middleware (Express 4.16+)

```javascript
// ❌ Deprecated (separate package)
const express = require('express');
const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// ✅ Modern (built-in)
const express = require('express');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
```

## Moment.js (Entire library in maintenance mode)

```javascript
// ❌ Deprecated (moment.js is in maintenance mode)
const moment = require('moment');
const date = moment().format('YYYY-MM-DD');

// ✅ Modern - use date-fns
const { format } = require('date-fns');
const date = format(new Date(), 'yyyy-MM-dd');

// ✅ Modern - use Day.js (moment-like API)
const dayjs = require('dayjs');
const date = dayjs().format('YYYY-MM-DD');

// ✅ Modern - use native Intl
const date = new Intl.DateTimeFormat('en-CA').format(new Date());
```

## jQuery (Modern alternatives)

```javascript
// ❌ jQuery (not technically deprecated but outdated)
$('.element').addClass('active');
$('.element').on('click', handler);
$.ajax({ url: '/api/data' });

// ✅ Modern - Vanilla JavaScript
document.querySelector('.element').classList.add('active');
document.querySelector('.element').addEventListener('click', handler);
fetch('/api/data');

// ✅ Modern - React/Vue/Angular for complex UIs
```

## Webpack

### webpack.optimize.UglifyJsPlugin (Webpack 4.0+)

```javascript
// ❌ Deprecated
const webpack = require('webpack');

module.exports = {
    plugins: [
        new webpack.optimize.UglifyJsPlugin()
    ]
};

// ✅ Modern - use mode: 'production'
module.exports = {
    mode: 'production',  // Enables built-in optimizations
    optimization: {
        minimize: true
    }
};
```
