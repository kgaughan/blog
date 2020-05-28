Title: SQL gotchas
Date: 2010-09-08 14:58
Category: Databases
Status: published

I've been reviewing some SQL queries recently, and I've noticed some things that people do that lead to far from optimal performance. Here's a few, and what people should be doing.

## `COUNT(*)` vs. `COUNT(col)`

At first blush, these may seem the same, but they actually mean very different things. `COUNT(*)` will aggregate the number of rows in the result set or group, whereas `COUNT(col)` will give you the number of non-null values that column has in the current result set or group. You almost always want `COUNT(*)`. If you don't know which you want, use `COUNT(*)`. Treat that like it's the law.

If you're thinking that this isn't a big deal, keep in mind that `COUNT(*)` requires much work on the part of the DBMS than `COUNT(col)`; the value of `COUNT(*)` falls naturally out of what the DBMS is doing whereas `COUNT(col)` requires the DBMS to keep track of an extra counter for non-null values for that column.

## Applying functions to fields you're searching against

Say you have a big table, and you want to get all the rows whose `created` fields is between two dates. `created` is indexed. If you were to try this:

```sql
SELECT id, title, created
FROM   entries
WHERE  (TO_DAYS(NOW()) - TO_DAYS(created)) > ? AND (TO_DAYS(NOW()) - TO_DAYS(created)) <= ?;
```

You're going to subject the DBMS to doing a full table scan just to get those entries. The reason for this is `TO_DAYS(created)`. By doing this, you prevent the DBMS from using the index on `created`. It's easy enough to rearrange this to work a lot better:

```sql
SELECT id, title, created
FROM   entries
WHERE  created BETWEEN CURRENT_DATE + INTERVAL ? DAY AND CURRENT_DATE + INTERVAL ? DAY;
```

It's a simple change, but now the DBMS is able to make effective use of the index.
