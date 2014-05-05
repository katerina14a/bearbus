#!/usr/bin/python
import csv
import htmlentitydefs
import re
from django.core.management.base import BaseCommand
import urllib2
from xml.dom.minidom import parseString
from bus.models import Route, Stops

def uniqify(seq):
    set = {}
    map(set.__setitem__, seq, [])
    return set.keys()

def unescape(text):
    def fix_up(m):
        text = m.group(0)
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text
    return re.sub("&#?\w+;", fix_up, text)


def sync():

    # make sure to only get stops serviced by actransit & perimeter (with csv)
    # actransit: http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=actransit
    #   returns list of <route tag="F" title="F"/><route tag="BSD" title="Broadway Shuttle Weekdays"/>

    #update Route
    url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=actransit'
    data = urllib2.urlopen(url)
    response = data.read()
    dom = parseString(response)
    data.close()

    Route.objects.all().delete()
    for route_index in range(0, dom.getElementsByTagName('route').length):
        route = dom.getElementsByTagName('route')[route_index].toxml().split("\"")[1]
        Route(route_id=route).save()
    # Route(route_id="Perimeter").save()

    #update Stops
    Stops.objects.all().delete()
    # perimeter_schedule = csv.reader(open('/home/kat/PycharmProjects/BearBus/bustimes/static/perimeter.csv'))
    # for row in perimeter_schedule:
    #     Stops(intersection=row[0]).save()

    for route in Route.objects.all():
        url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=actransit&r=' + route.route_id
        data = urllib2.urlopen(url)
        response = data.read()
        dom = parseString(response)
        for stop in dom.getElementsByTagName('stop'):
            match = re.search(r'title="([^"]*)', unescape(stop.toxml()))
            if match:
                Stops(intersection=match.group(1)).save()
            else:
                break


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync()