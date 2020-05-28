Title: The World’s Simplest (decent) PHP Templating Engine...
Date: 2005-07-21 22:51
Category: Coding
Slug: php-templating-engine
Status: published

...is PHP, so why not use it?

```php
function include_view($view, $vars=null) {
    # Start buffering the generated text.
    ob_start();

    # Process the view.
    if (!is_null($vars)) {
        extract($vars, EXTR_OVERWRITE | EXTR_REFS);
    }
    include("views/$view.php");

    # Grab the generated content and clean up.
    $content = ob_get_contents();
    ob_end_clean();

    return $content;
}
```
