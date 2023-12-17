import rdflib
import matplotlib.pyplot as plt
from SPARQLWrapper import SPARQLWrapper, JSON
from irsx.xmlrunner import XMLRunner 
import pandas as pd 


class Academoney():
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
  sparql.setReturnFormat(JSON)
  sparql.setQuery("""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX : <http://dbpedia.org/resource/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
  SELECT  *  {
      ?s  rdf:type dbo:University.
      ?s  dbo:state ?state.
      ?state dbo:country  dbr:United_States.
      ?s dbo:endowment ?e.
      ?s  geo:long ?long.
      ?s geo:lat ?lat.
      ?s geo:geometry ?point.
        ?s dbo:numberOfUndergraduateStudents ?underGrads.
      ?s dbo:facultySize ?facultySize.
      ?s dbo:staff ?staff.
 ?s dbo:numberOfPostgraduateStudents ?postGrads.


} order by ?s
  
  """)
  



  def load(self):
    self.data = self.sparql.query().convert()  
  

  def get_endowment(self):
    '''
    A method to get the endowment
    '''
    d = filter (lambda x: float(x['e']['value'])>10000, self.data['results']['bindings'])
    return map(lambda x: float(x['e']['value']) ,d)

  def get_hist(self,data, bin, title, xlabel, fname):
    '''
    A method to return a histogram
    data -  list, array
    b - integer, # of bins
    title - string, title of hist figure
    '''
    plt.hist(data, bins = bin )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.savefig('../assets/'+fname)
    plt.show()
    
  def get_stanford_trustee(self, object_id = 201801979349301170) :
    '''
    get stanford trustees
    '''
    xml_runner = XMLRunner()
    parsed_filing = xml_runner.run_filing(object_id) 
    result = parsed_filing.get_result() 
    return [(e['PrsnNm'],e['TtlTxt']) for e in result[1]['groups']['Frm990PrtVIISctnA']]  

  def get_result(self,object_id):
    '''
    Method to get the result from an object_id
    '''
    xml_runner = XMLRunner()
    parsed_filing = xml_runner.run_filing(object_id) 
    return parsed_filing.get_result()

  def get_df(self):
    '''
    A method to return a dataframe from the json of the SPARQL
    '''
    df = pd.DataFrame({
                        'end':list(map(lambda x:float(x['e']['value']) ,self.data['results']['bindings']))  ,
                        'staff':list(map(lambda x:float(x['staff']['value']) ,self.data['results']['bindings'])),
                        'faclty_size':list(map(lambda x:float(x['facultySize']['value']) ,self.data['results']['bindings'])) ,
                        'undergrad': list(map(lambda x:float(x['underGrads']['value']) ,self.data['results']['bindings'])),
                        'post_grads':list(map(lambda x:float(x['postGrads']['value']) ,self.data['results']['bindings']))
                        })
    return df

  def get_loglog_scatter(self,xx,yy, title):
    '''
    A method to retun a loglog scatter plot
    xx, yy -  string columns names of df from get_df()
    title - string, title of plot.
    '''
    self.get_df().plot(kind='scatter', x=xx, y = yy, title=title, loglog=True, ylim=(1,1000000))
    plt.savefig('../assets/'+title+'.pdf')
    plt.show()


###
ac = Academoney()
#ac.load()
ac.get_stanford_trustee(object_id = 201713489349301036)
result = ac.get_result(201713489349301036)
  