Title: A reasonable XML RPC envelope protocol, and asynchronous calls
Date: 2008-05-12 11:57
Category: Coding
Slug: srgp
Status: published

!!! note
    This is juvenile, but it's still better than XML-RPC. [Here](https://web.archive.org/web/20080807163956/http://talideon.com/weblog/2008/05/srgp.cfm) is the original post.

Sometimes something you do as a joke can yield interesting results.

About a year or so ago, I was feeling bored and decided to see how much of a diet I could put [XML-RPC](http://xmlrpc.scripting.com/) on as you do. Though I managed to slim it down quite a bit and produce a [RELAX NG](https://relaxng.org/) schema for the resulting format, it was all just a diversion and I only did it for fun. I let all of this sit on my harddrive festering away for ages until I stumbled across it again and decided to fiddle with the idea of a HTTP-derived joke protocol designed _specifically_ for tunnelling the likes of XML-RPC.

## SRGP, a HTTP pod-person for RPC

I called the protocol _SRGP_, or _Simplified RPC Gateway Protocol_, and it was intended to be a pod-person equivalent of HTTP. It looked like HTTP, behaved a lot like HTTP, but there's something wrong about it.

It had a Winer-esque specification that didn't go to much effort to rigourously outline the workings of the protocol, and made lots of undocumented assumptions, all of which were meant to lead to subtly incompatible client and server implementations. Because it's a pod-person protocol, it could be implemented on top of a HTTP server with little effort.

It was too late for April Fool's Day, so I never published the spec, but the process of writing it did lead me down an interesting path.

## An overview of SRGP

SRGP _looks_ like HTTP, however it's subtly different, though not quite incompatible. The semantics of GET and POST change slightly. A GET request on an endpoint returns a service document or IDL description for that endpoint describing what it exposes. A POST request is used for sending a payload representing a remote procedure call to the endpoint.

Requests and responses are of the same form as their HTTP equivalents, but the number of headers SRGP has been trimmed down. It still understands `Content-Type`, `Accept-Encoding`, `Content-Encoding`, `User-Agent`, `Server`, `Connection`, `Host`, `Location`, `Content-Length`, `Retry-After`, and `Date`. These headers mean more or less the same thing as their HTTP equivalents.

It also introduces two header elements of its own: `Reference` and `Token`, but I'll get to those in a tick.

The response status codes are trimmed down. Their semantics are close to the HTTP originals:

200 OK
202 Accepted
301 Moved Permanently
400 Bad Request
403 Forbidden
404 Bad Endpoint
405 Bad Request Type
500 Internal Server Error
503 Service Unavailable
505 Protocol Version Not Supported

**200** implies that the request was successfully _dispatched_, but not necessarily that it was successfully _processed_. After all, it can contain a fault response. The headers accompanying it are `Content-Type` and `Date`, and if they were provided with the request, `Reference` and `Token` will be returned with the response too. The response might also include the `Content-Encoding`, `Server`, and `Connection` responses.

**202** implies that the request has been accepted but not yet processed, and the body _may_ contain a plaintext explanation of why. Other than that, it's just like a 200 response, but will always be accompanied by a `Reference` header so that the request can be retried at a later point. If none accompanied the request, the server generates its own. The response also contains a `Retry-After` header so the client knows the polling interval to use to retry the request to check if it's been processed.

The point behind the `Reference` header is to guarantee _call idempotency_. Lack of the header implies that the client doesn't particularly care if the is serviced one or many times, just as long as it get serviced. The presence of the `Reference` header in a request is the client's way of saying that it wants the call to be serviced once and one only, and that any number of calls with the same reference should be treated as a single call. To this extent, it's a bit like a HTTP client including an ETag in a POST request. The server should maintain reference affinity with the client that generated the reference in the first place, so that so clients can generate the same reference without the collision causing security and other problems. How affinity might work, I'm not sure.

Considering I've covered `Reference`, I'd might as well talk about `Token`. If `Cookie` is the state management equivalent of somebody with half their brain removed, `Token` is the equivalent of just leaving behind the brain stem. This header, when used in a request, can contain one of two things: ‘new', or ‘v="_token_"', where _token_ is a string that acts as a session identifier. `Token: new` is the client's way of saying they want to start a new session. The server responds with `Token: v="_token_"`, and the client sends that back with each request that's meant to be part of the session. Session state is unique to individual endpoints, not to the host. A session times out after 30 minutes without a request from the client, but other than that, it's up to the server to decide how it manages session state. References are not tied to sessions, nor the reverse. It's nicely stupid. `Token` is a whoopee cushion and a server or client may not even implement it.

**301**, **400**, **403**, **404**, **405**, **500**, **503**, and **505** all do what you might guess from familiarity with HTTP. **503** is notable though, so I think it's worth mentioning here. It means that the gateway server or endpoint is temporarily down, so the client should try again later. The body can contain a plaintext explanation of why it's down, and the response will include a `Retry-After` header so the client knows what amount of time to retry the original request after.

## The interesting diversion

The existence of SRGP is rather silly, though not entirely impractical. An implementation of it would be simpler than an implementation of HTTP, and it's somewhat more useful than tunnelling RPC over POST.

It does include at least two interesting and connected ideas: the `Reference` header and the repurposing of the _202_ response code. The existence of these makes it possible for a server to process calls _asynchronously_, which is something tunnelling RPC over POST doesn't let you do.

But now that calls can be processed asynchronously by the server, what about the client? To get a response, it needs to poll the server for the response. `POST` can be used, but it's not a great fit, we'll introduce a new verb, `POLL`, which is to `POST` in SRGP as `HEAD` is to `GET` in HTTP. The difference is that `POLL` is always accompanied by a `Reference` header, and never has a body. This allows the client to poll for an asynchronous response without the overhead of a possibly expensive to calculate or large request body. Other than that, it's behaviour is identical to `POST`.

It's sometimes better for both the server and client to instead have the server notify the client that the request's been processed. With that in mind, I decided to introduce one more verb and a header: `NOTIFY` and `Notify` respectively.

A `POST` that includes a `Notify` header must always include a `Reference` header. The presence of this header states that if the call is processed asynchronously, the server will send a `NOTIFY` request to the endpoint specified by the `Notify` header containing the response. The server indicates its understanding of the `Notify` header by repeating the `Notify` header in the **202** response headers verbatim. Neither clients nor servers can expect their opposite to implement `Notify` support and should fall back on polling if unimplemented.

When the server has processed the asynchronous request, it sends a `NOTIFY` request to the endpoint specified in the original request. The request contains the same headers and content as a polled **200** response would. The only valid 2xx code a notification endpoint can respond with is **200**. **503** and **301** responses are processed as you'd expect. A **400** response to valid request, or a **403**, **404**, **405**, **505** response should be handled by an angry phonecall or email to the entity who made the original request to fix their software. A **500** response should be handled by a polite phonecall or email asking them to fix their software.

## So, what's interesting about this?

With very little effort, we've managed to add a pretty flexible and, more to the point, useful asynchronous call mechanism on top of SRGP.

## Background: my XML-RPC reworking

Back to the XML-RPC reworking. It's been done many times before, but about a year ago I decided to create a schema that mapped almost one-to-one onto that of XML-RPC, but without the bloat. I did this for fun and certainly never expected that anybody would ever seriously consider implementing anything to process it.

Here's the sample response to a `metaWeblog.getPost` call:

```xml
<?xml version="1.0"?>
<methodResponse>
  <params>
    <param>
      <value><struct>
    <member>
      <name>categories</name>
      <value>
        <array>
          <data>
            <value>Michegas</value>
            <value>Mind Bombs</value>
            <value>Rest &amp; Relaxation</value>
            <value>Two-Way-Web</value>
            </data>
          </array>
        </value>
      </member>
    <member>
      <name>dateCreated</name>
      <value>
        <dateTime.iso8601>20030729T10:59:48</dateTime.iso8601>
        </value>
      </member>
    <member>
      <name>description</name>
      <value>Blogger Ed Cone of Greensboro talks about the several
        intersections he overlooks.&amp;nbsp; That is: junctions
        of the public and the personal (which every blogger faces)
        and more particularly the contrasting voices of a
        newspaper columnist and a blogger (he is both) and the
        opportunities for a local conversation in a global medium.</value>
      </member>
    <member>
      <name>enclosure</name>
      <value>
        <struct>
          <member>
            <name>length</name>
            <value>
              <i4>11421281</i4>
              </value>
            </member>
          <member>
            <name>type</name>
            <value>audio/mpeg</value>
            </member>
          <member>
            <name>url</name>
            <value>http://media.skybuilders.com/lydon/cone.mp3</value>
            </member>
          </struct>
        </value>
      </member>
    <member>
      <name>link</name>
      <value>http://blogs.law.harvard.edu/lydon/2003/07/18#a187</value>
      </member>
    <member>
      <name>permaLink</name>
      <value>http://radio.weblogs.com/0001015/2003/07/29.html#a1829</value>
      </member>
    <member>
      <name>postid</name>
      <value>
        <i4>1829</i4>
        </value>
      </member>
    <member>
      <name>title</name>
      <value>Chris Lydon interview with Ed Cone</value>
      </member>
    <member>
      <name>userid</name>
      <value>
        <i4>1015</i4>
        </value>
      </member>
    </struct></value>
      </param>
    </params>
  </methodResponse>
```

The more I look at an XML-RPC request or response, the more it looks to me like an elaborate practical joke.

Here's that same response in my trimmed down schema:

```xml
<?xml version="1.0"?>
<response>
  <map>
    <array key="categories">
      <string>Michegas</string>
      <string>Mind Bombs</string>
      <string>Rest &amp; Relaxation</string>
      <string>Two-Way-Web</string>
    </array>
    <date key="dateAdded">2003-07-29T10:59:48-05:00</date>
    <string key="description">
      Blogger Ed Cone of Greensboro talks about the several
      intersections he overlooks.&amp;nbsp; That is: junctions
      of the public and the personal (which every blogger faces)
      and more particularly the contrasting voices of a
      newspaper columnist and a blogger (he is both) and the
      opportunities for a local conversation in a global medium.
    </string>
    <map key="enclosure">
      <int key="length">11421281</int>
      <string key="type">audio/mpeg</string>
      <string key="url">
        http://media.skybuilders.com/lydon/cone.mp3
      </string>
    </map>
    <string key="link">
      http://blogs.law.harvard.edu/lydon/2003/07/18#a187
    </string>
    <string key="permaLink">
      http://radio.weblogs.com/0001015/2003/07/29.html#a1829
    </string>
    <string key="postid">1829</string>
    <string key="title">Chris Lydon interview with Ed Cone</string>
    <string key="userid">1015</string>
  </map>
</response>
```

There's no way anybody can convince me that's not better than the original.

As you can see, it didn't take an awful lot of effort on my part to strip out all the junk to give something a lot clearer and more compact than what Dave Winer came up with. All it took was removing the redundant `<value/>`, `<params/>`, `<param/>`, and `<data/>` tags; not being afraid of attributes and using them as the were intended, which allowed me to get rid of the `<member/>`, `<methodName/>`, `<member>`, and `<name/>` elements, and trim down `<fault/>` considerably; I trimmed down the names, getting rid of the redundant `<i4/>` and changing `<datetime.iso8601/>` to `<date/>` because it's more obvious and doesn't include a pointless description of its encoding, `<double/>` to `<float/>` as that's more familiar to the average person, `<base64/>` to `<binary/>` because that describes what it's for rather than how it's encoded, and `<struct/>` to `<map/>` because _struct_ has the implication of ordering, whereas _map_ doesn't.

Here's the RELAX-NG compact schema:

```rng
default namespace = "http://talideon.com/projects/schemas/xpc/v1/"
start = xpcCall | xpcResponse | xpcFault

xpcMethodName = xsd:string {
  pattern = "\[a-zA-Z\_\]\[a-zA-Z0-9\_\]\*(\\.\[a-zA-Z\_\]\[a-zA-Z0-9\_\]\*)\*"
}

xpcCall = element call {
  attribute method { xpcMethodName },
  xpcType\*
}

xpcResponse = element response {
  xpcType?
}

xpcFault = element fault {
  attribute code { xsd:integer },
  text
}

xpcType =
  element nil     { empty } |
  element int     { xsd:integer } |
  element boolean { xsd:boolean } |
  element string  { text } |
  element float   { xsd:double } |
  element date    { xsd:dateTime } |
  element binary  { xsd:base64Binary } |
  element array   { xpcType\* } |
  element map     { xpcMType\* }

xpcKey = attribute key { text }
xpcMType =
  element nil     { xpcKey, empty } |
  element int     { xpcKey, xsd:integer } |
  element boolean { xpcKey, xsd:boolean } |
  element string  { xpcKey, text } |
  element float   { xpcKey, xsd:double } |
  element date    { xpcKey, xsd:dateTime } |
  element binary  { xpcKey, xsd:base64Binary } |
  element array   { xpcKey, xpcType\* } |
  element map     { xpcKey, xpcMType\* }
```

The type system's extended slightly to include `<nil/>`, which represents the lack of a value. This is already a common extension. Method names now have a canonical form similar to that of method name in all the major languages though this is something I'm not terribly attached to. Because it _has_ a schema, it's rigourously defined, so a spec for this RPC system would never have required the Q&A section that accompanies the XML-RPC spec. Oh, and dates now require a timezone.

**Update:** For reference's sake, there's already a reworking of XML-RPC called [XPC](https://web.archive.org/web/20080807163956/http://www.focusresearch.com/gregor/sw/XPC/), which goes even further by combining all the scalar types together, so the mapping is one way. I don't mind annotating the types, but I wanted to minimise the waste markup. I considered batch calls, but just never bothered.
