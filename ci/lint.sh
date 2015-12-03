#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pip install flake8 flake8-respect-noqa

flake8_args='--ignore=E501,E228,E226,E261,E262,E128,E266,E265'

# 取出新增或修改的文件, 删除的就不用管了
git_diff_file_names=`git diff --name-status master | grep -E '^(A|M)' | grep ".py" | cut -f 2`

# 一次检查所有文件, 最后有错才报错退出
for file in $git_diff_file_names
do
		flake8 $DIR/../$file $flake8_args
done
