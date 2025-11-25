Title: Trying out Firebird
Date: 2025-11-25 23:05
Slug: trying-out-firebird
Category: Databases
Status: published

Way back in about 2004, I was looking at [Firebird](https://www.firebirdsql.org/) to possibly use it as an embedded database, similarly to how SQLite is used these days. That project didn't end up going anywhere, but I've always meant to come back to Firebird to give it a try. Now is as good a time as any.

I installed it as follows:

```console
$ sudo apt install firebird4.0-server
```

It went though the setup procedure and I configured a password for the `SYSDBA` user.

I then created a user for myself after reading over the [gsec](https://www.firebirdsql.org/file/documentation/html/en/firebirddocs/gsec/firebird-gsec.html) (user management) documentation. I'm sure there's probably some other way to do this that's more modern, but this is good enough:

```console
$ gsec -user sysdba -fe stdin
Enter password:
GSEC> add keith -admin yes -fname Keith -lname Gaughan -pw *redacted*
```

Yes, annoyingly it requires you to type the password in plaintext rather than offering a prompt, but at least it has the (minor) saving grace of not saving your history.

Lets verify that:

```console
$ gsec -user sysdba -fe stdin -display
Enter password:
     user name                    uid   gid admin     full name
------------------------------------------------------------------------------------------------
SYSDBA                              0     0 admin
KEITH                               0     0 admin     Keith  Gaughan
```

At least I no longer have to use `SYSDBA`!

Creating a database is a bit weird, and this is where its nature as an embeddable DBMS becomes more obvious, as it expects you to specify a path to a file. Whereas other DBMS abstract this away, firebird does not. There is, however, a file where you can provide aliases for the databases. Here's a truncated version of mine (omitting `employee`, as it doesn't seem to be present):

```console
$ cat /etc/firebird/4.0/databases.conf
# ------------------------------
# List of known databases
# ------------------------------

#
# Makes it possible to specify per-database configuration parameters.
# See the list of them and description on file firebird.conf.
# To place that parameters in this file add them in curly braces
# after "alias = /path/to/database.fdb" line. Example:
#       big = /databases/bigdb.fdb
#       {
#               LockMemSize = 32M       # We know that bigdb needs a lot of locks
#               LockHashSlots = 19927   # and big enough hash table for them
#       }
#

#
# Master security database specific setup.
# Do not remove it until you understand well what are you doing!
#
security.db = $(dir_secDb)/security4.fdb
{
        RemoteAccess = false
        DefaultDbCachePages = 256
}

#
# Live Databases:
#
```

I haven't been able to dig up much information on the format of this file yet, but from reading `/etc/firebird/4.0/firebird.conf`, I at least discovered that `$(dir_secDb)` is a predefined macro (presumably at compile-time) defined as `/var/lib/firebird/4.0/system`. There's also a directory called `/var/lib/firebird/4.0/data`, which is what I assume is a directory in which databases files can be created by the DBMS.

I can see how this design would give some flexibility, but it's also the kind of thing that might be rather confusing _unless_ you're using it in an embedded mode, especially if you were to naively try to create a database this way:

```console
$ isql-fb -user keith -f stdin
SQL> create database 'localhost:testing.fdb';
```

Note that I'm using `localhost:` at the beginning of the database name: that's necessary to get the daemon to do it, whereas omitting it will give you confusing errors, because it looks like `isql` attempts to create the database file itself!

But where did it end up? After some digging around, I found it in my `/tmp` directory of all places! There are certainly worse locations to create it, but you'd think that `/var/lib/firebird/4.0/data` would be the default location instead.

```text
testing = /var/lib/firebird/4.0/data/testing.fdb
```

My assumption is that this will cause that database to be crated there rather than in `/tmp`, so got firebird to reload its configuration byt restarting it and tried again:

```console
$ isql-fb -user keith -f stdin
Enter password:
Use CONNECT or CREATE DATABASE to specify a database
SQL> create database 'localhost:testing';
SQL> quit;
$ sudo ls -l /var/lib/firebird/4.0/data
total 1796
-rw-rw---- 1 firebird firebird 1835008 Nov 25 22:36 testing.fdb
```

This time, it behaved as expected. I couldn't find anything in `/etc/firebird/4.0/firebird.conf` that explained this behaviour with `/tmp` or any setting that allowed the default location for creating databases to be specified.

Now, let's see about creating a table.

```console
$ isql-fb -user keith -f stdin
Enter password:
Use CONNECT or CREATE DATABASE to specify a database
SQL> connect 'localhost:testing';
Database: 'localhost:testing', User: KEITH
SQL> show tables;
There are no tables in this database
SQL> create table entries (id integer generated by default as identity primary key, thing varchar(255));
SQL> show tables;
ENTRIES

SQL> select * from entries;
SQL> insert into entries (thing) values ('widget');
SQL> insert into entries (thing) values ('wotsit');
SQL> select * from entries;

          ID THING
============ =================================================================
           1 widget
           2 wotsit
```

It looks to be working!

Firebird is certainly a bit quirky compared to the other RDBMSs I've used in the past, but once you get past those (and its handling of where database files are located is definitely what I'd call quirky), it otherwise seem quite usable, and I might give it a try in a project to see how it goes.
