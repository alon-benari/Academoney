console.log('cytograph.js')

fetch('cytograph.json').then(response => {
  
  return response.json();
}).then(data => {
  // Work with JSON data here
 


  

// render the network
  var cy = cytoscape({
    container: document.getElementById('cy'),
          style:[
          {
              selector: 'node.highlight',
              style: {
                  'border-color': '#000',
                  'border-width': '2px',
                  'color':'',
                  
              }
          },
          {
              selector:'edge',
              style:{
                'target-arrow-shape':'triangle',
                'curve-style': 'bezier',
                'width':function(elem){return elem.data('amount')},
                'line-color':'blue',
                'opacity':0.7
                
                
            }
              },
              {
			selector: 'node',
		    style: {
              'shape':'data(shape)',
              'label':'data(name)',
							'content': 'data(name)',
             'width':   function(elem){return elem.data('balance')},
             'height': function(elem){return elem.data('balance')},
             'font-size': 'mapData(hits, 100,1000,100,100000)' ,
              'background-color':'mapData(balance,0 ,1000, #0f0,  #f00)'
             
						}
					},

                  ],
        layout:{name:'concentric',
          concentric: function(node){
            return node.degree();
          },
          spacingFactor:100,
          minNodeSpacing:10,
          padding:10,
          fit:true,
          // animationDuration:1500,
          // animate:true,
          // concentric:'concentric',
          // boundingBox: { // to give cola more space to resolve initial overlaps
          //       x1: 0,
          //       y1: 0,
          //       x2: 1000,
          //       y2: 1000
          //     }
              },   
       

          elements: 
                data
  
  })
}).catch(err => {
  // Do something for an error here
});






