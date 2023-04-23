# Centerline-Width
![PyPi](https://img.shields.io/pypi/v/centerline-width)
![license](https://img.shields.io/github/license/cyschneck/centerline-width)
[![NSF-2141064](https://img.shields.io/badge/NSF-2141064-blue)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2141064&HistoricalAwards=false)

Find the centerline and width of rivers based on the latitude and longitude from the right and left bank 

| River Outlined in Google Earth Pro | Generated Centerline for the River Bank |
| ------------- | ------------- |
| ![river_google_earth+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_example_google_earth.png) | ![river_centerline+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_example.png) |


Python implementation of [R-Code CMGO](https://github.com/AntoniusGolly/cmgo) (with modification)

## Requirements
Currently running on Python 3.7+

```
pip install -r requirments.txt
```
Requirements will also be downloaded as part of the pip download

## Install
PyPi pip install at [pypi.org/project/centerline-width/](https://pypi.org/project/centerline-width/)

```
pip install centerline-width
```

## Running Scripts
### Convert KML files to Text File

Convert two .kml files from Google Earth Pro for the left and right bank and export the coordinates into a text file

```
extractPointsToTextFile(left_kml=None,
			right_kml=None,
			text_output_name=None)
```

* **[REQUIRED]** left_kml (string): File location of the kml file for left bank
* **[REQUIRED]** right_kml (string): File location of the kml file for right bank
* [OPTIONAL] text_output_name (string): Output file name (and location)

```python
import centerline_width
centerline_width.extractPointsToTextFile(left_kml="leftbank.kml",
					right_kml="rightbank.kml",
					text_output_name="data/river_coords_output.txt")
```
Output: A text file `data/river_coords_output.txt` with the headers llat, llon, rlat, rlon

### Converted Text File to CSV

Convert a text file with coordinates for a left and right bank's latitude/longitude to a csv file

```
     llat       llon      rlat       rlon
30.037581 -92.868569 30.119804 -92.907933
30.037613 -92.868549 30.119772 -92.907924
30.037648 -92.868546 30.119746 -92.907917
30.037674 -92.868536 30.119721 -92.907909
30.037702 -92.868533 30.119706 -92.907905
```

Scripts expect data as a list of point for left and right banks:
- Header: llat, llon, rlat, rlon

```
convertColumnsToCSV(text_file=None, flipBankDirection=False)
```
* **[REQUIRED]** text_file (string): File location of the text file to convert
* [OPTIONAL] flipBankDirection (boolean): If the latitude/longitude of the banks are generated in reverse order, flip the final values so left/right bank are in order

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

### Return Latitude/Longitude Coordinates of Centerline
Return a list of tuples for each latitude/longtiude coordinate of the centerline based on the left and right banks
```
centerlineLatitudeLongitude(csv_data=None, optional_cutoff=None)
```
* **[REQUIRED]** csv_data (string): File location of the text file to convert
* [OPTIONAL] optional_cutoff (int): Include only the first x amount of the data to chart (useful for debugging)

```python
import centerline_width
centerline_width.centerlineLatitudeLongitude(csv_data="data/river_coords.csv", 
					optional_cutoff=cutoff)
```
Output: `[(-92.86788596499872, 30.03786596717931), (-92.86789573751797, 30.037834641974108), (-92.8679141386283, 30.037789636848878), (-92.8679251193248, 30.037756853899904), (-92.86796903819089, 30.03765423778148), (-92.86797335733262, 30.037643336049054), (-92.8679920356456, 30.037592224469797), (-92.86800576063828, 30.037555441489403), (-92.86800841510367, 30.037546512833107), (-92.8680119498663, 30.03753043193875)]`

## Plot Centerline in Matplotlib
### Plot the centerline created from a list of right and left banks with Voronoi vertices

```
plotCenterline(csv_data=None,
		display_all_possible_paths=False, 
		plot_title=None, 
		save_plot_name=None, 
		displayVoronoi=False,
		optional_cutoff=None)
```
* **[REQUIRED]** csv_data (string): File location of the text file to convert
* [OPTIONAL] display_all_possible_paths (boolean): Display all possible paths, not just the centerline (useful for debugging)
* [OPTIONAL] plot_title (string): Change plot title, defaults to "River Coordinates: Valid Centerline = True/False, Valid Polygon = True/False"
* [OPTIONAL] save_plot_name (string): Save the plot with a given name and location
* [OPTIONAL] displayVoronoi (boolean): Overlay Voronoi diagram used to generate centerline
* [OPTIONAL] optional_cutoff (int): Include only the first x amount of the data to chart (useful for debugging)

```python
import centerline_width
centerline_width.plotCenterline(csv_data="data/river_coords.csv", 
				display_all_possible_paths=False, 
				displayVoronoi=False, 
				optional_cutoff=550)
```
Output:
![river_coords_centerline+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/river_coords_centerline.png)

## Future Work: Coming Soon
### Plot the centerline width
Plot the width of the river based on the centerline

Display Centerline at even intervals Voronoi generated centerline
```
plotCenterlineWidth(csv_data=None,
		plot_title=None, 
		save_plot_name=None, 
		display_true_centerline=True,
		n_interprolate_centerpoints=None,
		transect_span_distance=3,
		apply_smoothing=False,
		flag_intersections=True,
		remove_intersections=False,
		optional_cutoff=None)
```
* **[REQUIRED]** csv_data (string): File location of the text file to convert
* [OPTIONAL] plot_title (string): Change plot title, defaults to "River Coordinates: Valid Centerline = True/False, Valid Polygon = True/False"
* [OPTIONAL] save_plot_name (string): Save the plot with a given name and location
* [OPTIONAL] display_true_centerline (boolean): Display generated true centerline based on Voronoi diagrams
* [OPTIONAL] n_interprolate_centerpoints (int): Recreate centerline coordinates with n evenly spaced points, defaults to the number of rows in the csv file
* [OPTIONAL] transect_span_distance (int): Sum up n amount of points around a centerpoint to determine the slope (increase to decrease the impact of sudden changes), defaults to 6, must be greater than 2 (since the slope is found from the difference in position between two points), measured orthogonal to the centerline
* [OPTIONAL] apply_smoothing (bool): Apply a B-spline smoothing to centerline
* [OPTIONAL] flag_intersections (bool): Display intersecting width lines as red in graph, defaults to True
* [OPTIONAL] remove_intersections (bool): Iterative remove intersecting lines, to maintain the most width lines, but return only non-intersecting width lines, defaults to False
* [OPTIONAL] optional_cutoff (int): Include only the first x amount of the data to chart (useful for debugging)

Transect span distance:
![transect_span_distance](https://user-images.githubusercontent.com/22159116/227870492-69d105b2-0d3e-4d50-90d9-e938400a58fb.png)

```
import centerline_width
centerline_width.plotCenterlineWidth(csv_data="data/river_coords.csv", 
				save_plot_name="data/river_coords_width.png", 
				display_true_centerline=False,
				n_interprolate_centerpoints=None,
				transect_span_distance=3,
				apply_smoothing=True,
				flag_intersections=True,
				remove_intersections=True,
				optional_cutoff=cutoff)
```
![river_coords_width+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/river_coords_width.png)

### Types of Centerlines
- Voronoi centerline: centerline generated by Voronoi vertices
- Evenly Spaced Centerline: centerline calculated but evenly spaced with a fixed number of points, instead of the points generated by the Vornoi diagram
- Smoothed Centerline: centerline smoothed by a b-spline

### Return Width of River
```
riverWidthFromCenterline(csv_data=None,
			n_interprolate_centerpoints=None,
			transect_span_distance=3,
			apply_smoothing=True,
			remove_intersections=False,
			save_to_csv=None,
			optional_cutoff=None)
```
* **[REQUIRED]** csv_data (string): File location of the text file to convert
* [OPTIONAL] n_interprolate_centerpoints (int): Recreate centerline coordinates with n evenly spaced points, defaults to the number of rows in the csv file
* [OPTIONAL] transect_span_distance (int): Sum up n amount of points around a centerpoint to determine the slope (increase to decrease the impact of sudden changes), defaults to 6, must be greater than 2 (since the slope is found from the difference in position between two points), measured orthogonal to the centerline
* [OPTIONAL] apply_smoothing (bool): Apply a B-spline smoothing to centerline
* [OPTIONAL] remove_intersections (bool): Iterative remove intersecting lines, to maintain the most width lines, but return only non-intersecting width lines, defaultsl to True
* [OPTIONAL] optional_cutoff (int): Include only the first x amount of the data to chart (useful for debugging)

```
river_width_dict = centerline_width.riverWidthFromCenterline(csv_data="data/river_coords.csv",
							transect_span_distance=3,
							apply_smoothing=True,
							remove_intersections=True,
							optional_cutoff=30)
```
Width dictionary = `{(-92.86781253030335, 30.038091261157252): 0.0012665460374170527, (-92.86785237492347, 30.037936004362408): 0.0012253609552254057, (-92.86788265990378, 30.037859857932435): 0.001166563476716173, (-92.86791593240025, 30.037784209097087): 0.0011192823818546845, (-92.86794925171479, 30.037708690068605): 0.0010967819847309656, (-92.86797967714938, 30.03763293305923): 0.001072182634460594}`

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

## Developer Notes: Tech Debt and Bugs
* clean up README with examples, working functions, and remove unused functions from __init__
* README overview of all three types of centerlines (voronoi generated, evenly spaced, gaussian smoothed)
* Combine backend functionality for plotCenterline and plotCenterlineWidth into a shared component
* Combine backend for riverWidthFromCenterline() and plotCenterline()
* Verify error handling for public functions
* Check that smoothing filter option does not produce a line that goes outside of the polygon
* Return the length of the centerline (length of the left/right bank)
* Return the knickpoints (occurrences of knickpoints)

## Citations
Based on similar work written in R:

>Golly, A. and Turowski, J. M.: Deriving principal channel metrics from bank and long-profile geometry with the R package cmgo, Earth Surf. Dynam., 5, 557-570, https://doi.org/10.5194/esurf-5-557-2017, 2017.

[Github - CMGO](https://github.com/AntoniusGolly/cmgo)

 <p align="center">
  <img src="https://user-images.githubusercontent.com/22159116/222872092-e0b579cc-4f84-4f49-aa53-397785fb9bf2.png" />
  <img src="https://user-images.githubusercontent.com/22159116/222872119-7c485ee2-4ffd-413a-9e4f-b043b122d2bb.png" />
  <img src="https://user-images.githubusercontent.com/22159116/222872019-12931138-9e10-4e51-aa1e-552e72d09af0.png" />
</p>
