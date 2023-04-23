from cv2 import cv2
import numpy as np
from typing import Tuple


def get_matched_image_center(origin_img: np.ndarray, template_img: np.ndarray, min_match_count=5) \
        -> Tuple[int, int, int, int]:
    origin_img = cv2.cvtColor(origin_img, cv2.COLOR_BGR2GRAY) if len(origin_img.shape) > 2 else origin_img
    template_img = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY) if len(template_img.shape) > 2 else template_img
    # Initiate SIFT detector创建sift检测器
    sift = cv2.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(template_img, None)
    kp2, des2 = sift.detectAndCompute(origin_img, None)
    # 创建设置FLANN匹配
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    good = []
    # 舍弃大于0.7的匹配
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
    if len(good) >= min_match_count:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        h, w = template_img.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        # x_value = [p[0][0] for p in dst]
        # y_value = [p[0][1] for p in dst]
        # centroid_x, centroid_y = (round(sum(x_value) / len(dst)), round(sum(y_value) / len(dst)))
        bbox_x, bbox_y, bbox_w, bbox_h = cv2.boundingRect(dst)
        return bbox_x, bbox_y, bbox_w, bbox_h
    else:
        err_msg = "Not enough matches are found - %d/%d" % (len(good), min_match_count)
        # print(err_msg)
        raise Exception(err_msg)


def FAST_SIFT_BruteForce(origin_img, template_img):
    orb = cv2.FastFeatureDetector_create(50)
    kp1 = orb.detect(template_img, None)
    kp2 = orb.detect(origin_img, None)
    sift = cv2.SIFT_create()
    kp1, des1 = sift.compute(template_img, kp1)
    kp2, des2 = sift.compute(template_img, kp2)
    bf = cv2.BFMatcher()
    matches = bf.radiusMatch(des1, des2, 100)
    return kp1, kp2, des1, des2, matches


def test():
    #
    '''
    基于FLANN的匹配器(FLANN based Matcher)
    1.FLANN代表近似最近邻居的快速库。它代表一组经过优化的算法，用于大数据集中的快速最近邻搜索以及高维特征。
    2.对于大型数据集，它的工作速度比BFMatcher快。
    3.需要传递两个字典来指定要使用的算法及其相关参数等
    对于SIFT或SURF等算法，可以用以下方法：
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    对于ORB，可以使用以下参数：
    index_params= dict(algorithm = FLANN_INDEX_LSH,
                       table_number = 6, # 12   这个参数是searchParam,指定了索引中的树应该递归遍历的次数。值越高精度越高
                       key_size = 12,     # 20
                       multi_probe_level = 1) #2
    '''
    from matplotlib import pyplot as plt
    MIN_MATCH_COUNT = 5  # 设置最低特征点匹配数量为10
    template_img = cv2.imread('../auto_buy_meiriyouxian_gui_images/test_template.png', cv2.IMREAD_GRAYSCALE)
    origin_img = cv2.imread('../auto_buy_meiriyouxian_gui_images/test1.png', cv2.IMREAD_GRAYSCALE)  # 读取要匹配的灰度照片
    # Initiate SIFT detector创建sift检测器
    sift = cv2.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(template_img, None)
    kp2, des2 = sift.detectAndCompute(origin_img, None)
    # 创建设置FLANN匹配
    FLANN_INDEX_KDTREE = 1
    FLANN_INDEX_LSH = 6

    # index_params = dict(algorithm=FLANN_INDEX_LSH,
    #     table_number=48,  # 12
    #     key_size=100,  # 20
    #     multi_probe_level=5)  # 2
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # store all the good matches as per Lowe's ratio test.
    # kp1, kp2, des1, des2, matches = FAST_SIFT_BruteForce(origin_img, template_img)
    good = []
    # 舍弃大于0.7的匹配
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
    # for mm in matches:
    #     for m in mm:
    #         good.append(m)
    print(len(good))
    if len(good) >= MIN_MATCH_COUNT:
        # 获取关键点的坐标
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        # 计算变换矩阵和MASK
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()
        h, w = template_img.shape
        # 使用得到的变换矩阵对原图像的四个角进行变换，获得在目标图像上对应的坐标
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        cv2.polylines(origin_img, [np.int32(dst)], True, 0, 2, cv2.LINE_AA)
    else:
        print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
        matchesMask = None
        # return (-1,-1)
    draw_params = dict(matchColor=(0, 255, 0),
        singlePointColor=(255, 0, 0),
        matchesMask=matchesMask,
        flags=0)
    result = cv2.drawMatches(template_img, kp1, origin_img, kp2, good, None, **draw_params)
    plt.imshow(result, 'gray')
    plt.show()
    return


if __name__ == '__main__':
    test()
