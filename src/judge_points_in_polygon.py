
def is_point_in_polygon(point, rangelist, judge_rectangle=False):
    """
        :param point: 待判定点坐标([121.123456,31.123456])
        :type point:list

        :param rangelist: 多边形坐标点集合,必须是按边连续的([[121.123456,31.123456],[121.223456,31.223456],...])
        :type rangelist:list

        :param judge_rectangle:可选参数,是否要先判断点是否在多边形的外接矩形内。
        :type judge_rectangle:bool


        :return: 待判定点是否在多边形内（包含在点和线段上的情况）(True/False)
        :rtype:bool
    """
    if judge_rectangle:
        # 判断是否在外包矩形内，如果不在，直接返回false
        maxlng, minlng, maxlat, minlat = -1, 999, -1, 999
        cur_lng, cur_lat = -1, -1
        for i in range(len(rangelist) - 1):
            cur_lng, cur_lat = rangelist[i]
            if cur_lng > maxlng:
                maxlng = cur_lng
            elif cur_lng < minlng:
                minlng = cur_lng
            if cur_lat > maxlat:
                maxlat = cur_lat
            elif cur_lat < minlat:
                minlat = cur_lat
        if (point[0] > maxlng or point[0] < minlng or
                point[1] > maxlat or point[1] < minlat):
            return False

    count = 0
    point1 = rangelist[0]
    for i in range(1, len(rangelist)):
        point2 = rangelist[i]
        # 点与多边形顶点重合
        if (point[0] == point1[0] and point[1] == point1[1]) or (point[0] == point2[0] and point[1] == point2[1]):
            # print("在顶点上")
            return True
        # 判断线段两端点是否在射线两侧 不在肯定不相交 射线（-∞，lat）（lng,lat）
        if (point1[1] < point[1] and point2[1] >= point[1]) or (point1[1] >= point[1] and point2[1] < point[1]):
            # 求线段与射线交点 再和lat比较
            point12lng = point2[0] - (point2[1] - point[1]) * (point2[0] - point1[0]) / (point2[1] - point1[1])
            # 点在多边形边上
            if (point12lng == point[0]):
                # print("点在多边形边上")
                return True
            if (point12lng < point[0]):
                count += 1
        point1 = point2
    if count % 2 == 0:
        return False
    else:
        return True


def main():
    return


if __name__ == '__main__':
    main()
