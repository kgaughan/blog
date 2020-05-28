Title: Slow entry submission
Date: 2004-09-15 20:31
Category: Databases
Slug: slow-submission
Status: published

I'm getting a little pissed off with the query used to generate this front page. The last two times I've posted up new entries, the blasted thing's gone and timed out on me for no good reason.

I wasn't able to run the MySQL profiler on it earlier because I'd no data. But now that I've amassed a good twenty five entries, I can test its performance and see what it's doing wrong.

The query that's in there is inspired by one I spotted in [SQL for Smarties](http://www.amazon.com/exec/obidos/tg/detail/-/1558605762/104-1854085-3800724) (second edition) on, I think, the top of page 332. I think that taking O(n^2) time to compute (not that it should matter with 25 entries, but it still seems to be taking a hit). _n_ in this case is 25. This is only my first guess, and I'm hoping that it's wrong.

What I'd like is if the indexes need tuning, but I doubt they do. I think it's going to just be another thing on my todo list. In the mean time, I think I might do something about caching the HTML rather than getting the parser to run over it time after time. I can see that sucking up horrible amounts of processing time quite easily. I'm also going to cache the linklog sidebar's output. It doesn't seem to take much time to generate, but it might be worth doing anyway.

But even all _that_ doesn't explain why it's taking so long. The query for generating the page is cached for five seconds, and the difference in fetching it is only about 300 miliseconds, which is acceptable seeing as the caching manages to counteract any horribleness that might happen due to the page being fetched repeatedly. The parser, while slow, typically takes about 1200ms to render the frontpage (yup, that's ColdFusion 5 for you). All that together with an insert doesn't add up to a timeout.

One final possibility is [blo.gs](http://blo.gs/). I think the pinging code might be screwing up, not because of them or me (maybe them), but because of good old fashioned network latency.

If that turns out to be the problem, I have a slightly hacky solution planned: once an hour, run a job that checks if new entries have been posted up on the site. If they have, ping. Thing is, this seems nasty, but if it's the only way around it, I guess I'll have to do it.
