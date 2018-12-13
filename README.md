# wrf_outfile_plot
WRF模型的运行结果需要借助如ARWpost+grads、NCL等后处理工具进行分析和绘图，但是python借助netcdf4扩展和matplotlib也可以读取和绘制nc文件，而且更加灵活。
本文档中的python脚本可以读取nc文件并绘制图件，脚本是以“NCEP FNL Operational Model Global Tropospheric Analyses, continuing from July 1999”源文件进行WRF模拟并输出结果文件作为测试文件。不同气象源文件的变量名称可能有所不同，脚本注释中也进行了提示，可以通过一定的方法来查看。
文档shapfile文件夹中存放了中国行政区划，在脚本中读取并绘制作为底图，若研究范围有所不同，可将需要范围的shp文件存入shapfile文件夹中，并在脚本中替换路径。

by meng xiangrui
