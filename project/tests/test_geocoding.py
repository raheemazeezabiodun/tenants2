import requests_mock

from project import geocoding


def test_search_works():
    with requests_mock.Mocker() as m:
        m.get(geocoding.SEARCH_URL, json=EXAMPLE_SEARCH_RESULT)
        results = geocoding.search("150 court")
        assert results[0].properties.label == "150 COURT STREET, Brooklyn, New York, NY, USA"


EXAMPLE_SEARCH_RESULT = {
  "geocoding": {
    "version": "0.2",
    "attribution": "/v1/attribution",
    "query": {
      "text": "150 court",
      "size": 10,
      "private": False,
      "lang": {
        "name": "English",
        "iso6391": "en",
        "iso6393": "eng",
        "defaulted": True
      },
      "querySize": 20,
      "parser": "addressit",
      "parsed_text": {
        "street": "150 court",
        "regions": []
      }
    },
    "engine": {
      "name": "Pelias",
      "author": "Mapzen",
      "version": "1.0"
    },
    "timestamp": 1535544972061
  },
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -73.993,
          40.6889
        ]
      },
      "properties": {
        "id": "692174",
        "gid": "nycpad:address:692174",
        "layer": "address",
        "source": "nycpad",
        "source_id": "692174",
        "name": "150 COURT STREET",
        "housenumber": "150",
        "street": "COURT STREET",
        "postalcode": "11201",
        "confidence": 0.885,
        "accuracy": "point",
        "country": "United States",
        "country_gid": "whosonfirst:country:85633793",
        "country_a": "USA",
        "region": "New York State",
        "region_gid": "whosonfirst:region:0",
        "region_a": "NY",
        "county": "Kings County",
        "county_gid": "whosonfirst:county:3",
        "locality": "New York",
        "locality_gid": "whosonfirst:locality:0",
        "locality_a": "NYC",
        "borough": "Brooklyn",
        "borough_gid": "whosonfirst:borough:3",
        "label": "150 COURT STREET, Brooklyn, New York, NY, USA",
        "pad_bin": "3003069",
        "pad_bbl": "3002920026",
        "pad_orig_stname": "COURT STREET",
        "pad_geomtype": "bin",
        "pad_low": "144",
        "pad_high": "152"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -74.20218,
          40.55466
        ]
      },
      "properties": {
        "id": "4384282",
        "gid": "nycpad:address:4384282",
        "layer": "address",
        "source": "nycpad",
        "source_id": "4384282",
        "name": "150 CODY COURT",
        "housenumber": "150",
        "street": "CODY COURT",
        "postalcode": "10312",
        "confidence": 0.883,
        "accuracy": "point",
        "country": "United States",
        "country_gid": "whosonfirst:country:85633793",
        "country_a": "USA",
        "region": "New York State",
        "region_gid": "whosonfirst:region:0",
        "region_a": "NY",
        "county": "Richmond",
        "county_gid": "whosonfirst:county:5",
        "locality": "New York",
        "locality_gid": "whosonfirst:locality:0",
        "locality_a": "NYC",
        "borough": "Staten Island",
        "borough_gid": "whosonfirst:borough:5",
        "label": "150 CODY COURT, Staten Island, New York, NY, USA",
        "pad_bin": "5116538",
        "pad_bbl": "5060260047",
        "pad_orig_stname": "CODY PLACE",
        "pad_geomtype": "bin",
        "pad_low": "150",
        "pad_high": "150"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -73.9654,
          40.57518
        ]
      },
      "properties": {
        "id": "1667739",
        "gid": "nycpad:address:1667739",
        "layer": "address",
        "source": "nycpad",
        "source_id": "1667739",
        "name": "150 BRIGHTWATR COURT",
        "housenumber": "150",
        "street": "BRIGHTWATR COURT",
        "postalcode": "11235",
        "confidence": 0.881,
        "accuracy": "point",
        "country": "United States",
        "country_gid": "whosonfirst:country:85633793",
        "country_a": "USA",
        "region": "New York State",
        "region_gid": "whosonfirst:region:0",
        "region_a": "NY",
        "county": "Kings County",
        "county_gid": "whosonfirst:county:3",
        "locality": "New York",
        "locality_gid": "whosonfirst:locality:0",
        "locality_a": "NYC",
        "borough": "Brooklyn",
        "borough_gid": "whosonfirst:borough:3",
        "label": "150 BRIGHTWATR COURT, Brooklyn, New York, NY, USA",
        "pad_bin": "3256962",
        "pad_bbl": "3086840086",
        "pad_orig_stname": "BRIGHTWATER COURT",
        "pad_geomtype": "bbl",
        "pad_low": "126",
        "pad_high": "218"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -73.93923,
          40.57957
        ]
      },
      "properties": {
        "id": "1678448",
        "gid": "nycpad:address:1678448",
        "layer": "address",
        "source": "nycpad",
        "source_id": "1678448",
        "name": "150 NORFOLK COURT",
        "housenumber": "150",
        "street": "NORFOLK COURT",
        "postalcode": "11235",
        "confidence": 0.881,
        "accuracy": "point",
        "country": "United States",
        "country_gid": "whosonfirst:country:85633793",
        "country_a": "USA",
        "region": "New York State",
        "region_gid": "whosonfirst:region:0",
        "region_a": "NY",
        "county": "Kings County",
        "county_gid": "whosonfirst:county:3",
        "locality": "New York",
        "locality_gid": "whosonfirst:locality:0",
        "locality_a": "NYC",
        "borough": "Brooklyn",
        "borough_gid": "whosonfirst:borough:3",
        "label": "150 NORFOLK COURT, Brooklyn, New York, NY, USA",
        "pad_bin": "3246687",
        "pad_bbl": "3087560019",
        "pad_orig_stname": "NORFOLK STREET",
        "pad_geomtype": "bin",
        "pad_low": "150",
        "pad_high": "150"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -73.9654,
          40.57518
        ]
      },
      "properties": {
        "id": "1667738",
        "gid": "nycpad:address:1667738",
        "layer": "address",
        "source": "nycpad",
        "source_id": "1667738",
        "name": "150 BRIGHTWATER COURT",
        "housenumber": "150",
        "street": "BRIGHTWATER COURT",
        "postalcode": "11235",
        "confidence": 0.881,
        "accuracy": "point",
        "country": "United States",
        "country_gid": "whosonfirst:country:85633793",
        "country_a": "USA",
        "region": "New York State",
        "region_gid": "whosonfirst:region:0",
        "region_a": "NY",
        "county": "Kings County",
        "county_gid": "whosonfirst:county:3",
        "locality": "New York",
        "locality_gid": "whosonfirst:locality:0",
        "locality_a": "NYC",
        "borough": "Brooklyn",
        "borough_gid": "whosonfirst:borough:3",
        "label": "150 BRIGHTWATER COURT, Brooklyn, New York, NY, USA",
        "pad_bin": "3256962",
        "pad_bbl": "3086840086",
        "pad_orig_stname": "BRIGHTWATER COURT",
        "pad_geomtype": "bbl",
        "pad_low": "126",
        "pad_high": "218"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -74.08861,
          40.64415
        ]
      },
      "properties": {
        "id": "4173087",
        "gid": "nycpad:address:4173087",
        "layer": "address",
        "source": "nycpad",
        "source_id": "4173087",
        "name": "150 NORTHVIEW COURT",
        "housenumber": "150",
        "street": "NORTHVIEW COURT",
        "postalcode": "10301",
        "confidence": 0.881,
        "accuracy": "point",
        "country": "United States",
        "country_gid": "whosonfirst:country:85633793",
        "country_a": "USA",
        "region": "New York State",
        "region_gid": "whosonfirst:region:0",
        "region_a": "NY",
        "county": "Richmond",
        "county_gid": "whosonfirst:county:5",
        "locality": "New York",
        "locality_gid": "whosonfirst:locality:0",
        "locality_a": "NYC",
        "borough": "Staten Island",
        "borough_gid": "whosonfirst:borough:5",
        "label": "150 NORTHVIEW COURT, Staten Island, New York, NY, USA",
        "pad_bin": "5149632",
        "pad_bbl": "5000540043",
        "pad_orig_stname": "NORTHVIEW COURT",
        "pad_geomtype": "bin",
        "pad_low": "150",
        "pad_high": "150"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -74.08861,
          40.64415
        ]
      },
      "properties": {
        "id": "4173086",
        "gid": "nycpad:address:4173086",
        "layer": "address",
        "source": "nycpad",
        "source_id": "4173086",
        "name": "150 NORTH VIEW COURT",
        "housenumber": "150",
        "street": "NORTH VIEW COURT",
        "postalcode": "10301",
        "confidence": 0.88,
        "accuracy": "point",
        "country": "United States",
        "country_gid": "whosonfirst:country:85633793",
        "country_a": "USA",
        "region": "New York State",
        "region_gid": "whosonfirst:region:0",
        "region_a": "NY",
        "county": "Richmond",
        "county_gid": "whosonfirst:county:5",
        "locality": "New York",
        "locality_gid": "whosonfirst:locality:0",
        "locality_a": "NYC",
        "borough": "Staten Island",
        "borough_gid": "whosonfirst:borough:5",
        "label": "150 NORTH VIEW COURT, Staten Island, New York, NY, USA",
        "pad_bin": "5149632",
        "pad_bbl": "5000540043",
        "pad_orig_stname": "NORTHVIEW COURT",
        "pad_geomtype": "bin",
        "pad_low": "150",
        "pad_high": "150"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -73.81861,
          40.79888
        ]
      },
      "properties": {
        "id": "2554245",
        "gid": "nycpad:address:2554245",
        "layer": "address",
        "source": "nycpad",
        "source_id": "2554245",
        "name": "150-03 WATERSIDE COURT",
        "housenumber": "150-03",
        "street": "WATERSIDE COURT",
        "postalcode": "11357",
        "confidence": 0.656,
        "accuracy": "point",
        "country": "United States",
        "country_gid": "whosonfirst:country:85633793",
        "country_a": "USA",
        "region": "New York State",
        "region_gid": "whosonfirst:region:0",
        "region_a": "NY",
        "county": "Queens County",
        "county_gid": "whosonfirst:county:4",
        "locality": "New York",
        "locality_gid": "whosonfirst:locality:0",
        "locality_a": "NYC",
        "borough": "Queens",
        "borough_gid": "whosonfirst:borough:4",
        "label": "150-03 WATERSIDE COURT, Queens, New York, NY, USA",
        "pad_bin": "4518280",
        "pad_bbl": "4045060002",
        "pad_orig_stname": "WATERSIDE COURT",
        "pad_geomtype": "bin",
        "pad_low": "150-03",
        "pad_high": "150-03"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -73.81847,
          40.79889
        ]
      },
      "properties": {
        "id": "2554247",
        "gid": "nycpad:address:2554247",
        "layer": "address",
        "source": "nycpad",
        "source_id": "2554247",
        "name": "150-07 WATERSIDE COURT",
        "housenumber": "150-07",
        "street": "WATERSIDE COURT",
        "postalcode": "11357",
        "confidence": 0.656,
        "accuracy": "point",
        "country": "United States",
        "country_gid": "whosonfirst:country:85633793",
        "country_a": "USA",
        "region": "New York State",
        "region_gid": "whosonfirst:region:0",
        "region_a": "NY",
        "county": "Queens County",
        "county_gid": "whosonfirst:county:4",
        "locality": "New York",
        "locality_gid": "whosonfirst:locality:0",
        "locality_a": "NYC",
        "borough": "Queens",
        "borough_gid": "whosonfirst:borough:4",
        "label": "150-07 WATERSIDE COURT, Queens, New York, NY, USA",
        "pad_bin": "4518281",
        "pad_bbl": "4045060003",
        "pad_orig_stname": "WATERSIDE COURT",
        "pad_geomtype": "bin",
        "pad_low": "150-07",
        "pad_high": "150-07"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -73.81777,
          40.79852
        ]
      },
      "properties": {
        "id": "2554283",
        "gid": "nycpad:address:2554283",
        "layer": "address",
        "source": "nycpad",
        "source_id": "2554283",
        "name": "150-20 WATERSIDE COURT",
        "housenumber": "150-20",
        "street": "WATERSIDE COURT",
        "postalcode": "11357",
        "confidence": 0.656,
        "accuracy": "point",
        "country": "United States",
        "country_gid": "whosonfirst:country:85633793",
        "country_a": "USA",
        "region": "New York State",
        "region_gid": "whosonfirst:region:0",
        "region_a": "NY",
        "county": "Queens County",
        "county_gid": "whosonfirst:county:4",
        "locality": "New York",
        "locality_gid": "whosonfirst:locality:0",
        "locality_a": "NYC",
        "borough": "Queens",
        "borough_gid": "whosonfirst:borough:4",
        "label": "150-20 WATERSIDE COURT, Queens, New York, NY, USA",
        "pad_bin": "4518286",
        "pad_bbl": "4045060013",
        "pad_orig_stname": "WATERSIDE COURT",
        "pad_geomtype": "bin",
        "pad_low": "150-20",
        "pad_high": "150-20"
      }
    }
  ],
  "bbox": [
    -74.20218,
    40.55466,
    -73.81777,
    40.79889
  ]
}
