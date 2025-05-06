# coder-coder
## 简介
        本项目旨在收集平时开发中编写的各类高性能易用库函数，并整合在一起，以供开发学习使用，请勿商用！

        This project aims at collecting various awesome,high performance,convienent library methods.
    Providing all of them for learning and developing.
    
        ⚠ PLEASE NOTE THAT COMMERCIAL USE IS PROHIBITED! ⚠
## ⚙ 安装说明
部分可能有冲突的依赖已指定版本存放于根目录的requirement.txt中，执行`pip install -r requirement.txt`以安装。其余依赖可根据不同库函数按需自由安装。
## 函数细节说明
以下将罗列所有当前项目中已收集的库函数，提供使用方法并对功能作简要阐述。

该库会不定时持续更新！
### 1. baidu_coord_to_tianditu_coord.py
将百度坐标转为天地图坐标。基本转换思路为：百度坐标系->火星坐标系->国测局坐标系->WGS坐标系

入口函数为baidu_coord_to_tianditu_coord()，入参为百度坐标对象。

### 2. CIEDE2000.py
一种色差计算公式。（[关于CIEDE](https://color.org/events/colorimetry/Melgosa_CIEDE2000_Workshop-July4.pdf)）

入口函数为：ciede2000()，入参为需要作色差比较的两个lab模型的颜色值。
### 3. console_display.py
用于将python数据结构格式化后在控制台以表格样式输出，美化输出结果。控制台输出的同时还会在当前目录下保存相同数据文件。

入口函数为console_display()，主要入参为第一项列设置column_settings和第二项行数据，具体字段结构可查看类ColumnSettingTest。
### 4. image_matcher_by_FLANN.py
一种基于FLANN神经网络的快速图像对比匹配算法。核心算法用到了opencv的cv2.FlannBasedMatcher匹配模型以及SIFT检测器。

入口函数为get_matched_image_center()，主要入参为第一项原始图片和第二项模板匹配图片。函数的返回值为若干个匹配图片的中心坐标元组构成的数组。

### 5. judge_points_in_polygon.py
快速判断二维坐标点是否在二维多边形内的函数。

入口函数为：is_point_in_polygon()，入参第一项为坐标点([121.123456,31.123456])，第二项为连续边的多边形坐标点。
### 6. tesee_ocr.py
一种基于卷积神经网络CNN与ocr图像识别技术的简易验证码训练与识别库，使用tensorflow驱动训练学习。

可调用gen_captcha_text_image()生成随机验证码，并调用train_cnn()来启动自训练。
训练与微调结束后，可调用crack_captcha()并传入验证码图片来尝试进行识别。

### 7. ip2Region.py
基于ip数据库的ip地址的地理位置区域判断。其中实现了3种方法以供调用，基于内存搜索的memorySearch()，基于二分搜索的binarySearch()，基于b-tree算法搜索的btreeSearch()。
可自行根据搜索速度需求来选择方法。

### 8. cgcs2000_to_wgs84.py
将cscs2000坐标系转为通用的wgs84坐标系。用到了pyproj里的Transformer库，本质属于"EPSG:4326", "EPSG:4490"的转换，使用示例：例如要转换经纬度为(121,31)的坐标，
则可以调用XYZ2LBH(*LBH2XYZ(121, 31, 0, 'wgs84'), 'cgcs2000')。

### 9. time_calculation.py
一个时间计数器，可用于倒计时并展示剩余时间。仅使用了python自带的time库。

入口函数为：wait_sleep()，第一项参数为预订的下一个最近日期的指定小时与分钟，例如，当前时间为4月1日20:47，如果传参(20,46),将会倒计时到4月2日的20:46。
第二项参数为提前开始秒数，会将第一项参数的时间减去此项描述，即为最终的倒计时结束时间。

## 🎉 贡献指南
如果您同样有很棒的库函数，可以fork本仓库，提交一些不错的代码到新分支，并向本仓库提交Pull requests，
在审核通过后，您的代码会加入到本仓库中。