Centring blocks with CSS
========================

:date: 2016-05-15 01:40
:category: CSS
:status: published

Some good friends of mine got married recently, and I helped out with the site
for the wedding. One of the things that needed to be put up on the site was a
poem. Now, just dropping the text of the poem into the page as-is would look
weird; poems have to be formatted a particular way. Also, to fit in with the
layout of the rest of the site, the container that the poem was in needed to
be centred, while its contents needed to be left-aligned, and the container
needed to be only as wide as it needed to be to contain the widest line of the
poem.

After some messing around, I came up with this bit of CSS:

.. code-block:: css

   .centred {
       /* Make the element only as wide as it needs to be. */
       display: inline-block;

       /* Let us apply positioning. */
       position: relative;

       /* Move the left of the element to the middle of the container. */
       left: 50%;

       /* Translate backwards half the width of the block, thus centring it. */
       transform: translateX(-50%);
   }

Apparently the new coolness out there for doing this kind of thing is the
flexbox__, but I had no idea what browsers the people viewing the site would be
using, so a more conservative solution that used relatively well-supported CSS
seemed like a better solution. Some day, flexboxes might be a `well supported
feature`__, but in the meantime, I'm happy with what I came up with, especially
as I remember when it used to be the holy grail of CSS.

.. __: https://www.w3.org/TR/css-flexbox-1/
.. __: http://caniuse.com/#feat=flexbox

Here's hoping this little hack might be of use to somebody.
