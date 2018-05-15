import numpy as np
import pandas as pd
import re
import operator

class data():
# seperate type
  def getdf(self,filename):
        self.dataset = pd.read_excel('{}'.format(filename))
        key = self.dataset.keys()
        getstart = []
        date = []
        catagories = []
        values = []
        for i in key:
            gettype = {}
            a = self.dataset[i]
            gettype['colums'] = i
            types = np.dtype(a)
            gettype['type'] = types
            getstart.append(gettype)

        for i in getstart:
            if i['type'] == 'object':
                catagories.append(i['colums'])
            if i['type'] == 'float64' or i['type'] == 'int64':
                values.append(i['colums'])
            if i['type'] == 'datetime64[ns]':
                date.append(i['colums'])

        return date,catagories,values,key
#
  def getinfo(self,indexx,indexy,mdata,filter):
        plotlist = []
        dimentioncol = []
        valcol = []
        forcol = 0
        for i in indexx:
            plotlist.append(i)
            dimentioncol.append(forcol)
            forcol += 1
        for i in indexy:
            plotlist.append(i)
            valcol.append(forcol)
            forcol += 1
        df = mdata.iloc[:,plotlist].values
        df = pd.DataFrame(df)
        sorted_x = sorted(filter.items(), key=operator.itemgetter(0))
        indexs = 0
        sorted_2 = {}
        for i in sorted_x:
            sorted_2[indexs] = i[1]
            indexs += 1
        for i in sorted_2:
            df = df[df[i].isin(sorted_2[i])].groupby(dimentioncol)[valcol].sum().reset_index()
            print(df)
        inform = df.to_dict(orient='records')
        if [] == inform:
            df = mdata.iloc[:,plotlist].values
            df = pd.DataFrame(df)
            df = df.groupby(dimentioncol)[valcol].sum().reset_index()
            inform = df.to_dict(orient='records')
            print(df)
        saveval = []
        for i in inform:
            insidetup = list()
            for a in range(len(i)):
                if a == len(i)-1:
                    layer2 = list()
                    layer2.append(insidetup)
                    layer2.append(i[a])
                    saveval.append(layer2)
                else:
                    insidetup.append(i[a])
        return saveval

  def fordate(self,mdata,filter):
        spresult = list()
        setfilter = set()
        for i in filter:
            for a in filter[i]:
                setfilter.add(a)
        for i in mdata:
            setdata = set()
            for a in i[0]:
                setdata.add(str(a))
            forcount = setdata.intersection(setfilter)
            if len(forcount) == len(filter):
                spresult.append(i)
        return spresult


# range date
  def selectdate(self,xy,formatdmy):
      listselect = []
      otherselect = []
      for indexxy in xy:
          otherinlist = []
          for i in indexxy[0]:
              i = str(i)
              normal = re.compile(r'(?P<date>\d+\-\d+\-\d+)')
              new_indexxy = re.findall(normal,i)
              if new_indexxy != []:
                  new_indexxy = new_indexxy[0]
                  new_indexxy = new_indexxy.split('-')
              else:
                  otherinlist.append(i)
          listselect.append(new_indexxy)
          otherselect.append(otherinlist)
      if formatdmy == 'years':
          slice = 0
          forpd = self.selectlayer2(listselect,slice,xy,otherselect)
      elif formatdmy == 'dates':
          slice = 2
          forpd = self.selectlayer2(listselect,slice,xy,otherselect)
      elif formatdmy == 'months':
          slice = 1
          forpd = self.selectlayer2(listselect,slice,xy,otherselect)
      data = pd.DataFrame(forpd)
      data = data.groupby(['dateselect','itemselect']).agg({'count': np.sum})
      inform = data.to_dict()
      for i in inform:
        for a in inform[i]:
             xy = inform[i]
      b = sorted(xy.items(), key=lambda x: x[0])
      return b

# interested list
  def selectlayer2(self,listselect,slice,xy,otherselect):
      listselect2 = []
      slices = 0
      for i in range(len(xy)):
              newxy = {}
              year = str(listselect[slices][slice])
              newxy['dateselect'] = year
              newxy['itemselect'] = ','.join(otherselect[i])
              newxy['count'] = xy[slices][1]
              slices += 1
              listselect2.append(newxy)
      return listselect2






