https://blog.csdn.net/weixin_43273102/article/details/88899644
makefile __alloca 问题
降低版本参考https://blog.csdn.net/zhongwcool/article/details/52300582
遇到问题make会产生
解决方法
降低版本参考https://blog.csdn.net/zhongwcool/article/details/52300582
遇到问题make会产生
/home/jzy/下载/make-3.82/glob/glob.c:1362：对‘__alloca’未定义的引用
/home/jzy/下载/make-3.82/glob/glob.c:1337：对‘__alloca’未定义的引用
/home/jzy/下载/make-3.82/glob/glob.c:1278：对‘__alloca’未定义的引用
/home/jzy/下载/make-3.82/glob/glob.c:1251：对‘__alloca’未定义的引用

解决方法
找到解压的文件glob.c
添加一行代码 #define __alloca alloca

添加前


#if defined _AIX && !defined __GNUC__
 #pragma alloca
#endif

1
2
3
4
5
添加后


#define __alloca alloca               //添加代码
#if defined _AIX && !defined __GNUC__
 #pragma alloca
#endif
1
2
3
4
5
这是我自己猜的，可以使用 。由于网上找不到相关问题，希望能有知道的大佬给予帮助。
--------------------- 
作者：原1241 
来源：CSDN 
原文：https://blog.csdn.net/weixin_43273102/article/details/88899644 
版权声明：本文为博主原创文章，转载请附上博文链接！
