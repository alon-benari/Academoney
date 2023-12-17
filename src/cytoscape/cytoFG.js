console.log('cytograph.js')

fetch('cytograph.json').then(response => {
  console.log('reading')
  return response.json();
}).then(data => {
  // Work with JSON data here
  console.log(data);
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
                // 'width':function(elem){return 2*elem.data('count')},
                'line-color':'blue',
                'opacity':0.5
                
                
            }
              },
      //         {
			// selector: 'node',
		  //   style: {
			// 				'content': 'data(label)',
      //         'width':function(elem){return elem.data('width')},
      //         'height':'data(height)',
      //         'font-size':'30px',
      //         'label':'data(name)',
      //         'background-color':function(elem){return elem.data('color')},
      //       //   'background-color':'green',
      //         'background-color': 'mapData(color,0,30,green,red)'
			// 			}
			// 		},

                  ],
        layout:{name:'random',
          spacingFactor:20,
          nodeSpacing:40,
          padding:30,
          fit:true,
          animationDuration:150,
          animate:true,
          // concentric:'concentric',
          boundingBox: { // to give cola more space to resolve initial overlaps
                x1: 0,
                y1: 0,
                x2: 1000,
                y2: 1000
              }
              },        
          elements: 
                data
  
  })
}).catch(err => {
  // Do something for an error here
});






