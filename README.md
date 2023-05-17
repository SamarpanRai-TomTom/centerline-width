# Centerline-Width
![PyPi](https://img.shields.io/pypi/v/centerline-width)
![license](https://img.shields.io/github/license/cyschneck/centerline-width)
[![NSF-2141064](https://img.shields.io/badge/NSF-2141064-blue)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2141064&HistoricalAwards=false)
[![pytests](https://github.com/cyschneck/centerline-width/actions/workflows/pytests.yml/badge.svg)](https://github.com/cyschneck/centerline-width/actions/workflows/pytests.yml)

Find the centerline and width of rivers based on the latitude and longitude positionss from the right and left bank 

* **Convert raw data from Google Earth Pro to CSV**
	* extractPointsToTextFile()
	* convertColumnsToCSV()
* **Find centerline and width of river**
	* centerlineLatitudeLongitude()
	* plotCenterline()
	* plotCenterlineWidth()
	* riverWidthFromCenterline()

| River Outlined in Google Earth Pro | Generated Centerline for the River Bank |
| ------------- | ------------- |
| ![river_google_earth+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_example_google_earth.png) | ![river_centerline+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_example.png) |

Python implementation of [R-Code CMGO](https://github.com/AntoniusGolly/cmgo) (with modification)

NOTE: This is Beta quality software that is being actively developed, use at your own risk. This project is not supported or endorsed by either JPL or NASA. The code is provided “as is”, use at your own risk.

## Requirements
Currently running on Python 3.7+

```
pip install -r requirements.txt
```
Requirements will also be downloaded as part of the pip download

## Install
PyPi pip install at [pypi.org/project/centerline-width/](https://pypi.org/project/centerline-width/)

```
pip install centerline-width
```

## Preprocessing
### Convert KML files to Text File

Convert two .kml files from Google Earth Pro (for the left and right bank) and export the coordinates into a text file

```
extractPointsToTextFile(left_kml=None,
			right_kml=None,
			text_output_name=None)
```

* **[REQUIRED]** left_kml (string): File location of the kml file for left bank
* **[REQUIRED]** right_kml (string): File location of the kml file for right bank
* **[REQUIRED]** text_output_name (string): Output file name (and location)

```python
import centerline_width
centerline_width.extractPointsToTextFile(left_kml="leftbank.kml",
					right_kml="rightbank.kml",
					text_output_name="data/river_coords_output.txt")
```
Output: The text file `data/river_coords_output.txt` with the headers `llat, llon, rlat, rlon` (for the left latitude, left longitude, right latitude, and right longitude)

Example:
```
     llat       llon      rlat       rlon
30.037581 -92.868569 30.119804 -92.907933
30.037613 -92.868549 30.119772 -92.907924
30.037648 -92.868546 30.119746 -92.907917
30.037674 -92.868536 30.119721 -92.907909
30.037702 -92.868533 30.119706 -92.907905
```

### Converted Text File to CSV

Convert a text file with coordinates for a left and right bank's latitude/longitude to a csv file

```
convertColumnsToCSV(text_file=None, flipBankDirection=False)
```
* **[REQUIRED]** text_file (string): File location of the text file to convert
* [OPTIONAL] flipBankDirection (boolean): If the latitude/longitude of the banks are generated in reverse order, flip the final values so left/right bank are in order

Scripts expects data as a list of point for left and right banks:
- Header: llat, llon, rlat, rlon

```python
import centerline_width
centerline_width.convertColumnsToCSV(text_file="data/river_coords.txt",
				flipBankDirection=True)
```
Converts text file:
```
     llat       llon      rlat       rlon
30.037581 -92.868569 30.037441 -92.867476
30.037613 -92.868549 30.037448 -92.867474
30.037648 -92.868546 30.037482 -92.867449
30.037674 -92.868536 30.037506 -92.867432
30.037702 -92.868533 30.037525 -92.867430
```
To a CSV file:
```
llat,llon,rlat,rlon
30.037581,-92.868569,30.037441,-92.867476
30.037613,-92.868549,30.037448,-92.867474
30.037648,-92.868546,30.037482,-92.867449
30.037674,-92.868536,30.037506,-92.867432
30.037702,-92.868533,30.037525,-92.867430
```
Output: A csv file `data/river_coords.csv` with the headers llat, llon, rlat, rlon

## Centerline and Width

### Types of Centerlines
- Voronoi centerline: centerline generated from where Voronoi vertices intersect within the river
- Evenly Spaced Centerline: centerline based on Voronoi centerline but evenly spaced with a fixed number of points
- Smoothed Centerline: centerline generated from the evenly spaced centerline but smoothed by a b-spline

### River Object
First, generate a river object to contain river data and available transformations
```
centerline_width.riverCenterline(csv_data=None, optional_cutoff=None)
```
* **[REQUIRED]** csv_data (string): File location of the text file to convert
* [OPTIONAL] optional_cutoff (int): Include only the first x amount of the data to chart (useful for debugging)

Object (class) attributes:

* river_name (string): name of object, set to the csv_data string
* df_len (int): length of the dataframe of the csv data spliced by the optional_cutoff
* left_bank_coordinates (list of two element lists): list of coordiantes of the left bank generated from the csv file
* right_bank_coordinates (list of two element lists) list of coordinates of the right bank generated from the csv file
* river_bank_polygon (Shapley Polygon): Multi-sided polygon generated to encapsulate river bank (used to define an inside and an outside of the river)
* top_bank (Shapley Linestring): A linestring that represents the top of the river/polygon
* bottom_bank (Shapley Linestring): A linestring that represents the bottom of the river/polygon
* starting_node (tuple): Tuple of the starting position of the centerline path
* ending_node (tuple): Tuple of the end position of the centerline path
* river_bank_voronoi (scipy Voronoi object): Voronoi generated by left/right banks
* centerline_latitude_longtiude (list of two element tuples): Latitude and Longitude coordinates of the centerline
* centerline_length (float): Length of the centerline of the river (in km)

```
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv")
```

### Return Latitude/Longitude Coordinates of Centerline
Return the latitude/longtiude coordinates of the centerline based on the left and right banks
```
river_object.centerline_latitude_longtiude
```
Centerline coordinates are formed from Voronoi vertices

```python
import centerline_width
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv", optional_cutoff=15)
river_centerline_coordinates = river_object.centerline_latitude_longtiude
```
Output is a list of tuples: (example) `[(-92.86788596499872, 30.03786596717931), (-92.86789573751797, 30.037834641974108), (-92.8679141386283, 30.037789636848878), (-92.8679251193248, 30.037756853899904), (-92.86796903819089, 30.03765423778148), (-92.86797335733262, 30.037643336049054), (-92.8679920356456, 30.037592224469797), (-92.86800576063828, 30.037555441489403), (-92.86800841510367, 30.037546512833107), (-92.8680119498663, 30.03753043193875)]`

### Return Length of Centerline
Return the length of the centerline found between the left and right bank
```
river_object.centerline_length
```
Length returned in kilometers
```python
import centerline_width
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv", optional_cutoff=550)
river_centerline_length = river_object.centerline_length
```
The length of the river object returns `215.34700589636674` km

## Plot Centerline in Matplotlib
### Plot the centerline created from a list of right and left banks with Voronoi vertices

```
plotCenterline(display_all_possible_paths=False, 
		plot_title=None, 
		save_plot_name=None, 
		display_voronoi=False)
```
* [OPTIONAL] display_all_possible_paths (boolean): Display all possible paths, not just the centerline (useful for debugging)
* [OPTIONAL] plot_title (string): Change plot title, defaults to "River Coordinates: Valid Centerline = True/False, Valid Polygon = True/False"
* [OPTIONAL] save_plot_name (string): Save the plot with a given name and location
* [OPTIONAL] display_voronoi (boolean): Overlay Voronoi diagram used to generate centerline

```python
import centerline_width
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv")
river_object.plotCenterline(display_all_possible_paths=False, display_voronoi=False)
```
Output:
![river_coords_centerline+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/river_coords_centerline.png)

## Plot Centerline Width Lines in Matplotlib
### Plot the Centerline Width Lines
Plot the width of the river based on the centerline

Display Centerline at even intervals from the Voronoi generated centerline
```
plotCenterlineWidth(plot_title=None, 
		save_plot_name=None, 
		display_true_centerline=True,
		n_interprolate_centerpoints=None,
		transect_span_distance=3,
		apply_smoothing=False,
		flag_intersections=True,
		remove_intersections=False)
```
* [OPTIONAL] plot_title (string): Change plot title, defaults to "River Coordinates: Valid Centerline = True/False, Valid Polygon = True/False"
* [OPTIONAL] save_plot_name (string): Save the plot with a given name and location
* [OPTIONAL] display_true_centerline (boolean): Display generated true centerline based on Voronoi diagrams
* [OPTIONAL] n_interprolate_centerpoints (int): Recreate centerline coordinates with n evenly spaced points, defaults to the number of rows in the csv file
* [OPTIONAL] transect_span_distance (int): Sum up n amount of points around a centerpoint to determine the slope (increase to decrease the impact of sudden changes), defaults to 6, must be greater than 2 (since the slope is found from the difference in position between two points), measured orthogonal to the centerline
* [OPTIONAL] apply_smoothing (bool): Apply a B-spline smoothing to centerline
* [OPTIONAL] flag_intersections (bool): Display intersecting width lines as red in graph, defaults to True
* [OPTIONAL] remove_intersections (bool): Iterative remove intersecting lines, to maintain the most width lines, but return only non-intersecting width lines, defaults to False

**apply_smoothing**

apply_smoothing applies a spline to smooth the centerline points created by the Voronoi vertices. This reduces the noise of the slopes and can create width lines that are less susceptible to small changes in the bank

| apply_smoothing=False | apply_smoothing=True |
| ------------- | ------------- |
| ![river_without_smoothing+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width_without_smoothing.png) | ![river_with_smoothing+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width_with_smoothing.png) |

**transect_span_distance**

Transect span describes the number of points that are averaged to generated a width line (example: transect_span_distance=3, average of three slopes)

![transect_span_distance](https://user-images.githubusercontent.com/22159116/227870492-69d105b2-0d3e-4d50-90d9-e938400a58fb.png)
| transect_span_distance=6 | transect_span_distance=30 |
| ------------- | ------------- |
| ![river_transect_6+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width_transect_6.png) | ![river_transect_30+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width_transect_30.png) |

**remove_intersections**

remove_intersections will remove the width lines that intersect other lines (that could be creating unrepresentative long width lines). Intersections are removed first in order from most to least (to ensure that the most width lines as possible are kept) and then, based on the longer of two intersecting lines

Intersecting lines are flagged in red by default (flag_intersections=True)

| remove_intersections=False | remove_intersections=True |
| ------------- | ------------- |
| ![river_keep+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width_keep_intersections.png) | ![river_remove+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width_remove_intersections.png)|

```python
import centerline_width
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv")
river_object.plotCenterlineWidth(save_plot_name="data/river_coords_width.png",
					display_true_centerline=False,
					n_interprolate_centerpoints=None,
					transect_span_distance=3,
					apply_smoothing=True,
					flag_intersections=True,
					remove_intersections=True)
```
![river_coords_width+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/river_coords_width.png)

### Return Width of River

Return the width of the river at each (evenly spaced) centerline coordinate

```
riverWidthFromCenterline(n_interprolate_centerpoints=None,
			transect_span_distance=3,
			apply_smoothing=True,
			remove_intersections=False,
			units="km",
			save_to_csv=None)
```
* [OPTIONAL] n_interprolate_centerpoints (int): Recreate centerline coordinates with n evenly spaced points, defaults to the number of rows in the csv file
* [OPTIONAL] transect_span_distance (int): Sum up n amount of points around a centerpoint to determine the slope (increase to decrease the impact of sudden changes), defaults to 6, must be greater than 2 (since the slope is found from the difference in position between two points), measured orthogonal to the centerline
* [OPTIONAL] apply_smoothing (bool): Apply a B-spline smoothing to centerline
* [OPTIONAL] remove_intersections (bool): Iterative remove intersecting lines, to maintain the most width lines, but return only non-intersecting width lines, defaultsl to True
* [OPTIONAL] units (string): Units to measure distance, options: ["km" (kilometers), "m" (meters), "mi" (miles), "nmi" (nautical miles), "ft" (feet), "in" (inches), "rad" (radians), "deg" (degrees)], defaults to "km" (kilometers)
* [OPTIONAL] save_to_csv (string): Save river width output to a csv file, defaults to None (no file is saved)

```python
import centerline_width
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv")
river_width_dict = river_object.riverWidthFromCenterline(transect_span_distance=3,
							apply_smoothing=True,
							units="km",
							remove_intersections=True)
```
Width dictionary = `{(-92.86792084788995, 30.037769672351182): 0.10969163557087018, (-92.86795038641004, 30.03769867854198): 0.10794219579997719}`

## Documentation and Algorithm to Determine Centerline

The centerline is defined by the greatest distance from the right and left bank, created from a Voronoi Diagram. The remaining paths within the river are filtered through Dijkstra's algorithm to find the shortest path that is the centerline

### Right and Left bank points are plotted (X-Axis for Latitude, Y-Axis for Longitude)
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example1.png)

### Generate a polygon to encapsulate the river between the right and left banks to define in and outside of river
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example2.png)

### Generate a Voronoi based on the points along the river banks
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example3.png)

### Display Voronoi ridge vertices that lie within the polygon (within the river banks)
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example4.png)

### Filter out any point pairs that only have one connections to filter out the short dead end paths and find the starting and ending node based on distance from the top and bottom of polygon
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example6.png)
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example7.png)

### Find the shortest path from the starting node to the ending node ([Dijkstra's Algorithm](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html#networkx.algorithms.shortest_paths.generic.shortest_path))
| Points on River Bank | NetworkX Graph of Points on River Bank |
| ------------- | ------------- |
| ![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example10.png) | ![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example9.png) |

### Display the centerline found by connecting the starting/ending node with the shortest path
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example8.png)

This is an attempt at a more robust algorithm working from raw data to ensure that all dead ends are removed and no gaps exist in the centerline

Points that only have one connection are removed, but by limiting the number of connections for a point to just two will create gaps. The Voronoi vertices connect to other vertex values, but some connect to more and some only connect to one other point. Removing additional values will create gaps, so this is avoided in this code by not applying additional filters.

**All vertices:**
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example4.png)

**Vertices that have at least two connections (that would create gaps):**
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example5.png)

## Debugging, Error Handling, and Edge Cases
### Edge Cases
If the data starts with a large width, it is possible for the starting node to be invalid
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/invalid_example3.png)
Currently, the starting node is determined by the closest node to the top of the bank (in green) and the ending node is determined by the closest node to the bottom of the bank (in red)

### Invalid Polygon
A polygon is invalid if it overlaps within itself:
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/invalid_example1.png)
In this example, the polygon is invalid, but with such a small overlap it is still able to find a valid path

With limited data, the polygon will overlap more dramatically and will no longer be able to find a valid centerline:
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/invalid_example4.png)

### Invalid Centerline
If the data is too small, a centerline and its coordinates cannot not be found (since only a single Voronoi vertex exists within the polygon and after deadends are filtered)

`CRITICAL ERROR, Voronoi diagram generated too small to find centerline (no starting node found), unable to plot centerline. Set displayVoronoi=True to view. Can typically be fixed by adding more data to expand range.`
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/invalid_example2.png)
Can be fixed by expanding the data until the polygon is large enough to contain at least two different vertex points

## Developer Notes: Tech Debt and Bug Fixes
* Return the length of the left/right bank in riverCenterline class (right_bank_length, left_bank_length)
* Verify that smoothing filter option does not produce a line that goes outside of the polygon
* Return the knickpoints (occurrences of knickpoints)

## Citations
Based on work written in R (Golly et al. 2017):

>Golly, A. and Turowski, J. M.: Deriving principal channel metrics from bank and long-profile geometry with the R package cmgo, Earth Surf. Dynam., 5, 557-570, https://doi.org/10.5194/esurf-5-557-2017, 2017.

[Github - CMGO](https://github.com/AntoniusGolly/cmgo)

 <p align="center">
  <img src="https://user-images.githubusercontent.com/22159116/222872092-e0b579cc-4f84-4f49-aa53-397785fb9bf2.png" />
  <img src="https://user-images.githubusercontent.com/22159116/222872119-7c485ee2-4ffd-413a-9e4f-b043b122d2bb.png" />
  <img src="https://user-images.githubusercontent.com/22159116/222872019-12931138-9e10-4e51-aa1e-552e72d09af0.png" />
</p>

This material is based upon work supported by the National Science Foundation Graduate Fellowship under Grant No. 2141064. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the atuhors and do not neccessarily reflect the views of the National Science Foundation.

## Bug and Feature Request

Submit a bug fix, question, or feature request as a [Github Issue](https://github.com/cyschneck/centerline-width/issues) or to ugschneck@gmail.com/cyschneck@gmail.com
