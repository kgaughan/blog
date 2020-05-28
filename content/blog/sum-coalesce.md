Title: SQL Tricks: SUM(), then COALESCE()
Date: 2007-09-11 14:56
Slug: sum-coalesce
Category: Databases
Status: published

Seeing as I'm after doing this for the umpteenth time just now, I thought I'd note it here. There's no chance of me forgetting it, but somebody who doesn't know the trick might find it useful.

I have to write quite a few reports where I need to, say, count the total number of items and then the number of items that fit certain criteria. My favourite trick for reports like that is to `SUM()` on a boolean expression specifying the criteria, then `COALESCE()` the result with 0.

For instance, let's say you've a table containing customer invoices, and you want to get the total number of invoices and the number paid invoices, and the number of unpaid invoices with more than 20EUR left to pay on them. To do that, you'd do something like this:

```sql
SELECT  COUNT(*) AS invoices,
        COALESCE(SUM(amount_paid = amount_total), 0) AS paid,
        COALESCE(SUM(amount_total - amount_paid > 2000), 0) AS spongers
FROM    invoices
```

The way this works is that boolean expressions in SQL evaluate to either `1` or `0`. Because of this, summing what boolean expressions evaluate to can tell us how many records match that expression.

The presence of `COALESCE()` is to counter an edge case where the result you're summarising contains no row. This might be because the table's empty, the criteria specified in the `WHERE` clause doesn't match anything, &c. If this is so, `SUM()` will return `NULL`, but what we really want is `0`, so `COALESCE()` is in there to catch this.
