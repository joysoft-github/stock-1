# -*-coding=utf-8-*-
import datetime
import os
import sys
from optparse import OptionParser

__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''

import pandas as pd
import talib
import tushare as ts
import matplotlib as mpl
from mpl_finance import candlestick2_ochl,volume_overlay
from matplotlib  import pyplot as plt
from setting import get_engine
mpl.rcParams['font.sans-serif'] = ['simhei']
mpl.rcParams['axes.unicode_minus'] = False
api=ts.get_apis()

def plot_stock_line(code,name,start='2017-10-01',save=False):
    engine = get_engine('db_stock',local=True)
    today =datetime.datetime.now().strftime('%Y-%m-%d')
    fig = plt.figure(figsize=(10,8))
    base_info = pd.read_sql('tb_basic_info',engine,index_col='index')


    # fig,(ax,ax2)=plt.subplots(2,1,sharex=True,figsize=(16,10))
    ax=fig.add_axes([0,0.3,1,0.55])
    ax2=fig.add_axes([0,0.1,1,0.25])
    if code is None and name is not None:
        code = base_info[base_info['name']==name]['code'].values[0]
        print code

    df = ts.bar(code, conn=api, start_date=start)
    df = df.sort_index()
    # df=df.sort_values(by='datetime')

    # print df.head(5)
    # name=u'和顺电气'
    if name is None:
        name = base_info[base_info['code']==code]['name'].values[0]

    df =df.reset_index()
    # df = ts.get_k_data('300141',start='2018-03-01')
    # df['date']=df['date'].dt.strftime('%Y-%m-%d')
    df['datetime']=df['datetime'].dt.strftime('%Y-%m-%d')
    sma5=talib.SMA(df['close'].values,5)
    sma20=talib.SMA(df['close'].values,10)
    # ax.set_xticks(range(0,len(df),20))
    # # ax.set_xticklabels(df['date'][::5])
    # ax.set_xticklabels(df['datetime'][::20])
    candlestick2_ochl(ax,df['open'],df['close'],df['high'],df['low'],width=0.5,colorup='r',colordown='g',alpha=0.6)
    title=u'{} {} {}'.format(today,code,name)
    ax.set_title(title)
    ax.plot(sma5)
    ax.plot(sma20)
    plt.grid(True)


    # df['vol'].plot(kind='bar')
    volume_overlay(ax2,df['open'],df['close'],df['vol'],width=0.5,alpha=0.8,colordown='g',colorup='r')
    ax2.set_xticks(range(0,len(df),1))
    # ax.set_xticklabels(df['date'][::5])
    ax2.set_xticklabels(df['datetime'][::1])
    # ax2.grid(True)

    plt.setp(ax2.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.grid(True)
    # plt.subplots_adjust(hspace=0)
    # plt.show()
    if save:
        path = os.path.join(os.path.dirname(__file__),'data')
        fig.savefig(os.path.join(path,title+'.png'))
    else:
        plt.show()
    plt.close()

if __name__ == '__main__':    
    parser = OptionParser()
    parser.add_option("-c", "--code",
                  dest="code",
                  help="-c 300141 #using code to find security")
    parser.add_option("-n", "--name",
                    dest="name",
                  help="-n  和顺电气 #using code to find security")

    (options, args) = parser.parse_args()
    
    if len((sys.argv))>=2:
        code =options.code
        name =options.name
        name=name.decode('utf-8')
    else:
        code=None
        name=u'泰永长征'
    plot_stock_line(code=code,name=name,start='2018-02-01',save=False)
    ts.close_apis(api)