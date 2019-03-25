#!/bin/bash

SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")
cd $BASEDIR

project_path=$(cd `dirname $0`; pwd)
project_name="${project_path##*/}"
echo $project_path
echo $project_name

# if [ ! -d CodeCraft-2019 ]
# then
#     echo "ERROR: $BASEDIR is not a valid directory of SDK_python for CodeCraft-2019."
#     echo "  Please run this script in a regular directory of SDK_python."
#     exit -1
# fi
rm -f CodeCraft_code.tar.gz
if [ -e CodeCraft_code.tar.gz ]
then
	echo "didn't rm CodeCraft_code.tar.gz"
	exit -1
fi
cd ..
cp -rf $project_name CodeCraft-2019
rm -rf CodeCraft-2019/config CodeCraft-2019/venv CodeCraft-2019/.idea CodeCraft-2019/.git

tar -zcPf CodeCraft_code.tar.gz CodeCraft-2019
cp -r CodeCraft_code.tar.gz $project_name/CodeCraft_code.tar.gz
rm -f CodeCraft_code.tar.gz
rm -rf CodeCraft-2019
