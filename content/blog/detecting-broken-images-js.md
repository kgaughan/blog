Title: Detecting broken images with JavaScript
Date: 2005-02-22 16:24 
Slug: detecting-broken-images-js
Category: Coding
Status: published

!!! note
    A cache of the original can be found [here](https://web.archive.org/web/20091227154326/http://talideon.com/weblog/2005/02/detecting-broken-images-js.cfm).

I hit an annoying problem with a project at work. It's not my fault, there's nothing wrong with the code, but sometimes things will happen: people will delete images out of the backend, not upload the image they've given, or will be referencing an image on another server. Welcome to a plague of broken images.

So how to cope with this? Your guess is as good as mine, but for now my solution is to pretend the image isn't there at all. Not completely mind you: it occupies a space, but it's not shown.

But it's not immediately obvious how you check if the images on the page have loaded ok or not. After a few minutes of hacking, here's the most transparent method I could come up with:

```javascript
function IsImageOk(img) {
    // During the onload event, IE correctly identifies any images that
    // weren't downloaded as not complete. Others should too. Gecko-based
    // browsers act like NS4 in that they report this incorrectly.
    if (!img.complete) {
        return false;
    }

    // However, they do have two very useful properties: naturalWidth and
    // naturalHeight. These give the true size of the image. If it failed
    // to load, either of these should be zero.
    if (typeof img.naturalWidth != "undefined" && img.naturalWidth == 0) {
        return false;
    }

    // No other way of checking: assume it's ok.
    return true;
}
```

There's half the work done. Now for the other half. When the page loads, we run over the `images[]` array to check them all.

```javascript
AddEvent(window, "load", function() {
    for (var i = 0; i < document.images.length; i++) {
        if (!IsImageOk(document.images[i])) {
            document.images[i].style.visibility = "hidden";
        }
    }
});
```

And that *should* do the trick.
