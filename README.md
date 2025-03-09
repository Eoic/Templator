# Templator
A very simple static site generator.

## Building
1. `py -m pip install --upgrade build`
2. `py -m build`

## Installing
`pip install .` (use `-e` flag to install for development)

## Usage
* Compile templates from `html/` directory into `dist/`:
    ```
    templator compile -i html/ -o dist/
    ```
* Use `tempaltor -h` to show all available commands.

### About
1. Template files have `.html` extensions and use standard HTML syntax and a few template-specific expressions described below.
2. Templates have these tags:
    * `(% pull <template name> %)` - include a template relative to this template file, but not outside the template root. For example `(% pull partials/header %)`

    * `(( <content> ))` - any object that has a string representation (e.g. int, str, object). The tag is replaced with the content of the object. If the object does not exist, a default placeholder is inserted instead. For example, `(( username ))`.

    * `(% for <item> in <items> %) (( <item> )) (% done %)` - a for each loop for iterating over a collection of items and rendering their contents to the template file.
3. Each template file can have an accompanying context file in `JSON` format for providing data to the template. The context file name should begin with the name of the template for which this file is defined and end with "context", where words are separated by an underscore. For example, providing a context file to `index.html` would mean creating a file named `index_context.json`. The context file should reside in the same directory as the HTML template file.
4. Templates what include `.part.` in their filename are treated as dependencies of other templates and are not compiled to the output directory separately. For example, `footer.part.html` may only be included by `index.html` so there is not reason to compile it separately as `root.html`.