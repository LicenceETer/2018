+#!/bin/bash
#
# Creat Time :Thu 21 Nov 2013 10:42:16 PM GMT
#this is my first shell on github

cat > sed_change.txt << "EOF"
This is the header line.
This is the first data line.
This is the second data line.
This is the last line.
EOF


# b   branch   跳转命令
# [adress]b [label]
# 参数address 决定了哪些行的数据会触发跳转命令,
# label参数定义了你要跳转到的位置.
# 如果没有label参数，跳转命令会跳到脚本的结尾.

# 简单跳转
echo 简单跳转
sed '{2,3b ; s/This is/Is this/ ; s/line./test?/}' sed_change.txt

# 可以指定跳转标签，将它加到b命令后面即可.
# 标签以冒号开始，最多可以有7个字符.

# -------------------------------------------------------------
# 指定标签跳转
echo 指定标签跳转
sed '{/first/b jump1 ; s/This is the/No jump on/
:jump1
s/This is the/Jump here on/}' sed_change.txt
# 跳转命令指定如果匹配文本first出现行
# 程序应该调到标为jump1的脚本行.
# 如果跳转命令的模式没有匹配，sed编辑器会继续执行脚本中的命令.

# -------------------------------------------------------------
# 利用/模式匹配/+跳转 一直循环替换
echo 利用/模式匹配/+跳转 一直循环替换
echo "My & name & is & lili.Her & name & is & cici" | sed -n '{
:cancel
s/&//p
/&/b cancel
}'
