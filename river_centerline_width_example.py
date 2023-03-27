# Find the center point and width between latitude/longitude points along right/left river bank
import centerline_width

if __name__ == "__main__":
	centerline_width.extractPointsToTextFile(left_kml="data/leftbank.kml", right_kml="data/rightbank.kml", text_output_name="data/river_coords.txt")
	centerline_width.convertColumnsToCSV(text_file="data/river_coords.txt", flipBankDirection=True)

	# Valid Examples
	cutoff = None
	#cutoff = 10
	#cutoff = 15 # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	#cutoff = 30
	#cutoff = 100 # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	cutoff = 550 # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	# Invalid Examples
	#cutoff = 5 # invalid centerline, invalid path, valid polygon, invalid starting node, invalid ending nodes
	#cutoff = 250 # valid centerline, valid path, invalid polygon, valid starting node, valid ending nodes
	#cutoff = 40 # invalid centerline, valid path, valid polgyon, invalid starting node, valid ending node
	#cutoff = 700 # invalid centerline, valid path, valid polgyon, invalid starting node, valid ending node
	#cutoff = 1000 # invalid centerline, invalid path, invalid polgyon, invalid starting node, valid ending node

	# Plot river banks
	#centerline_width.plotCenterline(csv_data="data/river_coords.csv", 
	#								save_plot_name="data/river_coords_centerline.png", 
	#								display_all_possible_paths=False, 
	#								displayVoronoi=False,
	#								displayCenterline=True,
	#								optional_cutoff=cutoff)

	centerline_width.plotCenterline(csv_data="data/river_coords.csv", 
									save_plot_name="data/river_coords_width.png", 
									displayCenterline=True,
									plot_width_lines=True,
									n_interprolate_centerpoints=5000,
									transect_span_distance=100,
									optional_cutoff=cutoff)
	exit()
	# Return the latitude/longtiude coordinates for the centerline
	centerline_long_lat_coordinates = centerline_width.centerlineLatitudeLongitude(csv_data="data/river_coords.csv", 
																					optional_cutoff=cutoff)
	#print(centerline_long_lat_coordinates)

	# Return the width of the river for each centerline vertex (distance from right, left, total)
	river_width_dict = centerline_width.riverWidthFromCenterline(csv_data="data/river_coords.csv", 
																centerline_coordinates=centerline_long_lat_coordinates,
																save_to_csv="data/river_width.csv",
																optional_cutoff=cutoff)

	# Centerline Total Length (in degrees)
	exit()
	centerline_length = centerline_width.centerlineLength(centerline_coordinates=centerline_long_lat_coordinates)
	print("Centerline Length (degrees) = {0}".format(centerline_length))

