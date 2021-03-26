#! env python3
# -*- coding : utf-8 -*-


import json
import time

import requests


class GeoAddress(object):
    address = {}
    '''
    location	经纬度坐标	        传入内容规则：经度在前，纬度在后，经纬度间以“,”分割，经纬度小数点后不要超过 6 位。如果需要解析多个经纬度的话，请用"|"进行间隔，并且将 batch 参数设置为 true，最多支持传入 20 对坐标点。每对点坐标之间用"|"分割。	必填	无
    poitype     返回附近POI类型	    以下内容需要 extensions 参数为 all 时才生效。	可选	无
                                        逆地理编码在进行坐标解析之后不仅可以返回地址描述，也可以返回经纬度附近符合限定要求的POI内容（在 extensions 字段值为 all 时才会返回POI内容）。设置 POI 类型参数相当于为上述操作限定要求。参数仅支持传入POI TYPECODE，可以传入多个POI TYPECODE，相互之间用“|”分隔。该参数在 batch 取值为 true 时不生效。获取 POI TYPECODE 可以参考POI分类码表
    radius	    搜索半径	        radius取值范围在0~3000，默认是1000。单位：米	可选	1000
    extensions	返回结果控制        extensions 参数默认取值是 base，也就是返回基本地址信息；	可选	base
                                        extensions 参数取值为 all 时会返回基本地址信息、附近 POI 内容、道路信息以及道路交叉口信息。
    batch	    批量查询控制	    batch 参数设置为 true 时进行批量查询操作，最多支持 20 个经纬度点进行批量地址查询操作。	可选	FALSE
                                        batch 参数设置为 false 时进行单点查询，此时即使传入多个经纬度也只返回第一个经纬度的地址解析查询结果。
    roadlevel	道路等级	        以下内容需要 extensions 参数为 all 时才生效。	可选	无
                                        可选值：0，1
                                        当roadlevel=0时，显示所有道路
                                        当roadlevel=1时，过滤非主干道路，仅输出主干道路数据
    sig	        数字签名	        请参考数字签名获取和使用方法	可选	无
    output	    返回数据格式类型    可选输入内容包括：JSON，XML。设置 JSON 返回结果数据将会以JSON结构构成；如果设置 XML 返回结果数据将以 XML 结构构成。	可选	JSON
    callback	回调函数	        callback 值是用户定义的函数名称，此参数只在 output 参数设置为 JSON 时有效。	可选	无
    homeorcorp	是否优化POI返回顺序 以下内容需要 extensions 参数为 all 时才生效。	可选	0
                                        homeorcorp 参数的设置可以影响召回 POI 内容的排序策略，目前提供三个可选参数：
                                        0：不对召回的排序策略进行干扰。
                                        1：综合大数据分析将居家相关的 POI 内容优先返回，即优化返回结果中 pois 字段的poi顺序。
                                        2：综合大数据分析将公司相关的 POI 内容优先返回，即优化返回结果中 pois 字段的poi顺序。

    '''

    def __init__(self, poitype='ALL', output='JSON', radius=1000, extensions='all', batch=False, roadlevel='1', homeorcorp=0):
        self.parameters = 'http://restapi.amap.com/v3/geocode/regeo?key=6560e81381db257f1cc892a7efb0ea9e&poitype=%s&output=%s&radius=%d&extensions=%s&batch=%s&roadlevel=%s&homeorcorp=%d' % (
            poitype, output, radius, extensions, batch, roadlevel, homeorcorp)
        self.output = output

    def get_address(self, *location):
        '''
        location:传入内容规则：经度在前，纬度在后，经纬度间以“,”分割，经纬度小数点后不要超过 6 位。
        geo = GeoAddress()
        add = geo.get_address(106.542193,29.744985)
        '''
        if len(location) < 2:
            raise Exception("经纬度错误：缺少经度或纬度")
        if len(location) > 2:
            raise Exception("经纬度错误：经纬度设置超过参数个数")
        url = self.parameters+'&location=%f,%f' % (location[0], location[1])
        r = requests.session()
        t = r.get(url=url)
        if t.status_code == 200:
            if self.output in ['json', 'JSON']:
                result = json.loads(t.text)
            else:
                result = t.text
        self.address['status'] = result['status']
        self.address["address"] = result['regeocode']['formatted_address']
        self.address["province"] = result['regeocode']['addressComponent']['province']
        self.address["city"] = result['regeocode']['addressComponent']['city']
        self.address["citycode"] = result['regeocode']['addressComponent']['citycode']
        self.address["district"] = result['regeocode']['addressComponent']['district']
        self.address["adcode"] = result['regeocode']['addressComponent']['adcode']
        self.address["township"] = result['regeocode']['addressComponent']['township']
        self.address["street"] = result['regeocode']['addressComponent']['streetNumber']['street'] + \
            result['regeocode']['addressComponent']['streetNumber']['number']
        self.address['village'] = []
        for vlg in result['regeocode']['pois']:
            self.address['village'].append(
                vlg['name'] + "（" + vlg['direction'] + '方向' + vlg['distance'] + "米）")
        return self.address
