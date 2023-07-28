## Web Static
> `css`, `html`

This directory contains static web files including `HTML` and `CSS`. It serves as a starting point for building static websites.

### File Info:
```bash
/
├── n-index.html - the main HTML files that represents the page structures of each webpage.
├── images - icons files directory.
└── styles
    └── *.css - the CSS files that contains styles and formatting rules for the web pages.
```

### W3C File Validation:
> [This](./w3c_validator.py) is a Python validator for the syntax of **HTML** and **CSS** files, and whether or not they make sense in terms of the `World Wide Web Consortium` web standards, and to ascertain interoperability and compatibility across different web browsers and devices.

Running it...
```bash
# simple file:
./w3c_validator.py index.html
# multiple files:
./w3c_validator.py index.html header.html styles/common.css
```
All errors are printed in `STDERR`  
**return**: `exit status` is the # of errors, 0 on Success


### Built with:
`HTML`: used for structuring the content of web pages.  
`CSS`: used for styling the web pages and controlling their appearance.
