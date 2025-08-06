# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 23:10:06 2021

@author: HYT,xx,syz,cqx
"""


def GetMainCalbeData():
    """
    Returns span_split_node,span_split_node_force,spans
    -------
    TYPE
        点，分点力，分跨数据.

    """
    ####    读取《主缆分跨点坐标-填入》    ####
    span_split_node = []

    with open('4-主缆分跨点坐标-填入.txt', 'r', encoding='utf-8') as f:
        flines = f.readlines()
    for i in flines:
        str_list = i.split('\n')[0].split(' ')
        str_list = [ii for ii in str_list if ii != '']
        span_split_node.append([eval(str_list[0]), eval(str_list[1])])

    # 读取文件--需要保证文件没有错误
    with open('1-成桥设计线型结果.txt', 'r', encoding='utf-8') as f:
        flines = f.readlines()

    ####    读取分点缆力    ####
    span_split_node_force = {}

    def jiequ(flines, str1_1, str2_1):
        jiequ_str_1 = []
        ifcunqu = 0
        for i in flines:
            if i == str1_1:
                ifcunqu = 1
            if i == str2_1:
                ifcunqu = 0
            if ifcunqu == 1:
                jiequ_str_1.append(i)
        return jiequ_str_1

    str1_1 = '@@@@@@@@@@@@@@@主索鞍处缆内力:\n'
    str2_1 = '@@@@@@@@@@@@@@@边索鞍处缆内力(锚跨侧为等效主缆):\n'
    j_str = jiequ(flines, str1_1, str2_1)[2:]
    for jiequ_str_1 in j_str:
        jiequ_str_1 = jiequ_str_1.split('\n')[0].split(' ')
        jiequ_str_1 = [i for i in jiequ_str_1 if i != '']
        cable_f = [eval(jiequ_str_1[-2]), eval(jiequ_str_1[-1])]
        cable_num = eval(jiequ_str_1[0])
        span_split_node_force[cable_num] = cable_f

    str1_2 = '@@@@@@@@@@@@@@@边索鞍处缆内力(锚跨侧为等效主缆):\n'
    str2_2 = '@@@@@@@@@@@@@@@\n'
    jiequ_str_2 = jiequ(flines, str1_2, str2_2)[2:]

    for i in jiequ_str_2:
        ii = i
        jiequ_str = ii.split('\n')[0].split(' ')
        jiequ_str = [iii for iii in jiequ_str if iii != '']
        cable_f = [eval(jiequ_str[-4]), eval(jiequ_str[-3])]
        cable_num = eval(jiequ_str[0])
        span_split_node_force[cable_num] = cable_f

    ####    读取分点标高、缆力    ####
    spans = []  # 分跨的数组信息
    # 分跨标高
    str1_3 = '@@@@@@@@@@@@@@@各分点线形与内力:\n'
    str2_3 = ''
    jiequ_str_3 = jiequ(flines, str1_3, str2_3)[1:]

    fenduan = []
    for i in range(len(jiequ_str_3)):
        if jiequ_str_3[i][0] == '第':
            fenduan.append(i)
    fenduan.append(len(jiequ_str_3))

    for i in range(len(fenduan) - 1):
        span = []
        for ii in range(fenduan[i], fenduan[i + 1]):
            span.append(jiequ_str_3[ii][3:-1])
        spans.append(span)
    ####    简单信息输出    ####
    print('Fun: GetMainCalbeData() 运行中...')
    print('读取分跨点数： ', len(span_split_node))
    print('读取分跨缆力数： ', len(span_split_node_force))
    print('读取主缆分点跨数： ', len(spans))
    for i, s in enumerate(spans):
        print('第', i + 1, '跨：共', len(s), '点。')
    print('Fun: GetMainCalbeData() 提取完成...')

    return span_split_node, span_split_node_force, spans


####    获取吊杆参数    ####
def GetHangerForce():
    """
    Returns
    有分点对应的吊杆力的数据
    -------
    TYPE
        hanger force data list .
    
    """
    with open('2-吊索理论下料长度.txt', 'r', encoding='utf-8') as f:
        flines = f.readlines()
    
    def numk(flines):
        """
        flines:输入的文件list
        numk:输出的list，为跨数，元素含义为第i跨
        """
        str1 = '            两端销铰式吊索长度(mm)'
        numk = []
        for i in flines:
            if i.split('---')[0] == str1:
                ifcunqu = 1
            else:
                ifcunqu = 0
            if ifcunqu == 1:
                numk.append(i[-3])
        return numk
    
    def lenlist(numk, flines):
        """
        numk:输入的list，为跨数，元素含义为第i跨
        flines:输入的文件list
        lenlist:输出的多重list，第一层为每跨对应的吊索参数集合，第二层为对应跨对应吊索号的吊索参数(第一个元素为吊索号)，第三层为对应的各个参数
        """
        str1 = '            两端销铰式吊索长度(mm)'
        str2 = '钢丝总重量'
        lenlist = []
        numk1 = []
        numk2 = []
        for i in flines:
            if i.split('---')[0] == str1:
                ifcunqu = 1
            else:
                ifcunqu = 0
            if ifcunqu == 1:
                numk1.append(flines.index(i))
            if i.split(':')[0] == str2:
                ifcunqu = 2
            else:
                ifcunqu = 0
            if ifcunqu == 2:
                numk2.append(flines.index(i))
        for i in range(len(numk)):
            m = []
            for ii in range(numk1[i] + 3, numk2[i]):
                ele = flines[ii]
                n = ele.split('\n')[0].split(' ')
                n = [i for i in n if i != '']
                m.append(n)
            lenlist.append(m)
        return lenlist
    
    numk = numk(flines)
    lenlist = lenlist(numk, flines)
    hanger_num = 0
    for i in lenlist:
        hanger_num = hanger_num + len(i)

    print('Fun: GetHangerForce() 运行中...')
    print('读取吊杆总数： ', hanger_num)
    print('Fun: GetHangerForce() 提取完成...')
    return lenlist


####    获取吊杆参数    ####
def GetHangerArea():
    """
    Returns
    所有分跨排序吊杆的截面积
    txt的输入中：必须输入首尾，
    吊杆面积不同时输入不同值
    不输入的默认使用前一个吊杆面积指
    -------
    TYPE
        hanger force data list .

    """
    with open('3-吊索编号及吊索面积.txt', 'r', encoding='utf-8') as f:
        flines = f.readlines()

    hanger_area = []
    r_start = 1
    r_end = 1

    ele = flines[0]
    n = ele.split('\n')[0].split(' ')
    n = [i for i in n if i != '']
    h_a = eval(n[1])
    for ele in flines:
        n = ele.split('\n')[0].split(' ')
        n = [i for i in n if i != '']
        r_end = eval(n[0])
        for ii in range(r_start, r_end - 1):
            hanger_area.append(h_a)
        hanger_area.append(eval(n[1]))
        h_a = eval(n[1])
        r_start = r_end
    print('Fun: GetHangerArea() 运行中...')
    print('读取吊杆面积总数： ', len(hanger_area))
    print('Fun: GetHangerArea() 提取完成...')
    return hanger_area


def WriteActiveExcel(E_list, cell_loc=(1, 1), New_HYT_Sheet=0):
    # 给定初始位置写入E_list
    # cell_loc = (1,1)
    # E_bound = 0 从头开始写
    # E_bound != 0 从指定位置开始写[2,2]
    import xlwings as xw
    try:
        wb = xw.books.active
        sheet = wb.sheets.active
    except:
        wb = xw.Book()
        sheet = wb.sheets.active
    if New_HYT_Sheet == 0:
        xw.Range(cell_loc).value = E_list
        print('已写入<' + sheet.name + '>' + str(len(E_list)) + '条记录!')
    elif New_HYT_Sheet == 1:
        i = 1
        while True:
            sheet_name = 'HYTSht' + str(i)
            try:
                sheet = wb.sheets.add(name=sheet_name, before=None, after=None)
                break
            except:
                i = i + 1
        sheet.range(cell_loc).value = E_list
        print('已写入<' + sheet_name + '>' + str(len(E_list)) + '条记录!')
    else:
        print('输入错误！')


def BLNASToMidas():
    """
    将本文件下的BLNAS数据转换为excel中：主缆坐标，主缆力，吊杆力
    Returns none
    -------
    None.

    """
    ####    主缆参数求解    ####
    # 主缆点
    span_split_node, span_split_node_force, spans = GetMainCalbeData()

    cable_node = [['x/m', 'y/m']]
    cable_force = []
    for i, n in enumerate(span_split_node):
        cable_node.append(n)
        cable_force.append(span_split_node_force[i + 1])
        try:
            s = spans[i]
            for ii in s:
                n = ii.split('\n')[0].split(' ')
                j = 0
                while j < len(n):
                    # 检测含有负号且负号不在首个字符
                    if n[j].find('-') != -1 and n[j][0] != '-':
                        tpStr = n[j].split('-')
                        n[j] = tpStr[0]
                        n.insert(j+1, '-' + tpStr[1])
                    j += 1

                n = [iii for iii in n if iii != '']
                cable_node.append([eval(n[1]), eval(n[2])])
                cable_force.append([eval(n[4]), eval(n[5])])
        except:
            pass
    WriteActiveExcel(cable_node, cell_loc=(1, 1), New_HYT_Sheet=1)

    # 主缆力
    cable_force_excel = [['缆段编号', '主缆力/kN']]
    for i in range(len(cable_force) - 1):
        cable_force_excel.append([i + 1, (cable_force[i][1] + cable_force[i + 1][0]) / 2])

    WriteActiveExcel(cable_force_excel, cell_loc=(1, 1), New_HYT_Sheet=1)
    # ####    吊杆参数求解    ####
    HangerForce = GetHangerForce()
    HangerArea = GetHangerArea()
    
    with open('5-吊索弹模.txt', 'r', encoding='utf-8') as f:
        flines = f.readlines()
    E = eval(flines[0])
    hanger_force = [['吊索编号', '吊索力/kN']]
    hanger_num = 0
    for i in HangerForce:
        for ii in i:
            # 对于骑跨式适用于骑跨部分的应变算的力
            # DL = eval(ii[3]) - eval(ii[7])
            # DR = eval(ii[4]) - eval(ii[8])
            # Davg = (DL + DR) / 2
            # WD = (eval(ii[8]) + eval(ii[7])) / 2
            # # print(ii[15])
            # w = eval(ii[15])
            # 上端减去下端是考虑了吊索重力
            Davg = (eval(ii[5]) + eval(ii[6])) / 2
            WD = (eval(ii[2]) + eval(ii[3])) / 2
           
            hanger_force.append([hanger_num + 1, Davg / WD * E * HangerArea[hanger_num]])
            hanger_num = hanger_num + 1
    
    WriteActiveExcel(hanger_force, cell_loc=(1, 1), New_HYT_Sheet=1)

if __name__ == "__main__":
    BLNASToMidas()
    a = input("程序运行完成，输入Enter退出！")