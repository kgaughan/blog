Title: A RELAX NG compact schema for RSD
Slug: rsd-rnc
Date: 2007-10-25 10:24
Status: published

I was feeling a bit bored last night and decided to write a schema for [RSD](https://github.com/danielberlinger/rsd) in [RELAX NG](http://relaxng.org/) [compact syntax](http://relaxng.org/compact-tutorial-20030326.html). RSD is about five years old at this point, and nobody ever seems to have got around to writing one, so this might help somebody who wanted to make sure they’re producing valid RSD files:

```rnc
default namespace = "http://archipelago.phrasewise.com/rsd"

# To make it explicit that these element do *not* contain any encoded HTML
# markup.
plainText = text

start = element rsd {
  attribute version { "1.0" },
  element service {
    element engineName { plainText },
    element engineLink { xsd:anyURI },
    element homePageLink { xsd:anyURI },
    element apis {
      element api {
        attribute name { text },
        attribute preferred { "true" | "false" },
        attribute apiLink { xsd:anyURI },
        attribute blogID { text },
        element settings {
          element docs { xsd:anyURI }?,
          element notes { plainText }?,
          element setting {
            attribute name { text },
            text
          }*
        }?
      }+
    }
  }
}
```

I’m not using [`xsd:boolean`](http://books.xmlschemata.org/relaxng/ch19-77025.html) for the `preferred` attribute because it accepts `0` or `false` for _false_ and `1` or `true` for _true_, whereas the spec states that it should only accept `false` and `true`.

Where this differs from the RSD spec, the spec is canonical, not this schema. However, this schema adds some rigour that the spec lacks, so where the spec is ambiguous, you can assume the schema above is correct.
