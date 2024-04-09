import geo
import networkx as nx
import json
import string
import os


def OS3EGraph():
    g = nx.Graph()
    paths = [
        ["Vancouver", "Seattle"],
        ["Seattle", "Missoula", "Minneapolis", "Chicago"],
        ["Seattle", "SaltLakeCity"],
        ["Seattle", "Portland", "Sunnyvale"],
        ["Sunnyvale", "SaltLakeCity"],
        ["Sunnyvale", "LosAngeles"],
        ["LosAngeles", "SaltLakeCity"],
        ["LosAngeles", "Tucson", "ElPaso"],
        ["SaltLakeCity", "Denver"],
        ["Denver", "Albuquerque", "ElPaso"],
        ["Denver", "KansasCity", "Chicago"],
        ["KansasCity", "Dallas", "Houston"],
        ["ElPaso", "Houston"],
        ["Houston", "Jackson", "Memphis", "Nashville"],
        ["Houston", "BatonRouge", "Jacksonville"],
        ["Chicago", "Indianapolis", "Louisville", "Nashville"],
        ["Nashville", "Atlanta"],
        ["Atlanta", "Jacksonville"],
        ["Jacksonville", "Miami"],
        ["Chicago", "Cleveland"],
        ["Cleveland", "Buffalo", "Boston", "NewYork", "Philadelphia", "Washington"],
        ["Cleveland", "Pittsburgh", "Ashburn", "Washington"],
        ["Washington", "Raleigh", "Atlanta"]
    ]
    
    for path in paths:
        for i in range(len(path) - 1):
            g.add_edge(path[i], path[i+1])
    
    return g



def write_json_file(filename, data):
    '''Given JSON data, write to file.'''
    json_file = open(filename, 'w')
    json.dump(data, json_file, indent = 4)


def read_json_file(filename):
    input_file = open(filename, 'r')
    return json.load(input_file)


METERS_TO_MILES = 0.000621371192
LATLONG_FILE = "os3e_latlong.json"


def lat_long_pair(node):
    return (float(node["Latitude"]), float(node["Longitude"]))


def dist_in_miles(data, src, dst):
    '''Given a dict of names and location data, compute mileage between.'''
    src_pair = lat_long_pair(data[src])
    src_loc = geo.xyz(src_pair[0], src_pair[1])
    dst_pair = lat_long_pair(data[dst])
    dst_loc = geo.xyz(dst_pair[0], dst_pair[1])
    return geo.distance(src_loc, dst_loc) * METERS_TO_MILES


def OS3EWeightedGraph():
    data = {}
    g = OS3EGraph()
    longit = {}
    lat = {}
    # Get locations
    if os.path.isfile(LATLONG_FILE):
        print("Using existing lat/long file")
        data = read_json_file(LATLONG_FILE)
    else:
        return g

    for node in g.nodes():
        latit = float(data[node]["Latitude"])
        lon = float(data[node]["Longitude"])
        lat[node] = latit
        longit[node] = lon
    nx.set_node_attributes(g, lat, 'Latitude')
    nx.set_node_attributes(g, longit, 'Longitude')

    # Append weights
    for src, dst in g.edges():
        g[src][dst]["weight"] = dist_in_miles(data, src, dst)
        #print "%s to %s: %s" % (src, dst, g[src][dst]["weight"])
    return g
