# Trace Format Reference

## strace Output Format

strace traces system calls made by a program. Each line follows this format:

```
syscall(arg1, arg2, ...) = return_value [extra_info]
```

### Common System Calls

**File Operations:**
- `open(filename, flags)` - Open a file
- `read(fd, buffer, count)` - Read from file descriptor
- `write(fd, buffer, count)` - Write to file descriptor
- `close(fd)` - Close file descriptor
- `stat(path, statbuf)` - Get file status
- `lseek(fd, offset, whence)` - Reposition file offset

**Process Operations:**
- `fork()` - Create child process
- `execve(path, argv, envp)` - Execute program
- `exit(status)` - Terminate process
- `wait4(pid, status, options, rusage)` - Wait for process

**Network Operations:**
- `socket(domain, type, protocol)` - Create socket
- `connect(sockfd, addr, addrlen)` - Connect to address
- `bind(sockfd, addr, addrlen)` - Bind socket to address
- `listen(sockfd, backlog)` - Listen for connections
- `accept(sockfd, addr, addrlen)` - Accept connection
- `send(sockfd, buf, len, flags)` - Send data
- `recv(sockfd, buf, len, flags)` - Receive data

### Return Values

- Positive numbers: Success (often file descriptor or bytes transferred)
- `0`: Success for some calls
- Negative numbers: Error codes (e.g., `-1 ENOENT` means file not found)

### Common Error Codes

- `ENOENT` (2): No such file or directory
- `EACCES` (13): Permission denied
- `EEXIST` (17): File exists
- `EINVAL` (22): Invalid argument
- `ECONNREFUSED` (111): Connection refused
- `ETIMEDOUT` (110): Connection timed out

## ltrace Output Format

ltrace traces library calls made by a program. Format is similar to strace:

```
function(arg1, arg2, ...) = return_value
```

### Common Library Calls

**String Operations:**
- `strlen(str)` - Get string length
- `strcmp(s1, s2)` - Compare strings
- `strcpy(dest, src)` - Copy string
- `strcat(dest, src)` - Concatenate strings

**Memory Operations:**
- `malloc(size)` - Allocate memory
- `free(ptr)` - Free memory
- `memcpy(dest, src, n)` - Copy memory
- `memset(s, c, n)` - Fill memory

**I/O Operations:**
- `fopen(path, mode)` - Open file
- `fread(ptr, size, nmemb, stream)` - Read from file
- `fwrite(ptr, size, nmemb, stream)` - Write to file
- `fclose(stream)` - Close file
- `printf(format, ...)` - Print formatted output

**Process Operations:**
- `system(command)` - Execute shell command
- `exit(status)` - Exit program

### Return Values

- Pointers: Memory addresses (e.g., `0x7fff12345678`)
- Integers: Numeric values
- `NULL` or `nil`: Null pointer
- `-1`: Error for many functions
