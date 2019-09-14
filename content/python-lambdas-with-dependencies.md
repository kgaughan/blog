Title: Creating AWS Lambda functions in Python with dependencies
Date: 2019-05-01 14:34
Slug: python-lambda-deps
Category: Coding
Status: published

This assumes you have a package called `mylambda` and a `requirements.txt` file listing your dependencies.

build.sh:

```sh
#!/bin/sh

tmp_dir=$(mktemp -d)
trap "rm -rf '$tmp_dir'" EXIT

pip install -r requirements.txt -t "$tmp_dir"
cp -R mylambda "$tmp_dir/mylambda"

here=$(pwd)
(
    cd $tmp_dir
    zip -r -9 $here/lambda.zip .
)
```

For installation of the dependencies to work, you need this `setup.cfg` file in the same directory as `build.sh` so pip can find it:

```ini
[install]
prefix=
```
