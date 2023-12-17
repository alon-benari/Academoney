import pandas as pd
import networkx as nx
from networkx.readwrite.json_graph import cytoscape_data
import json
from matplotlib import pyplot as plt


class ForeignGift:
  '''
  A method for network analysis approach to Foreign Gifts from the 
  https://studentaid.gov/data-center/school/foreign-gifts
  '''
  def __init__(self):
    N=10000
    self.k =1000 # scaler
    self.G = nx.DiGraph()
    
    self.data = pd.read_csv('../assets/ForeignGift.csv')#.iloc[:N,:]


    self.data['year'] = self.data['GiftReceivedDate'].apply(lambda x: x.split('/')[2]) 
    #
    d_country = self.set_giftor_id('CountryGiftor')
    self.data['country_id'] = self.data['CountryGiftor'].apply(lambda x : d_country[x])
    #
    d_institute = self.set_giftor_id('GiftorName')
    self.data['institute_id'] = self.data['GiftorName'].apply(lambda x: d_institute[x])
    #
    self.data.dropna(inplace=True)
    #
    

    #
    # Make the graph


  def id2shape(self):
    '''
    A method to return a dictionary mapping id to shape 
    '''
    shape = {}
    donor_shape =  {i:'triangle' for i in self.data['institute_id']} 
    univ_shape =  {i:'diamond' for i in self.data['OPEID']} 
    shape.update(donor_shape)
    shape.update(univ_shape)
    return shape


    
  def opeid2name(self):
    '''
    A method to return the name of the insitutution
    '''
    return self.data[['OPEID','Institution Name']].drop_duplicates().set_index('OPEID').to_dict()['Institution Name']
    
  def inst2country(self):
    '''
    return a dictionary of institute id to country of origin
    '''
    return self.data[['institute_id','CountryGiftor']].drop_duplicates().set_index('institute_id').to_dict()['CountryGiftor']

  def inst2name(self):
    '''
    returnn a dictionary of institue id to institute name
    '''
    return self.data[['institute_id','GiftorName']].drop_duplicates().set_index('institute_id').to_dict()['GiftorName']
    

  def set_giftor_id(self,column):
    '''
    A method to generate a giftor id
    '''
    return  {g:i for i,g in enumerate(self.data[column].unique())}  



  def get_amount_country(self, data, opeid, country_id):
    '''
    A method to tell how much was given by a given country to a given opeid for a given dataset.
    '''
    q = 'country_id=='+ str(country_id) +' & OPEID=='+ str(opeid)
    return data.query(q)


  def get_amount_institue(self, data, opeid, institute_id):
    '''
    A method to tell how much was given by a given instituted to a given opeid for a given dataset.
    '''
    q = 'institute_id=='+ str(country_id) +' & OPEID=='+ str(opeid)
    return data.query(q)


  
  def set_edge_institute(self,data ):
    '''
    A method to return an edgelist of institue -> universtiy.
    Will return the graph with edges.
    data -  dataframe to create an edgelist from.
    
    '''
    edge_dict =list(map( lambda x: {x:data[data.OPEID==x]['institute_id'].unique()}, data.OPEID.unique() ))
    e = []
    for l in edge_dict:      
        for t,s in l.items():
          e.append(self.set_edges(s,t))
    for edge_set  in e:
      self.G.add_edges_from(edge_set)

    for e1,e2 in self.G.edges():
      self.G[e1][e2]['count'] = int(data.query('OPEID == '+str(e2)+'& institute_id=='+str(e1)).shape[0])

    for e1,e2 in self.G.edges():
      self.G[e1][e2]['amount'] = int(data.query('OPEID == '+str(e2)+'& institute_id=='+str(e1)).ForeignGiftAmount.sum()/self.k)
    
    nx.set_node_attributes(self.G, self.inst2name(),'name')
    nx.set_node_attributes(self.G, self.inst2country(),'label') 
    nx.set_node_attributes(self.G, self.opeid2name(),'name')  
    #
    # some statistics
    # 
    
    nx.set_node_attributes(self.G,{x[0]:str(50+x[1]*10) for x in  dict(self.G.in_degree()).items()} , 'recipients')

    nx.set_node_attributes(self.G,{x[0]:str(50+x[1]*10) for x in  dict(self.G.out_degree()).items()} ,'donors')
    
    nx.set_node_attributes(self.G, self.get_univ_balance(data), 'balance')
    
    nx.set_node_attributes(self.G, self.get_donor_balance(data), 'balance')

    nx.set_node_attributes(self.G, self.id2shape(), 'shape')

    nx.set_node_attributes(self.G, {n:100*c for n,c in self.G.degree()}, 'hits')
   
  def get_univ_balance(self,data):
    '''
    return a dictionary for each OPEID  the total incoming domations
    '''
    return {opeid: data[data.OPEID == opeid].ForeignGiftAmount.sum()/self.k for opeid  in data.OPEID.unique()}

  def get_donor_balance(self, data):
    '''
    return the sum amount the  donor donated 
    '''
    return {id: data[data.institute_id == id].ForeignGiftAmount.sum()/self.k for id  in data.institute_id.unique()}



  def set_edges(self, source, target):
    '''
    create edge pairs
    '''
    edges = []
    for s in source:
      edges.append((int(s),int(target)))

    return edges

  def get_year_data(self,y):
    '''
    A method to return a parse dataset by year
    y - (string) the year to be parsed
    '''
    return self.data[self.data.year == y]

  def to_cytoscape(self):
    '''
    method to write the graph ready for cytoscape visualozation
    '''
    
    graph = cytoscape_data(self.G)
   
    with open('./cytoscape/cytograph.json','w') as f:
            json.dump(graph['elements'], f, indent = 4)
    return graph['elements']

###
fg = ForeignGift()   
d = fg.get_year_data('2019') 
fg.set_edge_institute(d)
g = fg.to_cytoscape()

