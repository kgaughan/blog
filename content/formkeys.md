Title: Formkeys
Date: 2006-02-02 20:44:08
Category: Coding
Status: published

Formkeys are something I first discovered when snooping around the source for [Slashcode](http://www.slashcode.com/) many, many moons ago. The idea is to embed a hidden field in a form that can be later used to check if a form has been submitted twice, or if somebody’s attempting to use it for the purpose of [crapflooding](http://www.urbandictionary.com/define.php?term=crapflood).

I wrote my own implementation of the idea in ColdFusion for my own use. Ok, I wrote _two_ implementations, both with different intents behind them. The first one used session variables and the second using a database. I’ll outline the way I implemented them, though there are many other ways of doing so.

They’re useful for protecting against duplicate form submission and against cross-site request forgery attacks.

## Common Elements

For it to be effective, you need:

*   A lump of _opaque data_: this is your _formkey_ or your _salt_.
*   Some information to validate the formkey when you get it back. These could include a _user id_, _remote host address_, _action/form name_ and _creation timestamp_.
*   A _usage timestamp_ marking when it was used.

In both of my implementations, I went the route of using a [salted hash](https://en.wikipedia.org/wiki/Salt_(cryptography)) of the data I was keeping to validate the formkey.

Initially the usage timestamp will be `null` because the formkey hasn’t been used, but the moment the server gets a request that includes that formkey, the usage timestamp is set to the current time to prevent reuse of that formkey. If you keep formkeys around, you can use them to track if anybody or anything appears to be attempting CSRF attacks on your users.

## Session-based Formkeys

For this, I stored a struct called `formkeys` in the `SESSION` struct. This struct is keyed by the formkey and maps onto another struct containing the data to validate the formkey, specifically:

*   the address of the remote host that generated the request,
*   the timestamp of its creation, and
*   the random salt.

This data, as well as the contents of the `action` field passed with the form and the user id of the user associated with the session, is concatenated and hashed. This hash is compared with the formkey and if they match, it validates.

If the formkey cannot be found or doesn’t match the data associated with it, it fails.
