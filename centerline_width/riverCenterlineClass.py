# River object class used for all functions and centerline functions

# External Python libraries (installed via pip install)
import pandas as pd

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

class riverCenterline:
	def __init__(self,
				csv_data=None,
				optional_cutoff=None,
				interpolate_data=False,
				interpolate_n=5,
				interpolate_n_centerpoints=None, 
				equal_distance=10,
				ellipsoid="WGS84"):
		centerline_width.errorHandlingRiverCenterlineClass(csv_data=csv_data,
															optional_cutoff=optional_cutoff,
															interpolate_data=interpolate_data,
															interpolate_n=interpolate_n,
															interpolate_n_centerpoints=interpolate_n_centerpoints,
															equal_distance=equal_distance,
															ellipsoid=ellipsoid)

		# Description and dataframe
		self.river_name = csv_data
		self.interpolate_data = interpolate_data
		self.interpolate_n = interpolate_n
		df = pd.read_csv(csv_data)
		if optional_cutoff:
			df = df.head(optional_cutoff)
		self.df_len = len(df)
		self.interpolate_n_centerpoints = interpolate_n_centerpoints
		if self.interpolate_n_centerpoints is None: self.interpolate_n_centerpoints = self.df_len
		self.ellipsoid = ellipsoid

		# Left and Right Coordinates from the given csv data and data cutoff
		left_bank_coordinates, right_bank_coordinates = centerline_width.leftRightCoordinates(df)
		if interpolate_data:
			right_bank_coordinates, left_bank_coordinates = centerline_width.interpolateBetweenPoints(left_bank_coordinates, right_bank_coordinates, interpolate_n)
		self.left_bank_coordinates = left_bank_coordinates
		self.right_bank_coordinates = right_bank_coordinates
		self.left_bank_relative_coordinates, self.right_bank_relative_coordinates = centerline_width.relativeBankCoordinates(self.left_bank_coordinates, self.right_bank_coordinates, self.ellipsoid)

		# Right/Length Bank Length
		self.rightBankLength = centerline_width.centerlineLength(centerline_coordinates=right_bank_coordinates, ellipsoid=self.ellipsoid)
		self.leftBankLength = centerline_width.centerlineLength(centerline_coordinates=left_bank_coordinates, ellipsoid=self.ellipsoid)

		# Decimal Degrees: River polygon, position of the top/bottom polygon
		river_bank_polygon, top_bank, bottom_bank = centerline_width.generatePolygon(self.left_bank_coordinates, self.right_bank_coordinates, coord_type="Decimal Degrees")
		self.bank_polygon = river_bank_polygon
		self.top_bank = top_bank
		self.bottom_bank = bottom_bank

		# Area contained within river polygon
		self.riverArea = centerline_width.calculateRiverArea(self.bank_polygon, self.ellipsoid)

		# Relative Coordinates: River polygon, position of the top/bottom polygon
		river_bank_polygon, top_bank, bottom_bank = centerline_width.generatePolygon(self.left_bank_relative_coordinates, self.right_bank_relative_coordinates, coord_type="Relative Distance")
		self.bank_polygon_relative = river_bank_polygon
		self.top_bank_relative = top_bank
		self.bottom_bank_relative = bottom_bank

		# Decimal Degrees; Voronoi generated by left/right bank coordinates
		river_bank_voronoi = centerline_width.generateVoronoi(self.left_bank_coordinates, self.right_bank_coordinates, coord_type="Decimal Degrees")
		self.bank_voronoi = river_bank_voronoi

		# Relative Distance; Voronoi generated by left/right bank coordinates
		river_bank_voronoi = centerline_width.generateVoronoi(self.left_bank_relative_coordinates, self.right_bank_relative_coordinates, coord_type="Relative Distance")
		self.bank_voronoi_relative = river_bank_voronoi

		# Decimal Degrees all possible paths: starting/ending node, all possible paths (ridges), paths dictionary
		starting_node, ending_node, x_ridge_point, y_ridge_point, shortest_path_coordinates = centerline_width.centerlinePath(self.bank_voronoi, self.bank_polygon, self.top_bank, self.bottom_bank)
		self.starting_node = starting_node # starting position for centerline
		self.ending_node = ending_node # ending position for centerline
		self.x_voronoi_ridge_point = x_ridge_point # Voronoi x positions
		self.y_voronoi_ridge_point = y_ridge_point # Voronoi y positions

		# Relative Distances all possible paths: starting/ending node, all possible paths (ridges), paths dictionary
		self.starting_node_relative = centerline_width.relativeSingleCoordinate(self.left_bank_coordinates[0], self.starting_node, self.ellipsoid) # starting position for centerline
		self.ending_node_relative = centerline_width.relativeSingleCoordinate(self.left_bank_coordinates[0], self.ending_node, self.ellipsoid) # ending position for centerline
		x_relative_ridges, y_relative_ridges = centerline_width.relativeRidgeCoordinates(self.left_bank_coordinates[0], self.x_voronoi_ridge_point, self.y_voronoi_ridge_point, self.ellipsoid)
		self.x_voronoi_ridge_point_relative = x_relative_ridges # Voronoi relative x positions
		self.y_voronoi_ridge_point_relative = y_relative_ridges # Voronoi relative y positions

		# Voronoi Centerline Coordinates
		self.centerlineVoronoi = shortest_path_coordinates

		# Centerline length
		self.centerlineLength = centerline_width.centerlineLength(centerline_coordinates=shortest_path_coordinates, ellipsoid=self.ellipsoid)
		self.equal_distance = equal_distance

		# The different types of Centerline coordinates
		self.centerlineEqualDistance = centerline_width.equalDistanceCenterline(centerline_coordinates=self.centerlineVoronoi,
																				equal_distance=self.equal_distance,
																				ellipsoid=self.ellipsoid)
		self.centerlineEvenlySpaced = centerline_width.evenlySpacedCenterline(centerline_coordinates=self.centerlineVoronoi,
																				number_of_fixed_points=self.interpolate_n_centerpoints)
		self.centerlineSmoothed = centerline_width.smoothedCoordinates(river_object=self, centerline_coordinates=self.centerlineEvenlySpaced,
																		interprolate_num=self.interpolate_n_centerpoints)

		# Relative Distance from bottom left bank point to each Centerline coordinates
		self.centerlineVoronoiRelative = centerline_width.relativeCenterlineCoordinates(self.left_bank_coordinates[0], self.centerlineVoronoi, self.ellipsoid)
		self.centerlineEqualDistanceRelative = centerline_width.relativeCenterlineCoordinates(self.left_bank_coordinates[0], self.centerlineEqualDistance, self.ellipsoid)
		self.centerlineEvenlySpacedRelative = centerline_width.relativeCenterlineCoordinates(self.left_bank_coordinates[0], self.centerlineEvenlySpaced, self.ellipsoid)
		self.centerlineSmoothedRelative = centerline_width.relativeCenterlineCoordinates(self.left_bank_coordinates[0], self.centerlineSmoothed, self.ellipsoid)

	def plotCenterline(self,
						centerline_type="Voronoi",
						marker_type="line",
						centerline_color="black",
						dark_mode=False,
						equal_axis=False,
						display_all_possible_paths=False,
						plot_title=None,
						save_plot_name=None,
						show_plot=True,
						display_voronoi=False,
						coordinate_unit="Decimal Degrees"):
		centerline_width.plotCenterline(river_object=self,
										centerline_type=centerline_type,
										marker_type=marker_type,
										centerline_color=centerline_color,
										dark_mode=dark_mode,
										equal_axis=equal_axis,
										display_all_possible_paths=display_all_possible_paths, 
										plot_title=plot_title, 
										save_plot_name=save_plot_name, 
										display_voronoi=display_voronoi,
										show_plot=show_plot,
										coordinate_unit=coordinate_unit)

	def plotCenterlineWidth(self,
							plot_title=None, 
							save_plot_name=None, 
							display_true_centerline=True,
							transect_span_distance=3,
							transect_slope="Average",
							apply_smoothing=False,
							flag_intersections=True,
							remove_intersections=False,
							dark_mode=False,
							equal_axis=False,
							show_plot=True,
							coordinate_unit="Decimal Degrees"):
		centerline_width.plotCenterlineWidth(river_object=self,
											plot_title=plot_title, 
											save_plot_name=save_plot_name, 
											display_true_centerline=display_true_centerline,
											transect_span_distance=transect_span_distance,
											transect_slope=transect_slope,
											apply_smoothing=apply_smoothing,
											flag_intersections=flag_intersections,
											remove_intersections=remove_intersections,
											dark_mode=dark_mode,
											equal_axis=equal_axis,
											show_plot=show_plot,
											coordinate_unit=coordinate_unit)

	def riverWidthFromCenterline(self,
								transect_span_distance=3,
								transect_slope="Average",
								apply_smoothing=True,
								remove_intersections=False,
								coordinate_unit="Decimal Degrees",
								coordinate_reference="Centerline",
								save_to_csv=None):
		return centerline_width.riverWidthFromCenterline(river_object=self,
														transect_span_distance=transect_span_distance,
														transect_slope=transect_slope,
														apply_smoothing=apply_smoothing,
														remove_intersections=remove_intersections,
														coordinate_unit=coordinate_unit,
														coordinate_reference=coordinate_reference,
														save_to_csv=save_to_csv)

	def saveCenterlineCSV(self, 
						save_to_csv=None,
						latitude_header=None,
						longitude_header=None, 
						centerline_type="Voronoi",
						coordinate_unit="Decimal Degrees"):
		return centerline_width.saveCenterlineCSV(river_object=self,
												save_to_csv=save_to_csv,
												latitude_header=latitude_header, 
												longitude_header=longitude_header, 
												centerline_type=centerline_type,
												coordinate_unit=coordinate_unit)

	def saveCenterlineMAT(self,
						save_to_mat=None, 
						latitude_header=None,
						longitude_header=None, 
						centerline_type="Voronoi",
						coordinate_unit="Decimal Degrees"):
		return centerline_width.saveCenterlineMAT(river_object=self,
												save_to_mat=save_to_mat,
												latitude_header=latitude_header,
												longitude_header=longitude_header,
												centerline_type=centerline_type,
												coordinate_unit=coordinate_unit)
