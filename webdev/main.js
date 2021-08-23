import 'ol/ol.css';
import GeoJSON from 'ol/format/GeoJSON';
import Map from 'ol/Map';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import View from 'ol/View';
import {fromLonLat} from 'ol/proj';
import sync from 'ol-hashed';
import {Style, Fill, Stroke, Circle} from 'ol/style';

import Stamen from 'ol/source/Stamen';
import {Heatmap as HeatmapLayer, Tile as TileLayer} from 'ol/layer';


//Build with: npm run build
// test by moving to build directory and running 'ws'

// Stateman layer: http://maps.stamen.com/#terrain/12/37.7706/-122.3782
//layer options:  toner, toner-hybrid, toner-labels, toner-lines, toner-background, and toner-lite.

//Styles
const existingLanesColour = [0, 71, 171];
const proposedLanesColour = [255, 165, 0];

const incidentFatalStyle = new Style({
	image: new Circle({
		radius: 4,
		fill: new Fill({color: 'red'}),
		stroke: new Stroke({
		color: [255,255,255], width: 1
		})
	})
});

const incidentSeriousStyle = new Style({
	image: new Circle({
		radius: 3,
		fill: new Fill({
			color: 'black'
		}),
		stroke: new Stroke({
			color: [255,255,255], 
			width: 1
		})
	})
});

const incidentMinorStyle = new Style({
	image: new Circle({
		radius: 3,
		fill: new Fill({color: [175, 175, 175]}),
		stroke: new Stroke({
		color: [255,255,255], width: 1
		})
	})
});


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
		url: './data/bikelanesWeb.geojson'
	  }),
	style: function(feature, resolution) {
		const status = feature.get('status');
		const uses = feature.get('uses');
		return new Style({
			stroke: new Stroke({
			  color: status == "Existing" ? existingLanesColour : proposedLanesColour,
			  width: getWidth(uses)
			})
		});
	}
});

const incidentsFatal = new VectorLayer({
	source: new VectorSource({
		format: new GeoJSON(),
		url: './data/incidentFatal.geojson'
	  }),
	style: incidentFatalStyle
});

const incidentsSerious = new VectorLayer({
	source: new VectorSource({
		format: new GeoJSON(),
		url: './data/incidentSerious.geojson'
	  }),
	style: incidentSeriousStyle
});

const incidentsMinor = new VectorLayer({
	source: new VectorSource({
		format: new GeoJSON(),
		url: './data/incidentMinor.geojson'
	  }),
	style: incidentMinorStyle
});

// Maps and Views
const view = new View({
	center: fromLonLat([144.9631, -37.8136]),
    zoom: 14,
	minZoom: 10,
	maxZoom: 17,
	extent: [16004370.920654759, -4644851.540275239, 16270066.03097403, -4461402.672390816] 
  })

const map = new Map({
  target: 'map-container',
  layers: [
    stamenMap,
	bikelanes,
	incidentsMinor,
	incidentsSerious,
	incidentsFatal
  ],
  view: view
});

sync(map); // lock view on refresh

//Utils
function getWidth(uses) {
	return 1 + Math.min(Math.round(uses/150), 6);
}