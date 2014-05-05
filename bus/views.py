# Create your views here.
import csv
import htmlentitydefs
import re
import urllib2
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from xml.dom.minidom import parseString
from bus.models import Route, Stops

#request.user will give you a User object representing the currently logged-in user.
# If a user isn't currently logged in, request.user will be set to an instance of
# AnonymousUser (see the previous section). You can tell them apart with is_authenticated()

def home(request):
    return render_to_response('home.html',  {'stops': Stops.objects.all(), 'routes': Route.objects.all()})


# def routes(request):
# #    url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=actransit'
# #    data = urllib2.urlopen(url)
# #    response = data.read()
# #    dom = parseString(response)
# #    routes = [0] * dom.getElementsByTagName('route').length
# #    for route_index in range(0, dom.getElementsByTagName('route').length):
# #        routes[route_index] = dom.getElementsByTagName('route')[route_index].toxml().split("\"")[1]
# #        try:
# #            Route.objects.get(route_id=routes[route_index])
# #        except:
# #            Route(route_id=routes[route_index]).save()
# #        try:
# #            Route.objects.get(route_id="Perimeter")
# #        except:
# #            Route(route_id="Perimeter").save()
#     return render_to_response('routes.html', {'routes': Route.objects.all()})


def route_stops(request, route_id):
    if route_id == "Perimeter":
        perimeter_schedule = csv.reader(open('/home/kat/PycharmProjects/BearBus/bustimes/static/perimeter.csv'))
        perimeter_stops = []
        for row in perimeter_schedule:
            perimeter_stops.append(row[0])
        return render_to_response('route_stops.html', {'stops': perimeter_stops})
    else:
        def unescape(text):
            def fix_up(m):
                text = m.group(0)
                if text[:2] == "&#":
                    # character reference
                    try:
                        if text[:3] == "&#x":
                            return unichr(int(text[3:-1], 16))
                        else:
                            return unichr(int(text[2:-1]))
                    except ValueError:
                        pass
                else:
                    # named entity
                    try:
                        text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                    except KeyError:
                        pass
                return text # leave as is

            return re.sub("&#?\w+;", fix_up, text)

        url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=actransit&r=' + route_id
        data = urllib2.urlopen(url)
        response = data.read()
        dom = parseString(response)
        stops = []
        for stop in dom.getElementsByTagName('stop'):
            match = re.search(r'title="([^"]*)', unescape(stop.toxml()))
            if match:
                stops.append(match.group(1))
            else:
                break
        return render_to_response('route_stops.html', {'stops': stops})


# def login_user(request):
#     state = "Please log in below..."
#     username = password = ''
#     if request.POST:
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 state = "You're successfully logged in!"
#             else:
#                 state = "Your account is not active, please contact the site admin."
#         else:
#             state = "Your username and/or password were incorrect."
#     c = {'state':state, 'username': username}
#     c.update(csrf(request))
#     return render_to_response('login_user.html', c)


def stops(request):
#    def uniqify(seq):
#        set = {}
#        map(set.__setitem__, seq, [])
#        return set.keys()
#
#    def unescape(text):
#        def fix_up(m):
#            text = m.group(0)
#            if text[:2] == "&#":
#                # character reference
#                try:
#                    if text[:3] == "&#x":
#                        return unichr(int(text[3:-1], 16))
#                    else:
#                        return unichr(int(text[2:-1]))
#                except ValueError:
#                    pass
#            else:
#                # named entity
#                try:
#                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
#                except KeyError:
#                    pass
#            return text # leave as is
#
#        return re.sub("&#?\w+;", fix_up, text)
#
#    perimeter_schedule = csv.reader(open('/home/kat/PycharmProjects/BearBus/bustimes/static/perimeter.csv'))
#    all_stops = []
#    for row in perimeter_schedule:
#        all_stops.append(row[0])
#
#    common_routes=["F","18","51B","49","1","1R","FS","52","88"]
#    for route in common_routes:
#        url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=actransit&r=' + route
#        data = urllib2.urlopen(url)
#        response = data.read()
#        dom = parseString(response)
#        for stop in dom.getElementsByTagName('stop'):
#            match = re.search(r'title="([^"]*)', unescape(stop.toxml()))
#            if match:
#                all_stops.append(match.group(1))
#            else:
#                break
#
#    all_stops = uniqify(all_stops)
#    all_stops.sort()
#    return render_to_response('stops.html', {'stops': all_stops})
    return render_to_response('stops.html', {'stops': Stops.objects.all()})


def saved_stops(request):
    return render_to_response('saved_stops.html')


def logout(request):
    return render_to_response('logout.html')