
fetch('cytograph.json').then(response => {
  
  return response.json();
}).then(data => {
  // Work with JSON data here
 var diamond = data.nodes.filter(function(x){return x.data.shape == 'diamond'}).map(node => ({ 'name':node.data.name, 'dollar': node.data.balance, 'OPEID':node.data.id}));

 
 diamond = diamond.sort((a, b) => (a.dollar > b.dollar) ? 1 : -1)

 var diamond_data = [
   {
     y: diamond.map(function(x){ return x.name}),
     x: diamond.map(function(x) { return 1000*x.dollar}),
     type:'bar',
     orientation:'h'
   }
 ];

 Plotly.newPlot('InflowBar', diamond_data);



 var triangle = data.nodes.filter(function(x){return x.data.shape == 'triangle'}).map(node => ({ 'name':node.data.name, 'dollar': node.data.balance, 'donor_id':node.data.id}));
 
 triangle = triangle.sort((a, b) => (a.dollar > b.dollar) ? 1 : -1);

 var triangle_data = [
  {
    y: triangle.map(function(x){ return x.name}),
    x: triangle.map(function(x) { return 1000*x.dollar}),
    type:'bar',
    orientation:'h'
  }
];
Plotly.newPlot('DonorBar', triangle_data);
});