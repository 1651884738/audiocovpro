# audio_cov_pro
用于裁去音频头尾的静默时间。

## 程序打包
```angular2html
pyinstaller --onefile --add-binary "./ffmpeg/bin/ffmpeg.exe;." main.py

1、如果你想要生成一个文件夹，其中包含了可执行文件和其他依赖文件，可以省略--onefile选项
2、--add-binary选项用于指定要添加到可执行文件中的文件
3、.; 表示将FFmpeg库文件添加到可执行文件的根目录
.

```


## 参考资源:
https://github.com/jiaaro/pydub/blob/master/API.markdown
https://www.cnblogs.com/shwee/p/9427975.html