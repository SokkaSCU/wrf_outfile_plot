#!/usr/bin/env python
# coding=utf-8
# ==============================================================================
"""绘制WRF输出文件图"""
# ==============================================================================

# ==============================================================================
"""加载必要的python包"""
# ==============================================================================
import re
import netCDF4
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
# ==============================================================================

# ==============================================================================
"""定义绘制参数"""
# ==============================================================================
[timeindex,etaindex,type,cmap] = [0,0,'PB','RdYlBu']
# 在上一行中定义需要绘制的时间序数、垂直高度的层序数、需要绘制的气象要素代号、色带编号
# 其中气象要素代号可通过下行中被注释掉的输出函数进行查看
# print(dataset.variables.keys())
# 色带标号可前往"https://matplotlib.org/examples/color/colormaps_reference.html"
dataset = netCDF4.Dataset('文件路径')
# ==============================================================================

# ==============================================================================
"""提取相应数据"""
# ==============================================================================
timelist = dataset.variables['Times'][:] #时间变量
latlist = dataset.variables['XLAT'][:] #维度变量
lonlist = dataset.variables['XLONG'][:] #经度变量
etalist = dataset.variables['ZNU'][:] #垂直层数
# 不同数据源变量名称可能有所差异，可使用下行中被注释掉的输出函数进行查看
# print(dataset.variables.keys())
time = timelist[timeindex]
timestr = ''
for byte in time:
    timestr = timestr+byte.decode('utf-8')
eta = etalist[timeindex][etaindex]
lat = latlist[timeindex]
lon = lonlist[timeindex]
value = dataset.variables[type][:][timeindex][etaindex]
typedescription = re.compile('description: .*')\
                    .findall(str(dataset.variables[type]))[0][13:]
unit = re.compile('units: .*').findall(str(dataset.variables[type]))[0][7:]
# typedescription与unit读取了所绘制气象要素的描述和单位，若不能正常显示请使用下行被注释的
# 输出行查看描述信息，并修改正则表达式
# print(dataset.dimensions)
# valuearray = np.vstack((np.array(lon).reshape(-1),\
# ==============================================================================

# ==============================================================================
"""读取地图底图"""
# ==============================================================================
province_b = gpd.GeoDataFrame.from_file('~/shapfile/省级行政区.shp')['geometry']
province_b = province_b.to_crs({'init':'epsg:4326'})
# ==============================================================================

# ==============================================================================
"""绘图"""
# ==============================================================================
fig = plt.figure()
ax = fig.add_axes([0.05,0.05,0.8,0.9])
ax.contourf(lon,lat,value,8,alpha=1,cmap=cmap)
province_b.plot(ax=ax,color=(0,0,0,0),edgecolor=(0,0,0,1),linestyle='--')
ax.set_xlim(lon.min()-1,lon.max()+1),ax.set_ylim(lat.min()-1,lat.max()+4)
cax = fig.add_axes([0.86,0.06,0.03,0.8])
sm = plt.cm.ScalarMappable(cmap=cmap,\
                          norm=plt.Normalize(vmin=value.min(),vmax=value.max()))
sm._A = []
fig.colorbar(sm,cax=cax)
title = timestr+'/(Level='+str(etaindex+1)+')\n'+typedescription+'/('+unit+')'
fontprop = FontProperties(fname='/System/Library/Fonts/Times.ttc')
ax.text(lon.mean(),lat.max()+1.8,title,horizontalalignment='center',\
        verticalalignment='center',fontproperties=fontprop)
plt.show()
# ==============================================================================
