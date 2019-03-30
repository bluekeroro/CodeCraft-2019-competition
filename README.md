### 食用方式
1. 工程名不可以起名为CodeCraft-2019，和当前项目在同一路径下的其他项目也不可以起名为CodeCraft-2019
2. 运行CodeCraft_tar.sh打包脚本生成CodeCraft_code.tar.gz，该压缩包可直接提交到平台上运行
3. CodeCraft_tar.sh脚本打包时会自动不包含config目录，venv目录，.idea目录，.git目录
4. 在执行该脚本时，请勿同时用压缩软件打开CodeCraft_code.tar.gz。否则无法更新该压缩文件。

*打包命令：sh CodeCraft_tar.sh*  
*运行pip install -r requirements.txt 安装依赖*