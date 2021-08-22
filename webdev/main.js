import 'ol/ol.css';
import GeoJSON from 'ol/format/GeoJSON';
import Map from 'ol/Map';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import View from 'ol/View';
import {fromLonLat} from 'ol/proj';
import sync from 'ol-hashed';
import {Style, Fill, Stroke} from 'ol/style';

import Stamen from 'ol/source/Stamen';
import {Heatmap as HeatmapLayer, Tile as TileLayer} from 'ol/layer';


//Build with: npm run build
// test by moving to build directory and running 'ws'

// Stateman layer: http://maps.stamen.com/#terrain/12/37.7706/-122.3782
//layer options:  toner, toner-hybrid, toner-labels, toner-lines, toner-background, and toner-lite.

//Styles
const existingWays = new Style({
	  stroke: new Stroke({
		color: 'green',
		width: 2
	  })
	})

const proposedWays = new Style({
	stroke: new Stroke({
		color: 'red',
		width: 2
	})
	})

//Layers - Base
const stamenMap = new TileLayer({
	source: new Stamen({
	  layer: 'toner-lite',
	}),
  });
//Layers - Data
const bikelanes = new VectorLayer({
	source: new VectorSource({
		format: new GeoJSON(),
		url: './data/bikelanes.geojson'
	  }),
	style: function(feature, resolution) {
		const status = feature.get('status');
		const uses = feature.get('uses');
		return new Style({
			stroke: new Stroke({
			  color: status == "Existing" ? "green" : "red",
			  width: getWidth(uses)
			})
		  });
	  }
  });

// const test = new VectorLayer({
// 	source: new VectorSource({
//         format: new GeoJSON(),
//         url: './data/bikelanes.geojson'
// 	  }),
// 	  style: proposedWays
// });

// const test = new OlVector({
// 	source: new OlVectorSource({
//     	url: countries,
// 	  	format: new GeoJSON()
// 	})
//   });

const map = new Map({
  target: 'map-container',
  layers: [
    stamenMap,
	bikelanes
  ],
//   view: new View({
//     center: fromLonLat([0, 0]),
//     zoom: 2
//   })
  view: new View({
	center: fromLonLat([144.9631, -37.8136]),
    zoom: 14,
	minZoom: 10,
	maxZoom: 17,
	extent: [16004370.920654759, -4644851.540275239, 16270066.03097403, -4461402.672390816] 
  })
});


sync(map);

//Utils
function getWidth(uses) {
	return 1 + Math.min(Math.round(uses/150), 6);
}