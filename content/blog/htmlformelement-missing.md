Title: The DOM HTMLFormElement Interface Should Have a getElementsByName() Method
Date: 2005-05-17 17:15
Category: Coding
Slug: htmlformelement-missing
Status: published

While useful on the [HTMLDocument](http://www.w3.org/TR/2003/REC-DOM-Level-2-HTML-20030109/html.html#ID-26809268) interface, [getElementsByName()](http://www.w3.org/TR/2003/REC-DOM-Level-2-HTML-20030109/html.html#ID-26809268) would be much more useful if it was included in [HTMLFormElement](http://www.w3.org/TR/2003/REC-DOM-Level-2-HTML-20030109/html.html#ID-26809268) interface. Every time I want to look up elements by their names, it's usually on form elements rather than the document as a whole. Come to think of it, I don't think there's ever been a time I wanted to look elements up by name on the document, whereas I've wanted to do it on forms quite a bit. What a pain.

Oh, and here's some code to get the same effect.

```javascript
function getElementsByName(frm, name) {
    var elements = [];
    for (var i = 0; i < frm.elements.length; i++) {
        if (frm.elements[i].name == name) {
            elements[elements.length] = frm.elements[i];
        }
    }
    return elements;
}
```

It's trivial, but hey!

**Update**: It'd be enough to use `form.elements[name]`, so this is mostly redundant. The downside of using this method is that, at least in 2005, it didn't include element added to the form dynamically.
