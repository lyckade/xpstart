#xpstart - a better way to start X-Plane

## Description
X-Plane 10 don't load the sceneries in alphabetic order. Cause of this the scenery designer don't have any possibilities to say when x-plane should load a scenery.

Specially with the new default airports it is necessery to have a programm which orders the sceneries on a way which makes sence.

For this xpstart reorders the sceneries over the scenery_packs.ini file. Documentation can be found at [http://developer.x-plane.com/2012/09/scenery-packs-the-new-rules/](http://developer.x-plane.com/2012/09/scenery-packs-the-new-rules/)

## Layers

X-Plane sceneries can be grouped what they do. It is important that the groups are loaded in the correct order. The following groups are ordered the way x-plane should load them: 


* **Library**: A library is part of the custom scenery folder. It just has objects inside, which can be used by other sceneries. These is the only group where it doesn't matter when it is loaded.
* **Ground mesh**: Defines the ground mesh of the x-plane world. If there would be a custom scenery just with a mesh inside it should be loaded with that group.
* **Phototextures**: The photot sceneries e.g. from simheaven.com, are sceneries just with textures inside. 
* **OSM scenery**: Automatic generated sceneries mostly from OpenStreetMap.
* **Default scenery**: The x-plane default sceneries.
* **Exclusion**: Exclusion sceneries just have exclusions inside. Thesese sceneries are necessary, when a custom scenery don't have any exclusions. That there are no problems it is the easiest way to make a scenery just with exclusions inside.
* **Airport pack**: Custom sceneries for sceneries with more than one airport.
* **Airport**: Custom sceneries for airports.
* **new add-ons**: Sceneries were it was not possible to find a layer automaticaly

## Classes
### Layergroup
Every scenery will be added to exactly one layergroup. There is a default layergroup which can be overwritten to a user action.
### Scenery
A class which collects information about a x-plane scenery. The information is about objects, and the apt.dat definition.
